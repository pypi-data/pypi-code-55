from factpy.plates import IronPlate, CopperPlate
from factpy.bus import BusMaterial
from factpy.material_types import AssembledMaterial


class IronGear(AssembledMaterial):
    """IronGear is intermediate product made from iron plates."""
    crafting_time = 0.5
    ingredients = {IronPlate: 2}
    output = 1

    def __init__(self):
        super().__init__()

    @classmethod
    def a_class_method(cls):
        print("this is a class method")


class CopperWire(AssembledMaterial):
    """CopperWire is intermediate product made from copper plates."""
    crafting_time = 0.5
    ingredients = {CopperPlate: 1}
    output = 2

    def __init__(self):
        super().__init__()


class IronStick(AssembledMaterial):
    """IronStick is intermediate product made from iron plates."""
    crafting_time = 0.5
    ingredients = {IronPlate: 1}
    output = 2

    def __init__(self):
        super().__init__()
