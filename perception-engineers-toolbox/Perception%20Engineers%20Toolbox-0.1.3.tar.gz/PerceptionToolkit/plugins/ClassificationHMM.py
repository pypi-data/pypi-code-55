from PerceptionToolkit import Version
from PerceptionToolkit.PluginInterfaces import IClassificationPlugin
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.EyeMovements import Fixation
from typing import Sequence, Dict, Any, Union


class ClassificationHMM (IClassificationPlugin):
    @staticmethod
    def version() -> Version:
        return Version(0,0,1)

    def __init__(self):
        ...

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:
        ...

    def fit(self, data: Sequence[DataModel]) -> None:
        ...

    def predict(self, data: DataModel) -> int:
        ...


