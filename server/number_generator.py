import itertools
from collections.abc import Callable
from typing import Generator


class NumberGenerator:
    def __init__(self, transform_fn: Callable[[int], int] = lambda x: x) -> None:
        self._transform_fn = transform_fn

    def numbers(self) -> Generator[int, None, None]:
        for x in itertools.count(start=0):
            yield self._transform_fn(x)


def create_even_generator() -> NumberGenerator:
    return NumberGenerator(lambda x: x * 2)


def create_odd_generator() -> NumberGenerator:
    return NumberGenerator(lambda x: x * 2 + 1)
