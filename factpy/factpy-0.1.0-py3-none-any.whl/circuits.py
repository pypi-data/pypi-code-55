from factpy.plates import IronPlate
from factpy.crafting_components import CopperWire
from factpy.oil_products import PlasticBar
from factpy.bus import BusMaterial
from factpy.material_types import AssembledMaterial


class GreenCircuit(BusMaterial, AssembledMaterial):
    """GreenCircuit is the first tier of circuits."""
    crafting_time = 0.5
    ingredients = {CopperWire: 3, IronPlate: 1}
    output = 1

    def __init__(self):
        super().__init__()


class RedCircuit(BusMaterial, AssembledMaterial):
    """RedCircuit is the second tier of circuits."""
    crafting_time = 6
    ingredients = {CopperWire: 4, GreenCircuit: 2, PlasticBar: 2}
    output = 1

    def __init__(self):
        super().__init__()
