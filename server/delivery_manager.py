import asyncio
import json
import random
from asyncio import Queue
from asyncio.tasks import Task
from datetime import datetime
from typing import Dict, List, Tuple

from server.client_manager import ClientManager
from server.number_generator import NumberGenerator
from server.response import Response


class DeliveryManager:
    def __init__(
        self,
        generators: Dict[str, NumberGenerator],
        client_manager: ClientManager,
        random_delay: bool = False,
    ):
        self._generators = generators
        self._client_manager = client_manager
        self._message_queue: Queue[str] = Queue()
        self._tasks: List[Task[None]] = []
        self._random_delay: bool = random_delay

    def deliver_messages(self) -> None:
        tasks = [
            asyncio.create_task(self._agreggate_messages()),
            asyncio.create_task(self._send_messages()),
        ]
        self._tasks.extend(tasks)

    def stop(self) -> None:
        while len(self._tasks) > 0:
            task = self._tasks.pop()
            task.cancel()

    def running(self) -> bool:
        return len(self._tasks) > 0

    async def _agreggate_messages(self) -> None:
        def _create_task_for_generator(item: Tuple[str, NumberGenerator]) -> Task[None]:
            stream, generator = item
            return asyncio.create_task(self._enqueue_generator_messages(stream, generator))

        tasks = map(
            lambda entry: _create_task_for_generator(entry),
            self._generators.items(),
        )
        self._tasks.extend(tasks)

    async def _enqueue_generator_messages(self, stream: str, generator: NumberGenerator) -> None:
        async for number in generator.numbers():
            if self._random_delay:
                await asyncio.sleep(random.random())

            await self._message_queue.put(
                Response(stream=stream, content=number, timestamp=datetime.now()).to_json()
            )

    async def _send_messages(self) -> None:
        while True:
            if not self._message_queue.empty():
                message = await self._message_queue.get()
                stream = json.loads(message)["stream"]
                tasks = [
                    client.send_message(message)
                    for client in self._client_manager.stream_clients(stream)
                ]
                await asyncio.gather(*tasks)
            else:
                await asyncio.sleep(0.01)
