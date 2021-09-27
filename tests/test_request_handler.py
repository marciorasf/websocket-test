from unittest.mock import Mock

import pytest
from fastapi import WebSocket
from server.client_manager import ClientManager
from server.request import Request
from server.request_handler import RequestHandler


@pytest.fixture
def ws() -> Mock:
    return Mock(spec=WebSocket)


@pytest.fixture
def client_manager() -> Mock:
    return Mock(spec=ClientManager)


def test_handle_subscribe(ws: Mock, client_manager: Mock) -> None:
    handler = RequestHandler(client_manager)
    request = Request(action="subscribe", payload=dict())

    handler.handle(ws, request)

    client_manager.add.assert_called()


def test_handle_unsubscribe(ws: Mock, client_manager: Mock) -> None:
    handler = RequestHandler(client_manager)
    request = Request(action="unsubscribe", payload=dict())

    handler.handle(ws, request)

    client_manager.remove.assert_called()


def test_handle_unknown_action(ws: Mock, client_manager: Mock) -> None:
    handler = RequestHandler(client_manager)
    request = Request(action="other", payload=dict())  # type: ignore

    with pytest.raises(ValueError):
        handler.handle(ws, request)
