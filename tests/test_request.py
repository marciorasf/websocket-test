import json
from unittest.test.test_assertions import Test_Assertions

import pytest
from server.request import Request


def test_to_json() -> None:
    request = Request("subscribe", {"stream": "all"})

    json_message = request.to_json()
    assert json_message == '{"action": "subscribe", "payload": {"stream": "all"}}'


def test_from_json() -> None:
    data = json.loads('{"action": "subscribe", "payload": {"stream": "all"}}')

    request = Request.from_json(data)

    Test_Assertions().assertIsInstance(request, Request)
    assert request.action == "subscribe"
    assert request.payload == {"stream": "all"}


def test_from_json_without_payload() -> None:
    data = json.loads('{"action": "subscribe"}')

    request = Request.from_json(data)

    Test_Assertions().assertIsInstance(request, Request)
    assert request.action == "subscribe"
    assert request.payload is None


def test_from_json_without_action_raises_exception() -> None:
    data = json.loads('{"payload": ""}')

    with pytest.raises(KeyError):
        Request.from_json(data)
