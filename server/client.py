from asyncio import Queue
from dataclasses import dataclass
from typing import Set

from fastapi import WebSocket


@dataclass
class Client:
    id: str
    ws: WebSocket
    _queue: Queue[str] = Queue()

    def __post_init__(self) -> None:
        self._subscribed_streams: Set[str] = set()

    async def run(self) -> None:
        while True:
            message = await self._queue.get()
            await self.ws.send_text(message)

    async def send_message(self, message: str) -> None:
        await self._queue.put(message)

    def pending_messages(self) -> int:
        return self._queue.qsize()

    def subscribe(self, stream: str) -> None:
        self._subscribed_streams.add(stream)

    def unsubscribe(self, stream: str) -> None:
        if stream in self._subscribed_streams:
            self._subscribed_streams.remove(stream)

    def is_subscribed(self, stream: str) -> bool:
        return stream in self._subscribed_streams

    def has_subscription(self) -> bool:
        return len(self._subscribed_streams) > 0
