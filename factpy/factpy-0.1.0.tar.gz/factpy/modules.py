from factpy.circuits import GreenCircuit, RedCircuit

from factpy.material_types import AssembledMaterial


class SpeedModule(AssembledMaterial):
    """Increases a machine's speed by 20% and its energy consumption by 50%."""
    crafting_time = 15
    ingredients = {RedCircuit: 5, GreenCircuit: 5}
    output = 1

    def __init__(self):
        super().__init__()
