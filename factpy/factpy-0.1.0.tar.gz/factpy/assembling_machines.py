from factpy.circuits import GreenCircuit
from factpy.plates import IronPlate, SteelPlate
from factpy.crafting_components import IronGear
from factpy.modules import SpeedModule
from factpy.material_types import AssembledMaterial


class AssemblingMachine1(AssembledMaterial):
    """AssemblingMachine1 is the most basic assembling machine."""
    crafting_speed = 0.5
    crafting_time = 0.5
    ingredients = {GreenCircuit: 3, IronGear: 5, IronPlate: 9}
    output = 1

    def __init__(self):
        super().__init__()


class AssemblingMachine2(AssembledMaterial):
    """AssemblingMachine2 is an upgraded version of the assembling machine."""
    crafting_speed = 0.75
    crafting_time = 0.5
    ingredients = {AssemblingMachine1: 1, GreenCircuit: 3, IronGear: 5,
                   SteelPlate: 2}
    output = 1

    def __init__(self):
        super().__init__()


class AssemblingMachine3(AssembledMaterial):
    """AssemblingMachine3 is is the third and final tier of assembling machines."""
    crafting_speed = 1.25
    crafting_time = 0.5
    ingredients = {AssemblingMachine2: 2, SpeedModule: 4}
    output = 1

    def __init__(self):
        super().__init__()
