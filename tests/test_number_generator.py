import pytest
from server.number_generator import NumberGenerator, create_even_generator, create_odd_generator
from asyncstdlib.builtins import anext, aiter


@pytest.mark.asyncio
async def test_default_numbers() -> None:
    generator = NumberGenerator()
    numbers = aiter(generator.numbers())

    assert await anext(numbers) == 0
    assert await anext(numbers) == 1
    assert await anext(numbers) == 2


@pytest.mark.asyncio
async def test_even_generator() -> None:
    generator = create_even_generator()
    numbers = aiter(generator.numbers())

    assert await anext(numbers) == 0
    assert await anext(numbers) == 2
    assert await anext(numbers) == 4


@pytest.mark.asyncio
async def test_odd_generator() -> None:
    generator = create_odd_generator()
    numbers = aiter(generator.numbers())

    assert await anext(numbers) == 1
    assert await anext(numbers) == 3
    assert await anext(numbers) == 5
