import itertools
from collections.abc import Callable
from typing import AsyncGenerator
import asyncio


class NumberGenerator:
    def __init__(
        self, transform_fn: Callable[[int], int] = lambda x: x, interval_in_seconds: float = 0.5
    ) -> None:
        self._transform_fn = transform_fn
        self._interval_in_seconds = interval_in_seconds

    async def numbers(self) -> AsyncGenerator[int, None]:
        for x in itertools.count(start=0):
            yield self._transform_fn(x)
            await asyncio.sleep(self._interval_in_seconds)


def create_default_generator(interval_in_seconds: float = 0.5) -> NumberGenerator:
    return NumberGenerator(lambda x: x, interval_in_seconds)


def create_even_generator(interval_in_seconds: float = 0.5) -> NumberGenerator:
    return NumberGenerator(lambda x: x * 2, interval_in_seconds)


def create_odd_generator(interval_in_seconds: float = 0.5) -> NumberGenerator:
    return NumberGenerator(lambda x: x * 2 + 1, interval_in_seconds)
