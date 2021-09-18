from fastapi import WebSocket


def client_name(ws: WebSocket) -> str:
    return f"{ws.client.host}:{ws.client.port}"
