import pytest
from fastapi.testclient import TestClient
from server.main import app, manager


def test_get_root() -> None:
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200


# TODO Make this test work.
# Currently, it halts.
@pytest.mark.skip
@pytest.mark.asyncio
def test_websocket_endpoint() -> None:
    with TestClient(app) as client:
        with client.websocket_connect("/") as ws:
            ws.send_json('{"action": "subscribe", "payload": ""}')
            ws.receive_json()
            assert True


def test_setup_and_teardown() -> None:
    with TestClient(app):
        assert not manager.delivery_task.done()

    assert manager.delivery_task.done()
    assert manager.delivery_task.cancelled()
