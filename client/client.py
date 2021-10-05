import json
from typing import Any, List, Tuple

import websocket


async def simulate_client(url: str, n_messages: int) -> Tuple[List[Any], List[Any]]:
    ws = websocket.WebSocket()
    ws.connect(url)
    ws.send(json.dumps(dict(action="subscribe", stream="odd")))

    odd_responses = []
    for _ in range(n_messages):
        odd_responses.append(ws.recv())
    ws.send(json.dumps(dict(action="unsubscribe", stream="odd")))

    ws.send(json.dumps(dict(action="subscribe", stream="even")))
    even_responses = []
    for _ in range(n_messages):
        even_responses.append(ws.recv())
    ws.send(json.dumps(dict(action="unsubscribe", stream="even")))

    ws.close()

    return odd_responses, even_responses
