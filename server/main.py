import asyncio
from asyncio.tasks import Task
from typing import Optional, Dict, Any

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
    def __init__(self) -> None:
        self.client_manager = ClientManager()
        self.message_handler = MessageHandler(self.client_manager)
        self.delivery_manager = DeliveryManager(create_even_generator(), self.client_manager)
        self.delivery_task: Optional[Task[None]] = None


manager = Manager()
app = FastAPI()


@app.on_event("startup")
async def on_startup() -> None:
    manager.delivery_task = asyncio.create_task(manager.delivery_manager.deliver_numbers())


@app.on_event("shutdown")
async def on_shutdown() -> None:
    if manager.delivery_task:
        manager.delivery_task.cancel()


@app.websocket("/")
async def websocket_endpoint(ws: WebSocket) -> None:
    await ws.accept()

    client_name = utils.client_name(ws)
    logger.info(f"Client '{client_name}' connected.")

    try:
        while True:
            msg: Dict[str, Any] = await ws.receive_json()
            logger.debug(f"Client '{client_name}' sent message: {msg}.")

            manager.message_handler.handle(ws, Message.from_json(msg))
    except WebSocketDisconnect:
        logger.info(f"Client '{client_name}' disconnected.")

        if manager.client_manager.contains(client_name):
            manager.client_manager.remove(client_name)
