from factpy.material_types import AssembledMaterial


class NuclearFuel(AssembledMaterial):
    """Fuel with the highest energy density."""
    fuel_value = 121e3  # MJ

    def __init__(self):
        super().__init__()
