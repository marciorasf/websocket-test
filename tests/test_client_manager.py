from starlette.websockets import WebSocket
from server.client_manager import Client, ClientManager
import pytest
from unittest.mock import Mock


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

    assert retrieved_client == client


def test_remove(ws):
    manager = ClientManager()
    manager.add(Client(id="1", ws=ws))
    manager.add(Client(id="2", ws=ws))

    manager.remove("1")

    assert len(manager) == 1


def test_remove_nonexistent(ws):
    manager = ClientManager()

    with pytest.raises(KeyError):
        manager.remove("1")
