import asyncio
from asyncio.tasks import Task

from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

import server.utils as utils
from server.client_manager import ClientManager
from server.delivery_manager import DeliveryManager
from server.logger import logger
from server.message import Message
from server.message_handler import MessageHandler
from server.number_generator import create_even_generator


class Manager:
    def __init__(self):
        self.client_manager = ClientManager()
        self.message_handler = MessageHandler(self.client_manager)
        self.delivery_manager = DeliveryManager(create_even_generator(), self.client_manager)
        self.delivery_task: Task[None] = None


manager = Manager()
app = FastAPI()


@app.on_event("startup")
async def on_startup():
    manager.delivery_task = asyncio.create_task(manager.delivery_manager.deliver_trades())


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

        if manager.client_manager.contains(client_name):
            manager.client_manager.remove(client_name)
