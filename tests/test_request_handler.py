from unittest.mock import Mock

import pytest
from fastapi import WebSocket
from server.client import Client
from server.client_manager import ClientManager
from server.request import Request
from server.request_handler import RequestHandler


@pytest.fixture
def client_manager() -> Mock:
    return Mock(spec=ClientManager)


@pytest.fixture
def client() -> Client:
    ws = Mock(spec=WebSocket)
    return Client(id="1", ws=ws)


def test_handle_subscribe(client: Client, client_manager: Mock) -> None:
    handler = RequestHandler(client_manager)
    request = Request(action="subscribe", payload=dict())

    handler.handle(client, request)

    client_manager.add.assert_called()


def test_handle_unsubscribe(client: Client, client_manager: Mock) -> None:
    handler = RequestHandler(client_manager)
    request = Request(action="unsubscribe", payload=dict())

    handler.handle(client, request)

    client_manager.remove.assert_called()


def test_handle_unknown_action(client: Client, client_manager: Mock) -> None:
    handler = RequestHandler(client_manager)
    request = Request(action="other", payload=dict())  # type: ignore

    with pytest.raises(ValueError):
        handler.handle(client, request)
