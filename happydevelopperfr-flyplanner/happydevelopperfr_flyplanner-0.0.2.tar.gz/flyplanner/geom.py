import math


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


def distance(a: Point, b: Point):
    return math.sqrt(math.pow(b.x - a.x, 2) + math.pow(b.y - a.y, 2))
