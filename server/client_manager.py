from typing import Dict, Generator, Optional

from server.client import Client


class ClientManager:
    def __init__(self) -> None:
        self._clients: Dict[str, Client] = {}

    def add(self, client: Client) -> None:
        self._clients[client.id] = client

    def get(self, client_id: str) -> Optional[Client]:
        if client_id in self._clients:
            return self._clients[client_id]

        return None

    def contains(self, client_id: str) -> bool:
        return client_id in self._clients

    def remove(self, client_id: str) -> None:
        if client_id in self._clients:
            del self._clients[client_id]

    def clients(self) -> Generator[Client, None, None]:
        return (client for client in self._clients.values())

    def stream_clients(self, stream: str) -> Generator[Client, None, None]:
        return (client for client in self._clients.values() if client.is_subscribed(stream))

    def __len__(self) -> int:
        return len(self._clients)
