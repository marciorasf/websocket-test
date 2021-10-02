from dataclasses import dataclass

from fastapi import WebSocket


@dataclass
class Client:
    id: str
    ws: WebSocket

    async def send_message(self, message: str) -> None:
        await self.ws.send_text(message)
