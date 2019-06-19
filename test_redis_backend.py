"""
Test the PubNub backend
"""
from school_backends import RedisBackend
import unittest


class TestPubNubBackend(unittest.TestCase):
    def setUp(self):
        self.pb = RedisBackend(channel="test-channel", appname="test", instance_id=1)

    def test_publish(self):
        example_payload = {"foo": "bar"}
        self.pb.publish("example.test", example_payload)


if __name__ == "__main__":
    unittest.main()
