from unittest.mock import Mock

import pytest
from fastapi import WebSocket
from server.client import Client


@pytest.fixture
def ws() -> WebSocket:
    return Mock(spec=WebSocket)


@pytest.fixture
def client(ws: Mock) -> Client:
    return Client("1", ws)


@pytest.mark.asyncio
async def test_send_message(client: Client) -> None:
    await client.send_message("ola")

    assert client.pending_messages() == 1


def test_subscribe(client: Client) -> None:
    client.subscribe("default")

    assert client.is_subscribed("default")
    assert not client.is_subscribed("other")


def test_subscribe_same_stream_twice(client: Client) -> None:
    client.subscribe("default")

    # Should not raise an exception.
    client.subscribe("default")


def test_unsubscribe(client: Client) -> None:
    client.subscribe("default")

    client.unsubscribe("default")

    assert not client.is_subscribed("default")


def test_unsubscribe_nonexistent_stream(client: Client) -> None:
    # Should not raise exception.
    client.unsubscribe("default")


def test_is_subscribed(client: Client) -> None:
    client.subscribe("default")

    assert client.is_subscribed("default")
    assert not client.is_subscribed("other")


def test_has_subscription(client: Client) -> None:
    assert not client.has_subscription()

    client.subscribe("default")
    assert client.has_subscription()
