from server.message import Message


def test_to_json():
    message = Message("subscribe", {"stream": "all"})

    json_message = message.to_json()
    assert json_message == '{"action": "subscribe", "payload": {"stream": "all"}}'
