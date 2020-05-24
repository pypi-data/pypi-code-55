from typing import List
from flyplanner.geom import Point, distance


class Fly:
    def __init__(self, fly_positions: List[Point]):
        self.fly_positions = fly_positions

    def take_off_point(self) -> Point:
        return self.fly_positions[0]

    def landing_point(self) -> Point:
        return self.fly_positions[-1]

    def fly_length(self) -> float:
        dist = 0.0
        previous_point = None
        for i, val in enumerate(self.fly_positions):
            if i == 0:
                previous_point = val
            else:
                dist += distance(previous_point, val)
                previous_point = val

        return dist
