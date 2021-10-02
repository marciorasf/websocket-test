from unittest.mock import Mock

import pytest
from fastapi import WebSocket
from server.client import Client


@pytest.fixture
def ws() -> WebSocket:
    return Mock(spec=WebSocket)


@pytest.mark.asyncio
async def test_send_message(ws: Mock) -> None:
    client = Client("1", ws)
    await client.send_message("ola")

    ws.send_text.assert_called()
