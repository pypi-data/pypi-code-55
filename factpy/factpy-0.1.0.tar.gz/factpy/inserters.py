from factpy.crafting_components import IronGear
from factpy.circuits import GreenCircuit, RedCircuit
from factpy.plates import IronPlate
from factpy.bus import BusMaterial
from factpy.material_types import AssembledMaterial


class BurnerInserter(AssembledMaterial):
    """BurnerInserter is the most basic fuel based inserter."""
    crafting_time = 0.5
    ingredients = {IronGear: 1, IronPlate: 1}
    output = 1

    def __init__(self):
        super().__init__()


class BasicInserter(AssembledMaterial):
    """BasicInserter is the most basic electric inserter."""
    crafting_time = 0.5
    ingredients = {GreenCircuit: 1, IronGear: 1}
    output = 1

    def __init__(self):
        super().__init__()


class FastInserter(AssembledMaterial):
    """FastInserter is twice as fast as the basic electric inserter."""
    crafting_time = 0.5
    ingredients = {GreenCircuit: 2, BasicInserter: 1, IronPlate: 2}
    output = 1

    def __init__(self):
        super().__init__()


class LongHandedInserter(AssembledMaterial):
    """LongHandedInserter is an electric inserter that picks up and places
     items two tiles from its location.
     """
    crafting_time = 0.5
    ingredients = {BasicInserter: 1, IronGear: 1, IronPlate: 1}
    output = 1

    def __init__(self):
        super().__init__()


class FilterInserter(AssembledMaterial):
    """FilterInserter is a FastInserter with the ability to filter."""
    crafting_time = 0.5
    ingredients = {GreenCircuit: 4, FastInserter: 1}
    output = 1

    def __init__(self):
        super().__init__()


class StackInserter(AssembledMaterial):
    """StackInserter is a FastInserter that can move multiple items at
     the same time."""
    crafting_time = 0.5
    ingredients = {RedCircuit: 1, GreenCircuit: 15, FastInserter: 1,
                   IronGear: 15}
    output = 1

    def __init__(self):
        super().__init__()


class StackFilterInserter(AssembledMaterial):
    """StackFilterInserter combines the characteristics of
     the FilterInserter and the StackInserter."""
    crafting_time = 0.5
    ingredients = {GreenCircuit: 5, StackInserter: 1}
    output = 1

    def __init__(self):
        super().__init__()
