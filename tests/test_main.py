from fastapi import WebSocket
from server.main import app
from fastapi.testclient import TestClient
import json


def test_main():
    client = TestClient(app)

    with client.websocket_connect("/") as ws:
        ws: WebSocket

        payload = json.dumps({"subscribe": "all"})
        ws.send_json(payload)

        ws.close()

    assert True
