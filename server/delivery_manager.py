import asyncio
from asyncio import Queue
from asyncio.tasks import Task
from datetime import datetime
from typing import List

from server.client_manager import ClientManager
from server.number_generator import NumberGenerator
from server.response import Response


class DeliveryManager:
    def __init__(self, generators: List[NumberGenerator], client_manager: ClientManager):
        self.generators = generators
        self.client_manager = client_manager
        self.message_queue: Queue[str] = Queue()

    def deliver_messages(self) -> List[Task[None]]:
        return [
            asyncio.create_task(self._agreggate_messages()),
            asyncio.create_task(self._send_messages()),
        ]

    async def _agreggate_messages(self) -> None:
        async for number in self.generators[0].numbers():
            await self.message_queue.put(
                Response(content=number, timestamp=datetime.now()).to_json()
            )

    async def _send_messages(self) -> None:
        while True:
            if not self.message_queue.empty():
                message = await self.message_queue.get()
                tasks = [client.send_message(message) for client in self.client_manager.clients()]
                await asyncio.gather(*tasks)
            else:
                await asyncio.sleep(0.01)
