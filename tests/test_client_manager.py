from unittest.mock import Mock

import pytest
from fastapi import WebSocket
from server.client_manager import Client, ClientManager


@pytest.fixture
def ws() -> WebSocket:
    return Mock(spec=WebSocket)


@pytest.mark.asyncio
async def test_client_send_message(ws: Mock) -> None:
    client = Client("1", ws)
    await client.send_message("ola")

    ws.send_text.assert_called()


def test_add() -> None:
    manager = ClientManager()

    manager.add(Client(id="1", ws=ws))
    manager.add(Client(id="2", ws=ws))

    assert len(manager) == 2


def test_get() -> None:
    manager = ClientManager()
    client = Client(id="1", ws=ws)
    manager.add(client)

    retrieved_client = manager.get("1")

    assert retrieved_client is client


def test_get_nonexistent_client() -> None:
    manager = ClientManager()

    client = manager.get("1")

    assert client is None


def test_contains() -> None:
    manager = ClientManager()
    client = Client(id="1", ws=ws)
    manager.add(client)

    assert manager.contains("1")
    assert not manager.contains("2")


def test_remove(ws: Mock) -> None:
    manager = ClientManager()
    manager.add(Client(id="1", ws=ws))
    manager.add(Client(id="2", ws=ws))

    manager.remove("1")

    assert len(manager) == 1


def test_remove_nonexistent_doesnt_raise_exception() -> None:
    manager = ClientManager()

    manager.remove("1")


def test_clients(ws: Mock) -> None:
    manager = ClientManager()
    c1 = Client(id="1", ws=ws)
    manager.add(c1)
    c2 = Client(id="2", ws=ws)
    manager.add(c2)

    clients = manager.clients()

    assert next(clients) is c1
    assert next(clients) is c2
