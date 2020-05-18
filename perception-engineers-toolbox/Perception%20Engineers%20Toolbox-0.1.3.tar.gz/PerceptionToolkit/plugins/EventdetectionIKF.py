from PerceptionToolkit.PluginInterfaces import IEventdetectionPlugin
import numpy as np
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.EyeMovementTypes import EyeMovementTypes
from typing import Sequence, Dict, Any
from PerceptionToolkit.EventdetectionHelpers import VelocityCalculatorPixels
from PerceptionToolkit.Version import Version
from pomegranate import HiddenMarkovModel, NormalDistribution, State, GeneralMixtureModel


class EventdetectionIKF(IEventdetectionPlugin):
    """
    """

    def __init__(self):
        super(EventdetectionIKF, self).__init__()
        self.chi2threshold = 10
        self.kalmanFilterParameter1 = 1
        self.kalmanFilterParameter2 = 1

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:
        self.chi2threshold = parameters.get("chi2threshold", self.chi2threshold)
        self.kalmanFilterParameter1 = parameters.get("kalmanFilterParameter1", self.kalmanFilterParameter1)
        self.kalmanFilterParameter1 = parameters.get("kalmanFilterParameter1", self.kalmanFilterParameter1)

    @staticmethod
    def version() -> Version:
        return Version(0, 1, 0)


