from typing import Dict
from fastapi import WebSocket
from dataclasses import dataclass


@dataclass
class Client:
    id: str
    ws: WebSocket


class ClientManager:
    def __init__(self) -> None:
        self._clients: Dict[str, Client] = dict()

    def add(self, client: Client) -> None:
        self._clients[client.id] = client

    def get(self, id: str) -> Client:
        return self._clients[id]

    def remove(self, id: str) -> None:
        del self._clients[id]

    def __len__(self):
        return len(self._clients)
