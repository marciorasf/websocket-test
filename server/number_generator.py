import itertools
from collections.abc import Callable
from typing import AsyncGenerator
import asyncio


class NumberGenerator:
    def __init__(self, transform_fn: Callable[[int], int] = lambda x: x) -> None:
        self._transform_fn = transform_fn

    async def numbers(self) -> AsyncGenerator[int, None]:
        for x in itertools.count(start=0):
            yield self._transform_fn(x)
            await asyncio.sleep(0.5)


def create_even_generator() -> NumberGenerator:
    return NumberGenerator(lambda x: x * 2)


def create_odd_generator() -> NumberGenerator:
    return NumberGenerator(lambda x: x * 2 + 1)
