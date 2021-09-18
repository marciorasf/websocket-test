import logging

from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

from server.number_generator import create_even_generator

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("server")


number_generator = create_even_generator()


@app.on_event("startup")
async def on_startup():
    pass


@app.on_event("shutdown")
async def on_shutdown():
    pass


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            await websocket.receive_json()
    except WebSocketDisconnect:
        logger.debug("Closed connection")
