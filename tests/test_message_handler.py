from unittest.mock import Mock

import pytest
from fastapi import WebSocket
from server.client_manager import ClientManager
from server.message import Message
from server.message_handler import MessageHandler


@pytest.fixture
def ws() -> Mock:
    return Mock(spec=WebSocket)


@pytest.fixture
def client_manager() -> Mock:
    return Mock(spec=ClientManager)


def test_handle_subscribe(ws: Mock, client_manager: Mock) -> None:
    handler = MessageHandler(client_manager)
    message = Message(action="subscribe", payload=dict())

    handler.handle(ws, message)

    client_manager.add.assert_called()


def test_handle_unsubscribe(ws: Mock, client_manager: Mock) -> None:
    handler = MessageHandler(client_manager)
    message = Message(action="unsubscribe", payload=dict())

    handler.handle(ws, message)

    client_manager.remove.assert_called()


def test_handle_unknown_action(ws: Mock, client_manager: Mock) -> None:
    handler = MessageHandler(client_manager)
    message = Message(action="other", payload=dict())  # type: ignore

    with pytest.raises(ValueError):
        handler.handle(ws, message)
