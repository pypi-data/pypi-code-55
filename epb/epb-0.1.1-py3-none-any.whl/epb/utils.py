"""Helpers for energy performance of buildings computation."""

from enum import Enum
from typing import Optional


class Regulator(Enum):
    """The energy performance regulator.

    Exception: energy classes are not used in Flanders.
    """

    BRUSSELS = 1
    FLANDERS = 2
    FRANCE = 3
    WALLONIA = 4


def energy_class(regulator: Regulator, consumption: float) -> Optional[str]:
    """Get the energy class of a building.

    It follows the regulator rules, given its energy consumption.
    If the energy class cannot be calculated, `null` is returned.

    Args:
        regulator (Regulator): The regulator that defines class calculation rules.
        consumption (float): The consumption of the building in kWh/m².year.

    Returns:
        Optional[str]: The energy class. Example: `A++`, `A+`, `A`, `B`...
    """
    if regulator is Regulator.BRUSSELS:
        if consumption <= 0:
            return "A++"
        elif consumption <= 15:
            return "A+"
        elif consumption <= 30:
            return "A"
        elif consumption <= 45:
            return "A-"
        elif consumption <= 62:
            return "B+"
        elif consumption <= 78:
            return "B"
        elif consumption <= 95:
            return "B-"
        elif consumption <= 113:
            return "C+"
        elif consumption <= 132:
            return "C"
        elif consumption <= 150:
            return "C-"
        elif consumption <= 170:
            return "D+"
        elif consumption <= 190:
            return "D"
        elif consumption <= 210:
            return "D-"
        elif consumption <= 232:
            return "E+"
        elif consumption <= 253:
            return "E"
        elif consumption <= 275:
            return "E-"
        elif consumption <= 345:
            return "F"
        elif consumption > 345:
            return "G"

    elif regulator is Regulator.FRANCE:
        if consumption <= 50:
            return "A"
        elif consumption <= 90:
            return "B"
        elif consumption <= 150:
            return "C"
        elif consumption <= 230:
            return "D"
        elif consumption <= 330:
            return "E"
        elif consumption <= 450:
            return "F"
        elif consumption > 450:
            return "G"

    elif regulator is Regulator.WALLONIA:
        if consumption <= 0:
            return "A++"
        elif consumption <= 45:
            return "A+"
        elif consumption <= 85:
            return "A"
        elif consumption <= 170:
            return "B"
        elif consumption <= 255:
            return "C"
        elif consumption <= 340:
            return "D"
        elif consumption <= 425:
            return "E"
        elif consumption <= 510:
            return "F"
        elif consumption > 510:
            return "G"

    return None


def total_consumption(consumption: float, area: float) -> float:
    """Get the total consumption of a building in a year.

    It's function of the energy consumption and total area.

    Args:
        consumption (float): The consumption of the building in kWh/m².year.
        area (float): The total area of the building in m².

    Returns:
        float: The total consumption of a building in a year in kWh/m².
    """
    return consumption * area
