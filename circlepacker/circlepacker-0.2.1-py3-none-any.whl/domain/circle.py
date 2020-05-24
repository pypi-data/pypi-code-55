import math
from typing import List, Dict
from circlepacker.domain.variables import DesignVariable
from circlepacker.domain.model import Model


class Circle(Model):
    def __init__(self, x: DesignVariable, y: DesignVariable, radius: float) -> None:
        self.x = x
        self.y = y
        self.radius = radius

    @property
    def area(self):
        return math.pi * self.radius ** 2

    def get_design_variables(self) -> List[DesignVariable]:
        return [self.x, self.y]

    def set_design_variables(self, new_variable_values: Dict[str, float]) -> None:
        return self._set_design_variables(new_variable_values)
