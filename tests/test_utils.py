from unittest.mock import Mock

import server.utils as utils
from fastapi import WebSocket


def test_client_name():
    ws: WebSocket = Mock(spec=WebSocket)
    ws.client.host = "127.0.0.1"
    ws.client.port = "1234"

    client_name = utils.client_name(ws)

    assert client_name == "127.0.0.1:1234"
