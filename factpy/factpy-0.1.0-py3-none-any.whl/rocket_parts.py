from factpy.material_types import AssembledMaterial


class RocketFuel(AssembledMaterial):
    """Fuel which is also used in the production of rockets."""
    fuel_value = 100  # MJ

    def __init__(self):
        super().__init__()
