"""
gmlp.fitness
============
Generates a fitness.
"""

def calculate_fitness(population, goal):
	"""
	Calculate the fitness based on where you want to be from where you are.

	:param population: Your population which you'll be calculating the population.

	:param goal: Your goal that you want your fitness to be subtracted from to find the correct calculations.
	"""
	fit_scores = []
	for organism in range(len(population)):
		fitness = 0
		place = population[organism]
		for p in range(len(goal)):
			fitness = fitness + abs(goal[p] - place[p])
			# where you want to be subtracted by where you are
		fit_scores.append(fitness)
	return fit_scores

def custom_fitness(population, goal, starting_fit_value, PopulationHasGenes:True, GoalHasGenes:False):
	scores = []
	if PopulationHasGenes == True:
		if GoalHasGenes == False:
			for org in range(len(population)):
				fitness = starting_fit_value
				place = population[org]
				for target in range(len(goal)):
					fitness += abs(goal[target] - place[target])
				scores.append(fitness)
			return scores

	else:
		if GoalHasGenes == True:
			for org in range(len(population)):
				fitness = starting_fit_value
				fitness = starting_fit_value
				fitness += abs(goal[org] - population[org])
				scores.append(fitness)
			return scores