"""
gmlp.fitness
============
Generates a fitness.
"""

def calculate_fitness(population, problem):
	"""
	Calculate the fitness based on where you want to be from where you are.

	:param population: Your population which you'll be calculating the population.

	:param problem: Your goal that you want your fitness to be subtracted from to find the correct calculations.
	"""
	population = population
	problem = problem
	fit_scores = []
	for organism in range(len(population)):
		fitness = 0
		for p in range(len(problem)):
			place = population[organism]
			fitness = fitness + abs(problem[p] - place[p])
			# where you want to be subtracted by where you are
		fit_scores.append(fitness)
	return fit_scores