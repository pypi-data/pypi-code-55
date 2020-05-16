from factpy.bus import BusMaterial
from collections import Counter
import re


class Meta(type):

    def __repr__(self):
        # split string based on CamelCase
        return re.sub(r'([A-Z])', r' \1', self.__name__).strip()


class AssembledMaterial(metaclass=Meta):
    """docstring forAssembledMaterial."""

    def __init__(self):
        pass

    @classmethod
    def crafing_time_with_assembly_machine(cls, machine):
        return cls.crafting_time / machine.crafting_speed

    @classmethod
    def units_per_second(cls, machine):
        return cls.output / cls.crafing_time_with_assembly_machine(machine)

    @classmethod
    def ingredient_units_needed_per_second(cls, ingredient, machine):
        return cls.units_per_second(machine) * cls.ingredients[ingredient] / cls.output

    @classmethod
    def number_of_ingredient_machines(cls, machine, belt, desired_number=1):
        # Counter can handle floats but certain method will not work e.g. elements()
        factory_cnt = Counter()
        bus_belt_cnt = Counter()

        for ingredient in cls.ingredients.keys():

            needed_ingredients = (cls.ingredient_units_needed_per_second(ingredient, machine)
                                  * desired_number)

            if issubclass(ingredient, BusMaterial):
                bus_belt_cnt[ingredient] = needed_ingredients / belt.capacity
                continue

            number = needed_ingredients / ingredient.units_per_second(machine)

            factory_cnt[ingredient] = number

            # Recursively call the same method on the ingredient
            rec_factory_cnt, rec_bus_belt_cnt = ingredient.number_of_ingredient_machines(
                machine, belt, number)

            # Update couters with recursive counters
            factory_cnt = factory_cnt + rec_factory_cnt
            bus_belt_cnt = bus_belt_cnt + rec_bus_belt_cnt

        return (factory_cnt, bus_belt_cnt)


class SmeltedMaterial(metaclass=Meta):
    """docstring fo SmeltedMaterial"""

    def __init__(self):
        pass

    @classmethod
    def crafing_time_with_furnace(cls, furnace):
        return cls.crafting_time / furnace.crafting_speed

    @classmethod
    def units_per_second(cls, furnace):
        return cls.output / cls.crafing_time_with_furnace(furnace)

    @classmethod
    def furnaces_per_x_belt(cls, x, belt, furnace):
        return x * belt.capacity / cls.units_per_second(furnace)

    @classmethod
    def ingredients_output_ratio(cls):
        # TODO: Rename this method
        return {key: val/cls.output for key, val in cls.ingredients.items()}


class MinedMaterial(metaclass=Meta):
    """docstring fo SmeltedMaterial"""

    def __init__(self):
        pass
