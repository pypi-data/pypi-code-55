"""
gmlp.evolution
==============
Your base module for starting your genetic programming.
"""
import random
from fitness import custom_fitness
class Error(Exception):
	pass

class SettingsError(Error):
	"""Settings Not Defined!"""
	pass

class Enviroment:
	"""
	Used to start your evolutionary neural network.

	:param goal: This is the goal for your evolutionary neural network. If your population is binary your goal should be binary.

	:param crossover_prob: The probability for your organisms to crossover.
	"""
	def __init__(self, goal, crossover_prob):
		self.goal = goal
		self.crossover_prob = crossover_prob

	def generate_population(self, genes=None, pop_size=10000, binary=False):
		"""
		Generates a population.

		:param genes: The genes per organism.

		:param pop_size: Your population size.

		:param binary: This is if you want your population in a binary form if True.
		"""
		self.genes = genes
		self.size = pop_size
		self.binary = binary
		if self.binary == True:
			return [[random.randint(0, 1) for g in range(self.genes)]for n in range(self.size)]
				
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

class Enn:
	"""
	``THIS FEATURE IS IN DEVELOPMENT!``
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
		
	def start(self, generations, population_size=100, score_func=None, 
			  score_settings=None, selection_func=None, selection_settings=None,
			  mutation_func=None, mutation_settings=None):
		"""
		Start your evolutionary neural network.

		:param generations: How many generations you want to loop through.

		:param population_size: How big your popultion is.

		:param score_func: If score_func is not None, then this will be how you determine your scores.

		:param score_settings: If score_func is None, then you can define the settings of the score in a dictionary.
		\n Here are some keywords:
		\n     1. isList: A True/False statement that will state if your population is a list.
		\n     2. PopHasGenes: A True/False statement that will state if your population has genes Ex.(pop = [[1,2,3],[4,5,6],[7,8,9]]).
		\n     3. fitnessValue: Your starting fitness value.
		\n     4. GoalHasGenes: A True/False statement that will state if your goal has genes Ex.(goal = [[1,2,3],[4,5,6],[7,8,9]]).
		\n Example of score_settings ->
		\n     score_settings = {"isList":True, "PopHasGenes":True, "fitnessValue":0, "GoalHasGenes":False}

		:param selection_func: If selection_func is not None, then this will be how you select the fittest population.

		:param selection_settings: If selection_func is None, then you can define the settings of the selection in a dictionary.
		\n Here are some keywords:
		\n     1. tournament_selection: A True/Flase statement to choose if you want tournament selection.
		If you don't know what tournament selection is check this article: https://en.wikipedia.org/wiki/Selection_(genetic_algorithm)
		\n     2. rouletteWheel: A True/Flase statement to choose if you want roulette wheel selection.
		If you don't know what roulette wheel selection is check this article: https://en.wikipedia.org/wiki/Selection_(genetic_algorithm)
		\n Example of selection_settings ->
		\n     sel_settings = {"tournament_selection":True, "rouletteWheel":False}

		:param mutation_func: If mutation_func is not None, then this will be how you mutate your population.

		:param mutation_settings: If mutation_func is None, then you can define the settings of the mutation in a dictionary.
		\n Here are some keywords"
		\n     1. shuffle: A True/Flase statement to choose if you want shuffle mutation.
		\n     2. valueEncoding: A True/Flase statement to choose if you want value encoding mutation.
		"""
		self.keywords = ["isList", "PopHasGenes", "fitnessValue", "GoalHasGenes"]
		# self.population = [[self.net()for gene in range(self.genes)]for n in range(population_size)]
		if score_func != None:
			self.scores = score_func()
			raise SettingsError
		elif score_func == None:
			if score_settings == None:
				print('f')
			else:
				if self.keywords[0] not in score_settings:
					raise ValueError(f"{self.keywords[0]} Not Found In Score Settings!")
				else:
					if score_settings[self.keywords[0]] == True:
						pass
					else:
						self.population = list(self.population)
						
				if self.keywords[1] not in score_settings:
					raise ValueError(f"{self.keywords[1]} Not Found In Score Settings!")
				else:
					if score_settings[self.keywords[1]] == True:
						self.PopHasGenes = True
					else:
						self.PopHasGenes = False

				if self.keywords[2] not in score_settings:
					raise ValueError(f"{self.keywords[2]} Not Found In Score Settings!")
				else:
					self.fitness = score_settings[self.keywords[2]]
				if self.keywords[3] not in score_settings:
					raise ValueError(f"{self.keywords[3]} Not Found In Score Settings!")
				else:
					if score_settings[self.keywords[3]] == True:
						self.ghg = True
					else:
						self.ghg = False
				self.scores = custom_fitness(self.population, self.goal, self.fitness, self.ghg)