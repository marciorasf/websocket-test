from server.client_manager import Client, ClientManager
from server.logger import logger
from server.request import Request


class RequestHandler:
    def __init__(self, client_manager: ClientManager) -> None:
        self._client_manager = client_manager

    def handle(self, client: Client, request: Request) -> None:
        if request.action == "subscribe":
            self._subscribe(client, request.stream)
        elif request.action == "unsubscribe":
            self._unsubscribe(client, request.stream)
        else:
            raise ValueError("Unknown action.")

    def _subscribe(self, client: Client, stream: str) -> None:
        logger.debug(f"Subscribing client '{client.id}'.")

        client.subscribe(stream)
        self._client_manager.add(client)

    def _unsubscribe(self, client: Client, stream: str) -> None:
        logger.debug(f"Unsubscribing client '{client.id}'.")

        client.unsubscribe(stream)
        self._client_manager.remove(client.id)
