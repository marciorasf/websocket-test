from asyncio.queues import Queue
from unittest.mock import Mock
from unittest.test.test_assertions import Test_Assertions

import pytest
from fastapi import WebSocket
from server.client_manager import Client, ClientManager


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


def test_remove_nonexistent_doesnt_raise_exception():
    manager = ClientManager()

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


def test_if_empty_queue_is_created_on_client_instantiation(ws):
    c1 = Client(id="1", ws=ws)

    Test_Assertions().assertIsInstance(c1.queue, Queue)
    assert c1.queue.empty()
