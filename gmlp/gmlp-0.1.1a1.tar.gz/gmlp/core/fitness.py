"""
gmlp.fitness
============
Generates a fitness.
"""

class Fitness_Function:
    """
    This takes where you want to be from where you are.
    """
    def __init__(self):
        pass

    def calculate_fitness(self, population, problem):
        """
        Calculate the fitness based on where you want to be from where you are.

        :param population: Your population which you'll be calculating the population.

        :param problem: Your goal that you want your fitness to be subtracted from to find the correct calculations.
        """
        self.population = population
        self.problem = problem
        self.fit_scores = []
        for organism in range(len(self.population)):
            self.fitness = 0
            for p in range(len(self.problem)):
                self.place = self.population[organism]
                self.fitness = self.fitness + abs(self.problem[p] - self.place[p])
                # where you want to be subtracted by where you are
            self.fit_scores.append(self.fitness)
        return self.fit_scores