import asyncio
import logging
from asyncio.tasks import Task

from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

import server.utils as utils
from server.client_manager import ClientManager
from server.message import Message
from server.message_handler import MessageHandler
from server.number_generator import NumberGenerator, create_even_generator

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
logger = logging.getLogger("server")


class DeliveryManager:
    def __init__(self, number_generator: NumberGenerator, client_manager: ClientManager):
        self.number_generator = number_generator
        self.client_manager = client_manager

    async def start_sending_trades(self):
        async for number in self.number_generator.numbers():
            logger.debug(f"New number: {number}")

            tasks = [client.send_number(str(number)) for client in self.client_manager.clients()]
            await asyncio.gather(*tasks)


class Manager:
    def __init__(self):
        self.number_generator = create_even_generator()
        self.client_manager = ClientManager()
        self.message_handler = MessageHandler(self.client_manager)
        self.delivery_manager = DeliveryManager(self.number_generator, self.client_manager)
        self.delivery_task: Task[None] = None


manager = Manager()

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    manager.delivery_task = asyncio.create_task(manager.delivery_manager.start_sending_trades())


@app.on_event("shutdown")
async def on_shutdown():
    manager.delivery_task.cancel()


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
