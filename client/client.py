import websocket
import json

ws = websocket.WebSocket()
ws.connect("ws://localhost:8000")
ws.send(json.dumps(dict(action="subscribe", payload="")))

responses = []
for _ in range(5):
    responses.append(ws.recv())

print(responses)

ws.send(json.dumps(dict(action="unsubscribe", payload="")))
ws.close()
