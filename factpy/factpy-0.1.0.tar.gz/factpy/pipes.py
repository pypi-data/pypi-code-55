from factpy.plates import IronPlate
from factpy.material_types import AssembledMaterial


class Pipe(AssembledMaterial):
    """Pipe is the most basic method of distribution of fluids."""
    crafting_time = 0.5
    ingredients = {IronPlate: 1}
    output = 1

    def __init__(self):
        super().__init__()


class PipeToGround(AssembledMaterial):
    """PipeToGround is the undergroud method of distribution of fluids."""
    crafting_time = 0.5
    ingredients = {IronPlate: 5, Pipe: 10}
    output = 2

    def __init__(self):
        super().__init__()
