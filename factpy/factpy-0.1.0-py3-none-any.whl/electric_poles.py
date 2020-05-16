from factpy.crafting_components import CopperWire, CopperPlate, IronStick
from factpy.natural_resources import Wood
from factpy.plates import SteelPlate
from factpy.circuits import RedCircuit
from factpy.material_types import AssembledMaterial


class SmallElectricPole(AssembledMaterial):
    """SmallElectricPole is the basic electric pole."""
    crafting_time = 0.5
    ingredients = {CopperWire: 2, Wood: 1}
    output = 2

    def __init__(self):
        super().__init__()


class MediumElectricPole(AssembledMaterial):
    """MediumElectricPole is an improved electric pole."""
    crafting_time = 0.5
    ingredients = {CopperPlate: 2, IronStick: 4, SteelPlate: 2}
    output = 1

    def __init__(self):
        super().__init__()


class BigElectricPole(AssembledMaterial):
    """BigElectricPole is an improved electric pole."""
    crafting_time = 0.5
    ingredients = {CopperPlate: 5, IronStick: 8, SteelPlate: 5}
    output = 1

    def __init__(self):
        super().__init__()


class Substation(AssembledMaterial):
    """Substation is an advanced electric pole."""
    crafting_time = 0.5
    ingredients = {RedCircuit: 5, CopperPlate: 5, SteelPlate: 10}
    output = 1

    def __init__(self):
        super().__init__()
