from dataclasses import dataclass
from typing import Set

from fastapi import WebSocket


@dataclass
class Client:
    id: str
    ws: WebSocket

    def __post_init__(self) -> None:
        self._subscribed_streams: Set[str] = set()

    async def send_message(self, message: str) -> None:
        await self.ws.send_text(message)

    def subscribe(self, stream: str) -> None:
        self._subscribed_streams.add(stream)

    def unsubscribe(self, stream: str) -> None:
        if stream in self._subscribed_streams:
            self._subscribed_streams.remove(stream)

    def is_subscribed(self, stream: str) -> bool:
        return stream in self._subscribed_streams

    def has_subscription(self) -> bool:
        return len(self._subscribed_streams) > 0
