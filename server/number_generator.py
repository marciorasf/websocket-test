class NumberGenerator:
    def __init__(self):
        self._current_value = 0

    def number(self):
        while True:
            self._current_value += 1
            yield self._current_value
