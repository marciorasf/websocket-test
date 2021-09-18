from dataclasses import dataclass
from typing import Dict, Generator

from fastapi import WebSocket

from server.logger import logger


@dataclass
class Client:
    id: str
    ws: WebSocket

    async def send_number(self, number: int) -> None:
        await self.ws.send_text(str(number))


class ClientManager:
    def __init__(self) -> None:
        self._clients: Dict[str, Client] = dict()

    def add(self, client: Client) -> None:
        self._clients[client.id] = client

    def get(self, id: str) -> Client:
        return self._clients[id]

    def contains(self, id: str) -> bool:
        return id in self._clients

    def remove(self, id: str) -> None:
        if id in self._clients:
            del self._clients[id]
        else:
            logger.warning(f"Tried to remove nonexistent client '{id}'.")

    def clients(self) -> Generator[Client, None, None]:
        return (client for client in self._clients.values())

    def __len__(self):
        return len(self._clients)
