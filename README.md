# PubSubLibrary

Simple Publish Subscribe python library

[![PyPI version](https://badge.fury.io/py/school_pubsub.svg)](https://badge.fury.io/py/school_pubsub)

### Demo

```
docker-compose up
```

(see `example.py`)

### Installation

```
pip install school_pubsub
```

### Backends available

* PubNub
* MockBackend (coming soon)
* Pika (RabbitMQ) (coming soon)
* Celery (coming soon)

### Gettings started

**Example usage**

**Publish**

```
pubsub = get_backend('backends', 'PubNubBackend', 'some-channel')
key = 'myapp.did_something'
payload: {"foo": "bar"}
pubsub.publish(key, payload)
```

**Subscribe**

```
"""
listen's for all events on 'some-channel', will only execute events which have a key
that matches in functionmapper. e.g.: `myapp.didsomething`

e.g.: an event like above. e.g.::

{ key: "myapp.didsomething",
  payload: {"foo": "bar"}
}

Would result in the subscriber calling: `thisapp.tasks.handle_did_something(payload)`
"""

functionmapper = {
    "myapp.didsomething": {
        "module": "thisapp.tasks",
        "method": "handle_did_something"
    }
}
pubsub = get_backend('backends', 'PubNubBackend', 'some-channel')

# this is a run_forever, you'll want to run it as it's own process
pubsub.subscribe(functionmapper)

```

### Reporting / monitoring:

**Find all apps registered against an event:**

`smembers pubsub.events.{event}.subscribers`

```
redis:6379> smembers pubsub.events.baz.subscribers
1) "subscriber-36da2988-4737-40a8-89e7-ee3efa5907c6"
2) "subscriber-d409466c-2052-43cd-a75c-89e45537bb83"
3) "subscriber-168e846d-00b5-463b-93b6-be8243c42cc9"
4) "subscriber-9b612545-e389-4fba-8733-123a8930c8d6"
5) "subscriber-8250cf68-2bfb-47bc-a3d2-f559bf700a72"
```

**Find all events for an app:**

`smembers pubsub.applications.{appname}.events`

```
redis:6379> smembers pubsub.applications.subscriber-1.events
1) "bus"
2) "baz"
3) "bar"
4) "foo"
```

**Find all ID's for a type of event event:**

`keys pubsub.events.actions.{event}.*.published`

```
redis:6379> keys pubsub.events.actions.baz.*.published
 1) "pubsub.events.actions.baz.744f4670-097d-42fc-9eec-e523da0efa20.published"
 2) "pubsub.events.actions.baz.a6e22989-9e4e-4813-8c6d-f7f47b6bd2b0.published"
 3) "pubsub.events.actions.baz.80df29f2-fb97-4cdb-9299-92be739bb29b.published"
...
```

**Find all the apps that received a message for a certain event:**

`smembers pubsub.events.actions.baz.{id}.received`

```
redis:6379> smembers pubsub.events.actions.baz.3dc9db5c-94b7-4ec1-8b4b-99dd0fa34e02.received
1) "subscriber-36da2988-4737-40a8-89e7-ee3efa5907c6"
2) "subscriber-8250cf68-2bfb-47bc-a3d2-f559bf700a72"
3) "subscriber-9b612545-e389-4fba-8733-123a8930c8d6"
```

**Pub and Sub!**

```
redis:6379> smembers pubsub.events.actions.bus.e134537c-2dfa-45ea-ae8f-288a2180cef8.published
1) "my.app"
redis:6379> smembers pubsub.events.actions.bus.e134537c-2dfa-45ea-ae8f-288a2180cef8.received
1) "subscriber-36da2988-4737-40a8-89e7-ee3efa5907c6"
2) "subscriber-8250cf68-2bfb-47bc-a3d2-f559bf700a72"
3) "subscriber-9b612545-e389-4fba-8733-123a8930c8d6"
```

### Packaging:

```python setup.py sdist upload```
