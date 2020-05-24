from circlepacker.domain.variables import DesignVariable
from typing import List, Dict


class Model:
    def __init__(self):
        pass

    @property
    def design_variables(self) -> List[DesignVariable]:
        raise NotImplementedError()

    def _set_design_variables(self, new_variable_values: Dict[str, float]) -> None:
        raise NotImplementedError()

    def set_design_variables(self, new_variable_values: Dict[str, float]) -> None:
        raise NotImplementedError()
