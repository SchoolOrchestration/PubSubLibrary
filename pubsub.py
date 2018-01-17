"""
A module for abstracting pub/sub backends (providing a consistent API across
backends)

Typical usage:

```
pubsub = pubsub.get_backend('backends', 'PubNubBackend', 'some-channel')
pubsub.publish('app.foo', {..})
pubsub.subscribe() # this is a blocking call
```
"""
import importlib


def get_backend(module, backend_class, channel):
    """Get a pubsub object. e.g.: `get_backend('backends', 'PubNubBackend')`"""
    mod = importlib.import_module(module)
    return getattr(mod, backend_class)(channel)


def publish(backend, key, payload):
    backend.publish(key, payload)


def listen(backend, function_mapper):
    """Process that runs forever listening on configured channel"""
    backend.subscribe(function_mapper)

