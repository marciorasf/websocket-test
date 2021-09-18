from collections.abc import Callable
import itertools


class NumberGenerator:
    def __init__(self, transform_fn: Callable[[int], int] = lambda x: x):
        self._transform_fn = transform_fn

    def numbers(self):
        for x in itertools.count(start=0):
            yield self._transform_fn(x)
