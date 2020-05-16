from factpy.plates import CopperPlate
from factpy.crafting_components import IronGear
from factpy.belts import YellowBelt
from factpy.inserters import BasicInserter
from factpy.material_types import AssembledMaterial


class RedScience(AssembledMaterial):
    """RedScience is first tier of science pack."""
    crafting_time = 5
    ingredients = {CopperPlate: 1, IronGear: 1}
    output = 1

    def __init__(self):
        super().__init__()


class GreenScience(AssembledMaterial):
    """GreenScience is second tier of science pack."""
    crafting_time = 6
    ingredients = {BasicInserter: 1, YellowBelt: 1}
    output = 1

    def __init__(self):
        super().__init__()


class BlackScience(AssembledMaterial):
    """BlackScience is third tier of science pack."""

    def __init__(self):
        super().__init__()


class BlueScience(AssembledMaterial):
    """BlueScience is fourth tier of science pack."""

    def __init__(self):
        super().__init__()


class PurpleScience(AssembledMaterial):
    """PurpleScience is fifth tier of science pack."""

    def __init__(self):
        super().__init__()


class GoldScience(AssembledMaterial):
    """GoldScience is sixth tier of science pack."""

    def __init__(self):
        super().__init__()


class SpaceScience(AssembledMaterial):
    """SpaceScience is last tier of science pack."""

    def __init__(self):
        super().__init__()
