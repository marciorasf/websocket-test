from fastapi.testclient import TestClient
from server.main import app, manager


def test_get_root() -> None:
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200


def test_setup_and_teardown() -> None:
    with TestClient(app):
        assert manager.delivery_task is not None
        assert not manager.delivery_task.done()

    assert manager.delivery_task.done()
    assert manager.delivery_task.cancelled()
