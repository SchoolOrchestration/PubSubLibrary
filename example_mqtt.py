#!/usr/bin/python
from pubsub import get_backend, publish, listen
import random
import time
import json
import sys
import uuid

CHANNEL = 'my.project.channel'

# this is an example of what a function_mapper might look like
FUNCTION_MAPPER = {
    CHANNEL: {
        'module': 'example_mqtt',
        'method': 'foo'
    }
}

events = ['foo', 'bar', 'baz', 'bus']


def get_function_mapper():
    """
    Generate a random function mapping
    """
    num_events_to_subscribe_to = random.randint(0, len(events))
    mapper = {}
    random.shuffle(events)
    for x in range(0, num_events_to_subscribe_to):
        mapper.update({
            events[x]: {
                'module': 'example_mqtt',
                'method': events[x]
            }
        })
    return mapper


def foo(data):
    print("###################################################")
    print("foo!")
    print(type(data))
    print("###################################################")


def bar(data):
    print("###################################################")
    print("bar!")
    print(type(data))
    print("###################################################")


def baz(data):
    print("###################################################")
    print("baz!")
    print(type(data))
    print("###################################################")


def bus(data):
    print("###################################################")
    print("bus!")
    print(type(data))
    print("###################################################")


# def message_received():
#     print "<< message received: "

BACKEND = 'MQTTBackend'  # options: RedisBackend, PubNubBackend, ..


def publisher():
    """
    Publishes a random blob of data after a random number of seconds
    """
    backend = get_backend('school_backends', BACKEND, CHANNEL, 'my.app')
    for x in range(0, 100):
        data = {"foo": "bar", "nested": [{"foo": "baz"}]}

        print("-----------------------")
        publish(backend, random.choice(events), data)
        sleep_time = random.choice(range(0, 10))
        print("Next publication in {}".format(sleep_time))
        time.sleep(sleep_time)


def subscribe():
    """
    listen for things getting published
    """
    RANDOM_TIME = random.randint(0,10)
    print("starting in {}".format(RANDOM_TIME))
    time.sleep(RANDOM_TIME)

    app_name = 'subscriber{}'.format(str(uuid.uuid4()))
    backend = get_backend('school_backends', BACKEND, CHANNEL, app_name)
    listen(backend, get_function_mapper())


if __name__ == "__main__":
    print(str(sys.argv))
    if len(sys.argv) == 1:
        publisher()
    else:
        subscribe()
