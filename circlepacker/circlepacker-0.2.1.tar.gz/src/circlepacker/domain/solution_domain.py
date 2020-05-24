from typing import List
from circlepacker.domain.model import Model
from circlepacker.domain.variables import DesignVariable
import uuid
from scipy.optimize import Bounds


class SolutionSpace:
    def __init__(self):
        self.models = {}
        self.model_ids = []

    def add_model(self, model: Model) -> None:
        new_id = str(uuid.uuid4().hex)
        self.model_ids.append(new_id)
        self.models[new_id] = model

    def get_values(self) -> List[float]:
        return_values = []
        for model_id in self.model_ids:
            for dv in self.models[model_id].design_variables:
                return_values.extend(dv.val)
        return return_values

    def get_variables(self) -> List[DesignVariable]:
        return [dv for model in self.models.values() for dv in model.design_variables]

    def get_bounds(self) -> List[Bounds]:
        return [variable.bounds for variable in self.get_variables()]
