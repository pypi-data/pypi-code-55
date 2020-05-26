"""
gmlp.evolution
==============
Your base module for starting your genetic programming.
"""
import random


class Enviroment:
	"""
	Used to start your evolutionary neural network.

	:param goal: This is the goal for your evolutionary neural network. If your population is binary your goal should be binary.

	:param crossover_prob: The probability for your organisms to crossover.
	"""
	def __init__(self, goal, crossover_prob):
		self.goal = goal
		self.crossover_prob = crossover_prob

	def generate_population(self, genes=None, size=10000, binary=False, settings=None):
		"""
		Generates a population.

		:param genes: The genes per organism.

		:param size: Your population size.

		:param binary: This is if you want your population in a binary form if True. If binary=False, then you must describe the ``settings`` param.

		:param settings: This is if binary is False, then your settings will be how you want your population instead of binary.
		"""
		self.genes = genes
		self.size = size
		self.binary = binary
		if self.binary == True:
			return [[random.randint(0, 1) for g in range(genes)]for n in range(size)]
		elif self.binary == False:
			if settings == None:
				raise NameError('Settings Not Defined!')
			else:
				return settings
				
	def tournament_selection(self, population, scores, tournament_size):
		"""
		Selects the fittest.

		:param population: This is your population param to be selected from.

		:param scores: Each of your population's fitness.

		:param tournament_size: How much organisms you want to select for each iteration.
		"""
		self.population = population
		self.scores = scores
		self.tournament_size = tournament_size
		self.fittest = []
		for fit in range(0, len(population)):
			self.random_org = random.randint(0, len(self.scores)-1)
			self.prev_score = self.scores[self.random_org]
			self.prev_pop = self.population[self.random_org]
			for t in range(0, self.tournament_size):
				self.fighters = random.randint(0, len(self.scores)-1)
				if self.scores[self.fighters] < self.prev_score:
					self.prev_score = self.scores[self.fighters]
					self.prev_pop = self.population[self.fighters]
			self.fittest.append(self.prev_pop)
		return self.fittest

	def crossover(self, population, target):
		"""
		The crossover of your population.

		:param population: Your population.

		:param target: Your target.
		"""
		self.pop = population
		self.target = target
		for k in range(int(len(self.pop)-2)):
			if random.random() < self.crossover_prob:
				self.parent1 = self.pop.pop(k)
				self.parent2 = self.pop.pop(k+1)
				self.crossover_point = random.randint(0, len(self.target))
				self.child1 = self.pop.insert(k, self.parent1[0:self.crossover_point]+self.parent2[self.crossover_point:])
				self.child2 = self.pop.insert(k+1, self.parent1[0:self.crossover_point]+self.parent2[self.crossover_point:])
		return self.pop

class Enn(Enviroment):
	"""
	Used as an enviroment to help with other evolutionary neural networks,
	such as putting another neural network into this enviroments.
	
	:param network: This will be your neural network that you will be evolution, or some other form of code.

	:param goal: Your goal that your evolutionary neural network will be working towards.

	:param crossover_prob: Your probability for your organisms to crossover.
	"""
	def __init__(self, network, goal, crossover_prob):
		self.net = network
		self.crossover_prob = crossover_prob
		self.goal = goal
	
