import json
from unittest.test.test_assertions import Test_Assertions

import pytest
from server.request import Request


def test_to_json() -> None:
    request = Request("subscribe", "default")

    json_message = request.to_json()
    assert json_message == '{"action": "subscribe", "stream": "default"}'


def test_from_json() -> None:
    data = json.loads('{"action": "subscribe", "stream": "default"}')

    request = Request.from_json(data)

    Test_Assertions().assertIsInstance(request, Request)
    assert request.action == "subscribe"
    assert request.stream == "default"


def test_from_json_without_field_raises_exception() -> None:
    data = json.loads("{}")

    with pytest.raises(KeyError):
        Request.from_json(data)
