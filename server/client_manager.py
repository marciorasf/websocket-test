from dataclasses import dataclass
from typing import Dict, Generator

from fastapi import WebSocket

from server.logger import logger


@dataclass
class Client:
    id: str
    ws: WebSocket

    async def send_message(self, message: str) -> None:
        await self.ws.send_text(message)


class ClientManager:
    def __init__(self) -> None:
        self._clients: Dict[str, Client] = {}

    def add(self, client: Client) -> None:
        self._clients[client.id] = client

    def get(self, client_id: str) -> Client:
        return self._clients[client_id]

    def contains(self, client_id: str) -> bool:
        return client_id in self._clients

    def remove(self, client_id: str) -> None:
        if client_id in self._clients:
            del self._clients[client_id]
        else:
            logger.warning(f"Tried to remove nonexistent client '{client_id}'.")

    def clients(self) -> Generator[Client, None, None]:
        return (client for client in self._clients.values())

    def __len__(self) -> int:
        return len(self._clients)
