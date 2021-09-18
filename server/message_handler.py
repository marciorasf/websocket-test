from fastapi import WebSocket

from server.client_manager import Client, ClientManager
from server.message import Message
import server.utils as utils


class MessageHandler:
    def __init__(self, client_manager: ClientManager) -> None:
        self.client_manager = client_manager

    def handle(self, ws: WebSocket, message: Message) -> None:
        if message.action == "subscribe":
            self._subscribe(ws)
        elif message.action == "unsubscribe":
            self._unsubscribe(ws)
        else:
            raise ValueError("Unknown action.")

    def _subscribe(self, ws: WebSocket) -> None:
        self.client_manager.add(Client(ws=ws, id=utils.client_name(ws)))

    def _unsubscribe(self, ws: WebSocket) -> None:
        self.client_manager.remove(utils.client_name(ws))
