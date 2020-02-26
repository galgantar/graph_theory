from itertools import count
from random import randint


class Color:
    NONE = None
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)

    available_colors = [RED, GREEN, BLUE, YELLOW]

    @staticmethod
    def infinite_generator():
        for i in count():
            yield Color.available_colors[i] if i < len(Color.available_colors) else Color.generate_random_color()

    @staticmethod
    def finite_generator(limit):
        for i in range(limit):
            yield Color.available_colors[i] if i < len(Color.available_colors) else Color.generate_random_color()

    @staticmethod
    def generate_random_color():
        return randint(30, 255), randint(30, 255), randint(30, 255)