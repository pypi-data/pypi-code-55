from factpy.belts import YellowBelt
from factpy.assembling_machines import AssemblingMachine1
from factpy.furnaces import StoneFurnace
from factpy.natural_resources import Coal


class FactoryCalculator():
    """docstring for FactoryCalculator."""

    def __init__(self, material, number, assembling_machine=AssemblingMachine1,
                 bus_belt=YellowBelt):

        super(FactoryCalculator, self).__init__()
        self.material = material
        self.number = number
        self.assembling_machine = assembling_machine
        self.bus_belt = bus_belt
        self.produced_output = self.produced_output_per_second()

    def produced_output_per_second(self):
        return self.material.units_per_second(self.assembling_machine) * self.number

    def calc_ingredient_factories_and_bus_belts(self):
        factories, bus_belts = self.material.number_of_ingredient_machines(
            self.assembling_machine, self.bus_belt)

        factories = {key: val*self.number for key, val in factories.items()}
        bus_belts = {key: val*self.number for key, val in bus_belts.items()}

        self.print_factorties_and_bus_belts(factories, bus_belts)

    def print_factorties_and_bus_belts(self, factories, bus_belts):
        print('\n-------------')
        print(f'{self.number} {self.material} {self.assembling_machine} produces '
              f'{self.produced_output} units per second')

        for mat, number in factories.items():
            print(f'-- needs {number} of {mat} {self.assembling_machine}')

        for mat, number in bus_belts.items():
            print(f'-- needs {number} {self.bus_belt} of {mat} from the bus')


class SmeltingCalculator(object):
    """docstring for SmeltingCalculator."""

    def __init__(self, material, number_of_belts, furnace=StoneFurnace,
                 belt=YellowBelt, fuel=Coal):

        super(SmeltingCalculator, self).__init__()
        self.material = material
        self.number_of_belts = number_of_belts
        self.furnace = furnace
        self.belt = belt
        self.fuel = fuel

    def calc_furnaces_and_input_belts(self):
        furnaces = self.material.furnaces_per_x_belt(self.number_of_belts,
                                                     self.belt,
                                                     self.furnace)

        # Assumes the same belt as the output belt (self.belt)
        ingredient_belts = self.material.ingredients_output_ratio()
        fuel_belts = self.furnace.x_fuel_belts(self.fuel, self.belt) * furnaces

        self.print_furnaces_and_input_belts(furnaces, ingredient_belts,
                                            fuel_belts)

    def print_furnaces_and_input_belts(self, furnaces, ingredient_belts,
                                       fuel_belts):
        ingredient, ingredient_betls = list(ingredient_belts.items())[0]

        print('\n-------------')
        print(f'{self.number_of_belts} {self.belt} of {self.material}\n'
              f'-- needs {furnaces} {self.furnace}\n'
              f'-- needs {ingredient_betls} {self.belt} of {ingredient}\n'
              f'-- needs {fuel_belts} {self.belt} of {self.fuel}')
