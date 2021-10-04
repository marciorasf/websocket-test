import asyncio
from asyncio import Queue
from asyncio.tasks import Task
from datetime import datetime
from typing import Dict, List

from server.client_manager import ClientManager
from server.number_generator import NumberGenerator
from server.response import Response


class DeliveryManager:
    def __init__(self, generators: Dict[str, NumberGenerator], client_manager: ClientManager):
        self._generators = generators
        self._client_manager = client_manager
        self._message_queue: Queue[str] = Queue()
        self._tasks: List[Task[None]] = []

    def deliver_messages(self) -> None:
        tasks = [
            asyncio.create_task(self._agreggate_messages()),
            asyncio.create_task(self._send_messages()),
        ]
        self._tasks.extend(tasks)

    async def _agreggate_messages(self) -> None:
        tasks = map(
            lambda generator: asyncio.create_task(self._enqueue_generator_messages(generator)),
            self._generators.values(),
        )
        self._tasks.extend(tasks)

    async def _enqueue_generator_messages(self, generator: NumberGenerator) -> None:
        async for number in generator.numbers():
            await self._message_queue.put(
                Response(content=number, timestamp=datetime.now()).to_json()
            )

    async def _send_messages(self) -> None:
        while True:
            if not self._message_queue.empty():
                message = await self._message_queue.get()
                tasks = [client.send_message(message) for client in self._client_manager.clients()]
                await asyncio.gather(*tasks)
            else:
                await asyncio.sleep(0.01)

    def stop(self) -> None:
        while len(self._tasks) > 0:
            task = self._tasks.pop()
            task.cancel()

    def running(self) -> bool:
        return len(self._tasks) > 0
