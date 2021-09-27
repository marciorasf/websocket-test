from fastapi import WebSocket

from server import utils
from server.client_manager import Client, ClientManager
from server.logger import logger
from server.request import Request


class RequestHandler:
    def __init__(self, client_manager: ClientManager) -> None:
        self.client_manager = client_manager

    def handle(self, ws: WebSocket, request: Request) -> None:
        if request.action == "subscribe":
            self._subscribe(ws)
        elif request.action == "unsubscribe":
            self._unsubscribe(ws)
        else:
            raise ValueError("Unknown action.")

    def _subscribe(self, ws: WebSocket) -> None:
        logger.debug(f"Subscribing client '{utils.client_name(ws)}'.")

        self.client_manager.add(Client(ws=ws, id=utils.client_name(ws)))

    def _unsubscribe(self, ws: WebSocket) -> None:
        logger.debug(f"Unsubscribing client '{utils.client_name(ws)}'.")

        self.client_manager.remove(utils.client_name(ws))
