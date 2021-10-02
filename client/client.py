import json
from typing import Any, List

import websocket


async def simulate_client(url: str, n_messages: int) -> List[Any]:
    ws = websocket.WebSocket()
    ws.connect(url)
    ws.send(json.dumps(dict(action="subscribe", payload="")))

    responses = []
    for _ in range(n_messages):
        responses.append(ws.recv())

    ws.send(json.dumps(dict(action="unsubscribe", payload="")))
    ws.close()

    return responses