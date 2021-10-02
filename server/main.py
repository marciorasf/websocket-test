import asyncio
import json
from asyncio.tasks import Task
from typing import Optional

from fastapi import FastAPI, WebSocket
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect

from server import utils
from server.client import Client
from server.client_manager import ClientManager
from server.delivery_manager import DeliveryManager
from server.logger import logger
from server.number_generator import NumberGenerator
from server.request import Request
from server.request_handler import RequestHandler


class Manager:
    def __init__(self) -> None:
        self.client_manager = ClientManager()
        self.request_handler = RequestHandler(self.client_manager)
        self.delivery_manager = DeliveryManager(NumberGenerator(), self.client_manager)
        self.delivery_task: Optional[Task[None]] = None


manager = Manager()
app = FastAPI()


@app.on_event("startup")
async def on_startup() -> None:
    manager.delivery_task = asyncio.create_task(manager.delivery_manager.deliver_messages())


@app.on_event("shutdown")
async def on_shutdown() -> None:
    if manager.delivery_task:
        manager.delivery_task.cancel()


@app.websocket("/")
async def websocket_endpoint(ws: WebSocket) -> None:
    await ws.accept()

    client = Client(id=utils.client_name(ws), ws=ws)
    logger.info(f"Client '{client.id}' connected.")

    try:
        while True:
            request = await ws.receive_json()
            logger.debug(f"Client '{client.id}' sent message: {request}.")

            manager.request_handler.handle(client.ws, Request.from_json(json.loads(request)))
    except WebSocketDisconnect:
        logger.info(f"Client '{client.id}' disconnected.")

        if manager.client_manager.contains(client.id):
            manager.client_manager.remove(client.id)


@app.get("/")
async def get_root() -> HTMLResponse:
    return HTMLResponse(
        """
        <h1>marciorasf's websocket tests.</h1>
        <br/>
        <h2>Use ws:// instead of https:// for connecting to the webserver.</h2>
        """
    )
