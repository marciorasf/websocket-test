from server.message import Message
from unittest.test.test_assertions import Test_Assertions
import json


def test_to_json():
    message = Message("subscribe", {"stream": "all"})

    json_message = message.to_json()
    assert json_message == '{"action": "subscribe", "payload": {"stream": "all"}}'


def test_from_json():
    data = json.loads('{"action": "subscribe", "payload": {"stream": "all"}}')

    message = Message.from_json(data)

    Test_Assertions().assertIsInstance(message, Message)
    assert message.action == "subscribe"
    assert message.payload == {"stream": "all"}
