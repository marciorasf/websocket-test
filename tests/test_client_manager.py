from unittest.mock import Mock

import pytest
from server.client_manager import Client, ClientManager
from starlette.websockets import WebSocket


@pytest.fixture
def ws() -> WebSocket:
    return Mock(spec=WebSocket)


def test_add():
    manager = ClientManager()

    manager.add(Client(id="1", ws=ws))
    manager.add(Client(id="2", ws=ws))

    assert len(manager) == 2


def test_get():
    manager = ClientManager()
    client = Client(id="1", ws=ws)
    manager.add(client)

    retrieved_client = manager.get("1")

    assert retrieved_client is client


def test_remove(ws):
    manager = ClientManager()
    manager.add(Client(id="1", ws=ws))
    manager.add(Client(id="2", ws=ws))

    manager.remove("1")

    assert len(manager) == 1


def test_remove_nonexistent():
    manager = ClientManager()

    with pytest.raises(KeyError):
        manager.remove("1")


def test_clients(ws):
    manager = ClientManager()
    c1 = Client(id="1", ws=ws)
    manager.add(c1)
    c2 = Client(id="2", ws=ws)
    manager.add(c2)

    clients = manager.clients()

    assert next(clients) is c1
    assert next(clients) is c2
