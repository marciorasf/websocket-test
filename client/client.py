import json
from typing import Any, List

import websocket


async def simulate_client(n_messages: int) -> List[Any]:
    ws = websocket.WebSocket()
    ws.connect("ws://localhost:8000")
    ws.send(json.dumps(dict(action="subscribe", payload="")))

    responses = []
    for _ in range(n_messages):
        responses.append(ws.recv())

    ws.send(json.dumps(dict(action="unsubscribe", payload="")))
    ws.close()

    return responses
