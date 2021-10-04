from fastapi import FastAPI, WebSocket
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect

from server import utils
from server.client import Client
from server.client_manager import ClientManager
from server.delivery_manager import DeliveryManager
from server.logger import logger
from server.number_generator import (
    create_default_generator,
    create_even_generator,
    create_odd_generator,
)
from server.request import Request
from server.request_handler import RequestHandler
from server.settings import Settings


class AppContext:
    def __init__(self) -> None:
        self.settings = Settings()
        self.client_manager = ClientManager()
        self.request_handler = RequestHandler(self.client_manager)
        self.delivery_manager = DeliveryManager(
            generators={
                "default": create_default_generator(self.settings.generator_interval_in_seconds),
                "even": create_even_generator(self.settings.generator_interval_in_seconds),
                "odd": create_odd_generator(self.settings.generator_interval_in_seconds),
            },
            client_manager=self.client_manager,
        )


context = AppContext()
app = FastAPI()


@app.on_event("startup")
async def on_startup() -> None:
    context.delivery_manager.deliver_messages()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    context.delivery_manager.stop()


@app.websocket("/")
async def websocket_endpoint(ws: WebSocket) -> None:
    await ws.accept()

    client = Client(id=utils.client_name(ws), ws=ws)
    logger.info(f"Client '{client.id}' connected.")

    try:
        while True:
            request = await ws.receive_json()
            context.request_handler.handle(client, Request.from_json(request))
    except WebSocketDisconnect:
        logger.info(f"Client '{client.id}' disconnected.")

        if context.client_manager.contains(client.id):
            context.client_manager.remove(client.id)


@app.get("/")
async def get_root() -> HTMLResponse:
    return HTMLResponse(
        """
        <h1>marciorasf's websocket tests.</h1>
        <br/>
        <h2>Use ws:// instead of https:// for connecting to the webserver.</h2>
        """
    )
