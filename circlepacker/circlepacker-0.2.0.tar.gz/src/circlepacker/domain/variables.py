import uuid
from typing import Dict
from scipy.optimize import Bounds


class DesignVariable:
    def __init__(
        self, attribute_name: str, bounds: Bounds, initial_condition: float = None
    ):
        self.attribute_name = attribute_name
        self.bounds = bounds
        self.initial_condition = initial_condition
        self.val = initial_condition

    def update(self, val: float) -> None:
        self.val = val
