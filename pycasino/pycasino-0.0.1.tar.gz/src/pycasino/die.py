import collections
import random


class Die:
    """Creates a die"""
    def __init__(self, dots: int) -> None:
        assert type(dots) == int
        self.dots = dots

    def throw(self) -> None:
        return random.randint(1, self.dots)

    def roll(self) -> None:
        return self.throw()

    def multi(self, k: int) -> list:
        assert type(k) == int
        return random.choices(range(1, self.dots+1), k=k)


collections.die = Die
