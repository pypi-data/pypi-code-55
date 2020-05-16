from factpy.plates import IronPlate
from factpy.furnaces import StoneFurnace
from factpy.crafting_components import IronGear
from factpy.circuits import GreenCircuit
from factpy.pipes import Pipe
from factpy.material_types import AssembledMaterial


class BurnerMiningDrill(AssembledMaterial):
    """BurnerMiningDrill is the first type of drill accessible to the player."""
    crafting_time = 2
    ingredients = {IronGear: 3, IronPlate: 3, StoneFurnace: 1}
    output = 1

    def __init__(self):
        super().__init__()


class ElectricMiningDrill(AssembledMaterial):
    """ElectricMiningDrill is the second type of drill accessible to the player."""
    crafting_time = 2
    ingredients = {GreenCircuit: 3, IronGear: 3, IronPlate: 10}
    output = 1

    def __init__(self):
        super().__init__()


class OffShorePump(AssembledMaterial):
    """OffShorePump produces water from a lake or ocean."""
    crafting_time = 0.5
    ingredients = {GreenCircuit: 2, IronGear: 1, Pipe: 1}
    output = 1

    def __init__(self):
        super().__init__()
