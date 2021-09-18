import pytest
from fastapi import WebSocket
from fastapi.testclient import TestClient
from server.main import app
from server.message import Message


@pytest.mark.timeout(1)
def test_main():
    client = TestClient(app)
    with client.websocket_connect("/") as ws:
        ws: WebSocket

        payload = Message(action="subscribe", payload=None).to_json()
        ws.send_text(payload)

        payload = Message(action="unsubscribe", payload=None).to_json()
        ws.send_text(payload)

        ws.close()
