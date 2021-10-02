from fastapi.testclient import TestClient
from server.main import app, context


def test_get_root() -> None:
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200


def test_setup_and_teardown() -> None:
    with TestClient(app):
        assert context.delivery_tasks is not None
        for task in context.delivery_tasks:
            assert not task.done()

    for task in context.delivery_tasks:
        assert task.done()
        assert task.cancelled()
