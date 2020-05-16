from factpy.natural_resources import IronOre, CopperOre
from factpy.bus import BusMaterial
from factpy.material_types import SmeltedMaterial


class Plate(BusMaterial, SmeltedMaterial):
    """A general plate"""

    def __init__(self):
        pass


class IronPlate(Plate):
    """IronPlate is a material that can be made by smelting iron ore
     in a furnace.
     """
    crafting_time = 3.2
    ingredients = {IronOre: 1}
    output = 1

    def __init__(self):
        super().__init__()
        pass


class CopperPlate(Plate):
    """CopperPlate is a material that can be made by smelting copper ore
     in a furnace.
     """
    crafting_time = 3.2
    ingredients = {CopperOre: 1}
    output = 1

    def __init__(self):
        super().__init__()
        pass


class SteelPlate(Plate):
    """SteelPlate is a material that can be made by smelting iron plates
     in a furnace.
     """
    crafting_time = 16
    ingredients = {IronPlate: 5}
    output = 1

    def __init__(self):
        super().__init__()
        pass
