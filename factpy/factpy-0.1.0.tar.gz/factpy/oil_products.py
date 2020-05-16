from factpy.natural_resources import Coal, Water
from factpy.plates import IronPlate
from factpy.bus import BusMaterial


class Petroleum():
    """Petroleum gas is used to create plastic bars and sulfur."""

    def __init__(self):
        pass


class Sulfur(BusMaterial):
    """Sulfur component in the production of Chemical science pack,
     Sulfuric acid and Explosives.
     """
    crafting_time = 1
    ingredients = {Petroleum: 30, Water: 30}
    output = 2

    def __init__(self):
        super().__init__()


class SulfuricAcid():
    """SulfuricAcid is liquid that is used to create batteries and
     processing units.
     """
    crafting_time = 1
    ingredients = {IronPlate: 1, Sulfur: 5, Water: 100}
    output = 50

    def __init__(self):
        pass


class PlasticBar(BusMaterial):
    """PlasticBar are a requirement for the production of red circuits."""
    crafting_time = 1
    ingredients = {Coal: 1, Petroleum: 20}
    output = 2

    def __init__(self):
        super().__init__()


class SolidFuel():
    """Kind of fuel made in a chemical plant."""
    fuel_value = 12  # MJ

    def __init__(self):
        super().__init__()
