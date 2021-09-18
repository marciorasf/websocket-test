import logging
from asyncio import Queue
from dataclasses import dataclass
from typing import Dict, Generator

from fastapi import WebSocket

logger = logging.getLogger("server")


@dataclass
class Client:
    id: str
    ws: WebSocket
    queue: Queue = Queue()


class ClientManager:
    def __init__(self) -> None:
        self._clients: Dict[str, Client] = dict()

    def add(self, client: Client) -> None:
        logger.debug(f"Adding client '{client.id}'")

        self._clients[client.id] = client

    def get(self, id: str) -> Client:
        return self._clients[id]

    def remove(self, id: str) -> None:
        logger.debug(f"Removing client '{id}'")

        if id in self._clients:
            del self._clients[id]
        else:
            logger.warning(f"Tried to remove nonexistent client '{id}'.")

    def clients(self) -> Generator[Client, None, None]:
        return (client for client in self._clients.values())

    def __len__(self):
        return len(self._clients)
