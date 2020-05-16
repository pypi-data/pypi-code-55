from factpy.natural_resources import Coal
from factpy.material_types import AssembledMaterial


class StoneFurnace(AssembledMaterial):
    """StoneFurnace is the most basic smelting machinery."""
    crafting_speed = 1
    energy_consumption = 90e-3  # MW

    def __init__(self):
        super().__init__()

    @classmethod
    def fuel_per_second(cls, fuel):
        # Factorio wiki: Burn time (s) = Fuel value (MJ) ÷ Energy consumption (MW)
        # Fuel per second is inverse of burn time
        return cls.energy_consumption / fuel.fuel_value

    @classmethod
    def x_fuel_belts(cls, fuel, belt):
        return cls.fuel_per_second(fuel) / belt.capacity


class SteelFurnace(AssembledMaterial):
    """SteelFurnace is the second-tier smelting machinery."""
    crafting_speed = 2
    fuel_per_second = {Coal: 0.0225}

    def __init__(self):
        super().__init__()


class ElectricFurnace(AssembledMaterial):
    """ElectricFurnace is the third-tier smelting machinery."""
    crafting_speed = 2

    def __init__(self):
        super().__init__()
