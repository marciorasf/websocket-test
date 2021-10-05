import json
from typing import Any, List

import websocket


async def simulate_client(url: str, n_messages: int) -> List[Any]:
    ws = websocket.WebSocket()
    ws.connect(url)
    ws.send(json.dumps(dict(action="subscribe", stream="odd")))

    responses = []
    for _ in range(n_messages):
        responses.append(ws.recv())

    ws.send(json.dumps(dict(action="unsubscribe", stream="odd")))
    ws.close()

    return responses
