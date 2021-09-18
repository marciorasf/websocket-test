from dataclasses import dataclass
from typing import Dict, Literal, Union

from starlette.websockets import WebSocket

from server.client_manager import Client, ClientManager


@dataclass
class Message:
    action: Union[Literal["subscribe"], Literal["unsubscribe"]]
    payload: Dict


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
        self.client_manager.add(Client(ws=ws, id=self._client_name(ws)))

    def _unsubscribe(self, ws: WebSocket) -> None:
        self.client_manager.remove(self._client_name(ws))

    def _client_name(self, ws: WebSocket) -> str:
        return f"{ws.client.host}:{ws.client.port}"
