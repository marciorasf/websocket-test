import json
from unittest.test.test_assertions import Test_Assertions

import pytest
from server.message import Message


def test_to_json() -> None:
    message = Message("subscribe", {"stream": "all"})

    json_message = message.to_json()
    assert json_message == '{"action": "subscribe", "payload": {"stream": "all"}}'


def test_from_json() -> None:
    data = json.loads('{"action": "subscribe", "payload": {"stream": "all"}}')

    message = Message.from_json(data)

    Test_Assertions().assertIsInstance(message, Message)
    assert message.action == "subscribe"
    assert message.payload == {"stream": "all"}


def test_from_json_without_payload() -> None:
    data = json.loads('{"action": "subscribe"}')

    message = Message.from_json(data)

    Test_Assertions().assertIsInstance(message, Message)
    assert message.action == "subscribe"
    assert message.payload is None


def test_from_json_without_action_raises_exception() -> None:
    data = json.loads('{"payload": ""}')

    with pytest.raises(KeyError):
        Message.from_json(data)
