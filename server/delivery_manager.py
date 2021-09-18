import asyncio

from server.client_manager import ClientManager
from server.logger import logger
from server.number_generator import NumberGenerator


class DeliveryManager:
    def __init__(self, number_generator: NumberGenerator, client_manager: ClientManager):
        self.number_generator = number_generator
        self.client_manager = client_manager

    async def deliver_numbers(self) -> None:
        async for number in self.number_generator.numbers():
            logger.debug(f"New number: {number}")

            tasks = [client.send_number(number) for client in self.client_manager.clients()]
            await asyncio.gather(*tasks)
