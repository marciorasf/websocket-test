import pytest
from asyncstdlib.builtins import aiter, anext
from server.number_generator import (
    NumberGenerator,
    create_default_generator,
    create_even_generator,
    create_odd_generator,
)


@pytest.mark.asyncio
async def test_default_number_generator() -> None:
    generator = NumberGenerator(interval_in_seconds=0)
    numbers = aiter(generator.numbers())

    assert await anext(numbers) == 0
    assert await anext(numbers) == 1
    assert await anext(numbers) == 2


@pytest.mark.asyncio
async def test_default_generator() -> None:
    generator = create_default_generator(interval_in_seconds=0)
    numbers = aiter(generator.numbers())

    assert await anext(numbers) == 0
    assert await anext(numbers) == 1
    assert await anext(numbers) == 2


@pytest.mark.asyncio
async def test_even_generator() -> None:
    generator = create_even_generator(interval_in_seconds=0)
    numbers = aiter(generator.numbers())

    assert await anext(numbers) == 0
    assert await anext(numbers) == 2
    assert await anext(numbers) == 4


@pytest.mark.asyncio
async def test_odd_generator() -> None:
    generator = create_odd_generator(interval_in_seconds=0)
    numbers = aiter(generator.numbers())

    assert await anext(numbers) == 1
    assert await anext(numbers) == 3
    assert await anext(numbers) == 5
