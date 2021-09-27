import asyncio
from datetime import datetime

from server.client_manager import ClientManager
from server.logger import logger
from server.number_generator import NumberGenerator
from server.response import Response


class DeliveryManager:
    def __init__(self, number_generator: NumberGenerator, client_manager: ClientManager):
        self.number_generator = number_generator
        self.client_manager = client_manager

    async def deliver_messages(self) -> None:
        async for number in self.number_generator.numbers():
            response = Response(content=number, timestamp=datetime.now()).to_json()
            logger.debug(f"New message: {response}")

            tasks = [client.send_message(response) for client in self.client_manager.clients()]
            await asyncio.gather(*tasks)
