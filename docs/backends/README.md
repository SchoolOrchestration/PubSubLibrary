# PubSub Backends

> The following are supported as backends for handling the pub/sub

## Redis

The following environment variables will be used:

| Config        | Requred       | Default  |
| ------------- |:-------------:| -----:|
| `PUBSUB_HOST`       | no | 'redis' |
| `PUBSUB_PASSWORD`   | no | `None` |
| `PUBSUB_PORT`       | no | `6379` |
| `PUBSUB_INDEX`      | no | `0` |

for checking the health of the subscriber (this needs to be run in the same directory as the subscriber is running)
```python
from pubsub import subscriber_health

backend = get_backend('school_backends', 'RedisBackend', 'some-channel', 'app-name')
subscriber_health(backend)
```

**Settings**

## PubNub

**Settings**

## Writing a custom backend

..
