# School PubSub

## Installation

## Getting Started

### Configuration

In order to publish or subscribe, you will need to retrieve a backend. We use the `get_backend` function for this:

```python
channel = 'some-channel'
appname = 'myapp'

#def get_backend(module, backend_class, channel, appname):

# get a redis backend:
backend = get_backend('backends', 'RedisBackend')

backend = get_backend('backends', 'PubNubBackend')
```

**Notes**
* `channel` - the global channel used to send this information out on
* `appname` - the name of the application, this is used for registration and acknowledgement

Find out more about various backends and how to configure
[on the backends page](/backends/)


### Publisher

Publishing is easy:

```python{3}
event = 'myevent'
data = { "foo": "bar" }
publish(backend, event, data)
```

### Subscriber

Subscribing is a little more complex

#### 1. Define your event routing

Event routing will delegate the event `data` to a defined function based on the **event key**.

Event routing is determined by matching the keydata to a module and a test to run. For example:

```python
FUNCTION_MAPPER = {
    'myevent': {
        "module": "myapp.tasks"
        "method": "do_something"
    }

    # if we receive the event `myevent`
    # with the data {"foo":"bar"}
    # on the channel we're listening on

    # with this mapping, it will essentially run:
    # from myapp.tasks import do_something
    # do_something({
    #     "key": "myevent",
    #     "data": {"foo":"bar"}
    # })
}
```

#### Create a subscriber and have it listen on the channel

```python

app_name = 'myapp'.format(str(uuid.uuid4()))
backend = get_backend('school_backends', BACKEND, CHANNEL, app_name)
listen(backend, FUNCTION_MAPPER)
```

## Contributing / Developing

### Running locally

```bash
docker-compose up
```

## Backends


