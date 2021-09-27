import asyncio
import json
from datetime import datetime
from typing import List
from unittest.mock import Mock

import pytest
from fastapi import WebSocket
from freezegun import freeze_time
from server.client_manager import Client, ClientManager
from server.delivery_manager import DeliveryManager
from server.number_generator import NumberGenerator
from server.response import Response


class MockClient(Client):
    def __init__(self, id: str, ws: WebSocket) -> None:
        self.id = id
        self.ws = ws
        self.messages: List[Response] = []

    async def send_message(self, message: str) -> None:
        parsed_message = json.loads(message)
        self.messages.append(
            Response(
                content=parsed_message["content"],
                timestamp=datetime.fromisoformat(parsed_message["timestamp"]),
            )
        )


@pytest.fixture
def ws() -> WebSocket:
    return Mock(spec=WebSocket)


@pytest.mark.asyncio
@freeze_time("2021-09-27 21:00:00", tick=True)
async def test_delivery_manager(ws: Mock) -> None:
    client = MockClient("1", ws)
    client_manager = ClientManager()
    client_manager.add(client)

    delivery_manager = DeliveryManager(NumberGenerator(interval_in_seconds=0.01), client_manager)
    task = asyncio.create_task(delivery_manager.deliver_messages())

    # Since interval_in_seconds=0.01,
    # at least [0,1] should be sent in 0.05s.
    await asyncio.sleep(0.05)

    task.cancel()

    assert len(client.messages) >= 2

    min_time = datetime.fromisoformat("2021-09-27 21:00:00")
    max_time = datetime.fromisoformat("2021-09-27 21:00:01")

    msg = client.messages.pop(0)
    assert msg.content == 0
    assert min_time < msg.timestamp < max_time

    msg = client.messages.pop(0)
    assert msg.content == 1
    assert min_time < msg.timestamp < max_time
