from server.number_generator import NumberGenerator


def test_default_numbers():
    generator = NumberGenerator()

    iterations = 0
    for number in generator.numbers():
        iterations += 1

        assert number == iterations - 1

        if iterations > 10:
            break


def test_numbers_even_function():
    generator = NumberGenerator(lambda x: x * 2)

    iterations = 0
    for number in generator.numbers():
        iterations += 1

        assert number == (iterations - 1) * 2

        if iterations > 10:
            break
