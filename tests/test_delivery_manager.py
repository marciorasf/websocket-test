import asyncio
from typing import List
from unittest.mock import Mock

import pytest
from fastapi import WebSocket
from server.client_manager import Client, ClientManager
from server.delivery_manager import DeliveryManager
from server.number_generator import NumberGenerator


class MockClient(Client):
    def __init__(self, id: str, ws: WebSocket) -> None:
        self.id = id
        self.ws = ws
        self.numbers: List[int] = []

    async def send_number(self, number: int) -> None:
        self.numbers.append(number)


@pytest.fixture
def ws() -> WebSocket:
    return Mock(spec=WebSocket)


@pytest.mark.asyncio
async def test_delivery_manager(ws: Mock) -> None:
    client = MockClient("1", ws)
    client_manager = ClientManager()
    client_manager.add(client)

    delivery_manager = DeliveryManager(NumberGenerator(interval_in_seconds=0.01), client_manager)
    task = asyncio.create_task(delivery_manager.deliver_numbers())

    # Since interval_in_seconds=0.01,
    # at least [0,1] should be sent in 0.05s.
    await asyncio.sleep(0.05)

    task.cancel()

    assert 0 in client.numbers
    assert 1 in client.numbers
