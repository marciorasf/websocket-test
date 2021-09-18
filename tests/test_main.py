from fastapi import WebSocket
from fastapi.testclient import TestClient
from server.main import app
from server.message import Message


def test_main():
    with TestClient(app) as client:
        with client.websocket_connect("/") as ws:
            ws: WebSocket

            payload = Message(action="subscribe", payload=None).to_json()
            ws.send_text(payload)

            ws.close()
