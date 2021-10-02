import asyncio
import json
from datetime import datetime
from multiprocessing import Process

import pytest
import uvicorn
from client.client import simulate_client
from server.main import app


class TestServer:
    async def run(self) -> None:
        self.proc = Process(
            target=uvicorn.run,
            args=(app,),
            kwargs={"host": "127.0.0.1", "port": 5000, "log_level": "info"},
            daemon=True,
        )

        self.proc.start()
        # Time to start server.
        await asyncio.sleep(0.1)

    def stop(self) -> None:
        self.proc.terminate()


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.freeze_time("2021-02-10 10:00:00", tick=True)
async def test_main() -> None:
    server = TestServer()
    await server.run()

    responses = await simulate_client("ws://localhost:5000", 2)

    for response in responses:
        parsed = json.loads(response)

        assert isinstance(parsed["content"], int)
        assert isinstance(parsed["timestamp"], str)

        # Test if can be converted to datetime.
        datetime.fromisoformat(parsed["timestamp"])

    server.stop()
