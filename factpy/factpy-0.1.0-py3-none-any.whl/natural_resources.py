from factpy.bus import BusMaterial
from factpy.material_types import MinedMaterial


class IronOre(MinedMaterial):
    """IronOre is a resource found on the map."""

    def __init__(self):
        pass


class Coal(MinedMaterial):
    """Coal is a resource found on the map."""
    fuel_value = 4  # MJ

    def __init__(self):
        pass


class Wood(MinedMaterial):
    """Wood is a resource found on the map."""
    fuel_value = 2  # MJ

    def __init__(self):
        pass


class Stone(BusMaterial, MinedMaterial):
    """Stone is a resource found on the map."""

    def __init__(self):
        pass


class CopperOre(MinedMaterial):
    """CopperOre is a resource found on the map."""

    def __init__(self):
        pass


class UraniumOre(MinedMaterial):
    """UraniumOre is a resource found on the map."""

    def __init__(self):
        pass


class RawFish(MinedMaterial):
    """RawFish is a resource found on the map."""

    def __init__(self):
        pass


class CrudeOil(MinedMaterial):
    """CrudeOil is a resource found on the map."""

    def __init__(self):
        pass


class Water(MinedMaterial):
    """Water is a resource found on the map."""

    def __init__(self):
        pass
