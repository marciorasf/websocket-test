import asyncio
import dataclasses
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Union

from server.client_manager import ClientManager
from server.logger import logger
from server.number_generator import NumberGenerator


@dataclass
class Message:
    content: Union[int, str]
    timestamp: datetime = datetime.now()

    def __str__(self) -> str:
        return json.dumps(dataclasses.asdict(self))


class DeliveryManager:
    def __init__(self, number_generator: NumberGenerator, client_manager: ClientManager):
        self.number_generator = number_generator
        self.client_manager = client_manager

    async def deliver_messages(self) -> None:
        async for number in self.number_generator.numbers():
            logger.debug(f"New number: {number}")

            message = Message(number)

            tasks = [client.send_message(str(message)) for client in self.client_manager.clients()]
            await asyncio.gather(*tasks)
