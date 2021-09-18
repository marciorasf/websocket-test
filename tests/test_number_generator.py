from server.number_generator import NumberGenerator


def test_numbers():
    generator = NumberGenerator()

    iterations = 0
    for number in generator.number():
        iterations += 1

        assert number == iterations

        if iterations > 10:
            break
