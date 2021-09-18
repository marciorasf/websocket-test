from server.number_generator import NumberGenerator, create_even_generator, create_odd_generator


def test_default_numbers() -> None:
    generator = NumberGenerator()

    iterations = 0
    for number in generator.numbers():
        iterations += 1

        assert number == iterations - 1

        if iterations > 10:
            break


def test_even_generator() -> None:
    generator = create_even_generator()

    iterations = 0
    for number in generator.numbers():
        iterations += 1

        assert number == (iterations - 1) * 2

        if iterations > 10:
            break


def test_odd_generator() -> None:
    generator = create_odd_generator()

    iterations = 0
    for number in generator.numbers():
        iterations += 1

        assert number == (iterations - 1) * 2 + 1

        if iterations > 10:
            break
