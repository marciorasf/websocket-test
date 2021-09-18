import logging

from fastapi import FastAPI, WebSocket
from websockets.exceptions import ConnectionClosedOK

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
        async for number in number_generator.numbers():
            await websocket.send_text(str(number))
    except ConnectionClosedOK:
        logger.debug("Closed connection.")
