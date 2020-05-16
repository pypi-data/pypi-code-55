from factpy.calculators import FactoryCalculator, SmeltingCalculator
from factpy.assembling_machines import AssemblingMachine1
from factpy.sciences import GreenScience
from factpy.belts import YellowBelt, RedBelt

from factpy.furnaces import StoneFurnace, SteelFurnace
from factpy.plates import IronPlate, CopperPlate, SteelPlate
from factpy.inserters import BurnerInserter, FastInserter
from factpy.crafting_components import IronGear
from factpy.circuits import GreenCircuit
from factpy.natural_resources import Coal


def run():
    wanted_material = GreenScience
    wanted_number_of_factories = 4
    assembling_machine = AssemblingMachine1
    bus_belt = YellowBelt

    calc = FactoryCalculator(wanted_material, wanted_number_of_factories,
                             assembling_machine, bus_belt)
    calc.calc_ingredient_factories_and_bus_belts()

    wanted_material = IronPlate
    wanted_number_of_belt = 2
    belt = YellowBelt
    furnace = StoneFurnace
    fuel = Coal

    calc2 = SmeltingCalculator(wanted_material, wanted_number_of_belt,
                               furnace, belt, fuel)
    calc2.calc_furnaces_and_input_belts()


if __name__ == '__main__':
    run()
