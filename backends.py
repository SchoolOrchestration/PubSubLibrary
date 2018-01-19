from pubnub.pubnub import PubNub, SubscribeListener
from pubnub.pnconfiguration import PNConfiguration
import importlib
import redis
import json
import time
import os


def get_secret(secret_name, default=None):
    """Returns a docker secret"""
    try:
        return open('/run/secrets/{}'.format(secret_name)).read().rstrip()
    except FileNotFoundError:
        return os.environ.get(secret_name, default)


def call_mapped_method(message, function_mapper: dict):
    """
    fund method description from function_mapper[message.key]
    and execute function_mapper[message.key](message)

    Where message is a python dict
    """
    if isinstance(message, dict) and not isinstance(message['data'], int):
        data = message['data'].decode("utf-8")
        event_key = message['channel'].decode("utf-8")
        task_definition = function_mapper.get(event_key, None)
        if task_definition is not None:
            mod = importlib.import_module(task_definition.get('module'))
            method = task_definition.get('method')
            getattr(mod, method)(normalize(data)['payload'])


def normalize(content, as_json=True):
    """
    Take a string, bytestring, dict or even a json object and turn it into a
    pydict
    """
    if as_json:
        content = content.replace("\"", "|")
        content = content.replace("'", "\"")
        content = content.replace("|", "'")
        return json.loads(content)


class RedisBackend:

    def __init__(self, channel):
        self.channel = channel
        self.redis = redis.StrictRedis(
            host=get_secret('PUBSUB_HOST', 'redis'),
            port=6379,
            db=0
        )

    def publish(self, key, payload):
        data = {
            "key": key,
            "payload": payload
        }
        return self.redis.publish(self.channel, data)

    def subscribe(self, function_mapper):
        p = self.redis.pubsub()
        p.subscribe(self.channel)

        while True:
            message = p.get_message()
            if message:
                call_mapped_method(message, function_mapper)
            time.sleep(0.001)  # be nice to the system :)


class PubNubBackend:
    """
    Usage:

    **Subscribe**
    ```
    pubsub = PubNubBackend(channel, pub_key, sub_key)
    pubsub.subscribe()
    ```

    Requires environment variables:
    * PUBNUB_PUBLISH_KEY
    * PUBNUB_SUBSCRIBE_KEY

    """

    def __init__(self, channel):
        publish_key = get_secret('PUBNUB_PUBLISH_KEY', None)
        subscribe_key = get_secret('PUBNUB_SUBSCRIBE_KEY', None)

        if None in [subscribe_key, publish_key]:
            msg = ('Please make sure you\'ve set environment varialbes: '
                   'PUBNUB_PUBLISH_KEY and PUBNUB_SUBSCRIBE_KEY')
            raise Exception(msg)
        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = subscribe_key
        pnconfig.publish_key = publish_key
        pnconfig.ssl = False
        self.channel = channel
        self.pubnub = PubNub(pnconfig)

    def publish(self, key, payload):
        def publish_callback(result, status):

            if result:
                print(result)
            if status.error is not None:
                raise Exception('PubSub publish error: %s: %s' %
                                (status.error, status.error_data))
        data = {
            "key": key,
            "payload": payload
        }
        self.pubnub.publish() \
            .channel(self.channel) \
            .message(data) \
            .async(publish_callback)

    def listen(self, function_mapper):
        """
        Implements a multicast pub/sub. It is the responsibility of the
        subscriber determine if it needs to perform any actions based on
        the message key

        functionmapper is a dict that maps payload keys to methods to call
        Methods will receive the payload as the first argument.

        e.g.:

        ```
        function_mapper = {
            'test': {
                'module': 'config',
                'method': 'foo'
            }
        }
        ```
        """
        my_listener = SubscribeListener()
        self.pubnub.add_listener(my_listener)
        self.pubnub.subscribe().channels(self.channel).execute()
        # self.pubnub.add_channel_to_channel_group()\
        #     .channel_group("test")\
        #     .channels(channels)\
        #     .sync()

        my_listener.wait_for_connect()
        print('connected')

        while True:
            result = my_listener.wait_for_message_on(self.channel)
            print(result.message)
            event_key = result.message.get('key')
            task_definition = function_mapper.get(event_key, None)
            print('key: %s' % event_key)
            print('task definition: %s' % task_definition)

            if task_definition is not None:
                mod = importlib.import_module(task_definition.get('module'))
                method = task_definition.get('method')
                getattr(mod, method)(result.message)
