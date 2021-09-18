import pytest
from server.number_generator import NumberGenerator, create_even_generator, create_odd_generator


@pytest.mark.asyncio
async def test_default_numbers() -> None:
    generator = NumberGenerator()

    iterations = 0
    async for number in generator.numbers():
        iterations += 1

        assert number == iterations - 1

        if iterations > 3:
            break


@pytest.mark.asyncio
async def test_even_generator() -> None:
    generator = create_even_generator()

    iterations = 0
    async for number in generator.numbers():
        iterations += 1

        assert number == (iterations - 1) * 2

        if iterations > 3:
            break


@pytest.mark.asyncio
async def test_odd_generator() -> None:
    generator = create_odd_generator()

    iterations = 0
    async for number in generator.numbers():
        iterations += 1

        assert number == (iterations - 1) * 2 + 1

        if iterations > 3:
            break
