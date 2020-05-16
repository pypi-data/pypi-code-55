from factpy.crafting_components import IronGear
from factpy.plates import IronPlate
from factpy.bus import BusMaterial
from factpy.material_types import AssembledMaterial


class YellowBelt(AssembledMaterial):
    """YellowBelt is the first tier among the three transport belts."""
    capacity = 15
    crafting_time = 0.5
    ingredients = {IronGear: 1, IronPlate: 1}
    output = 2

    def __init__(self):
        super().__init__()


class RedBelt(AssembledMaterial):
    """RedBelt is the second tier among the three transport belts."""
    capacity = 30
    crafting_time = 0.5
    ingredients = {IronGear: 5, YellowBelt: 1}
    output = 1

    def __init__(self):
        super().__init__()


class BlueBelt(AssembledMaterial):
    """BlueBelt is the third tier among the three transport belts."""
    capacity = 45

    def __init__(self):
        super().__init__()
