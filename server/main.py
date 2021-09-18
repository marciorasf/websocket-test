import logging

from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

import server.utils as utils
from server.client_manager import ClientManager
from server.message import Message
from server.message_handler import MessageHandler
from server.number_generator import create_even_generator

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
logger = logging.getLogger("server")


class Manager:
    def __init__(self):
        self.number_generator = create_even_generator()
        self.client_manager = ClientManager()
        self.message_handler = MessageHandler(self.client_manager)


manager = Manager()

app = FastAPI()


@app.websocket("/")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    client_name = utils.client_name(ws)
    logger.info(f"Client '{client_name}' connected.")

    try:
        while True:
            msg = await ws.receive_json()
            logger.debug(f"Client '{client_name}' sent message: {msg}.")

            manager.message_handler.handle(ws, Message.from_json(msg))
    except WebSocketDisconnect:
        logger.info(f"Client '{client_name}' disconnected.")
