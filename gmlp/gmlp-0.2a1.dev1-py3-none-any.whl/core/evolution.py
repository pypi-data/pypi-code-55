"""
gmlp.evolution
==============
Your base module for starting your genetic programming.
"""

import random
import re
import time

from .fitness import *
from .mutations import *
from .selection import *


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
    Used as an enviroment to help with other evolutionary neural networks,
    such as putting another neural network into this enviroments.
    
    :param network: This will be your neural network that you will be evolution, or some other form of code.

    :param goal: Your goal that your evolutionary neural network will be working towards.

    :param crossover_prob: Your probability for your organisms to crossover.
    """
    def __init__(self, network, goal, crossover_prob, population, mutation_prob):
        self.net = network
        self.crossover_prob = crossover_prob
        self.goal = goal
        self.population
        self.prob = mutation_prob
        
    def start(self, settings, generations, score_func, score_settings, crossover_func=None, selection_func=None, mutation_func=None):
        """
        Start your evolutionary neural network.

        :param settings: These will be how you put your mutation function, your selection function, and your crossover function.

        :param generations: How many generations you want to loop through.

        :param score_func: If score_func is not None, then this will be how you determine your scores.

        :param score_settings: If score_func is None, then you can define the settings of the score in a dictionary.
        \n Here are some keywords:
        \n     1. isList: A True/False statement that will state if your population is a list.
        \n     2. pophasgenes: A True/False statement that will state if your population has genes Ex.(pop = [[1,2,3],[4,5,6],[7,8,9]]).
        \n     3. fitnessValue: Your starting fitness value.
        \n     4. goalhasgenes: A True/False statement that will state if your goal has genes Ex.(goal = [[1,2,3],[4,5,6],[7,8,9]]).
        \n Example of score_settings ->
        \n     score_settings = {"isList":True, "pophasgenes":True, "fitnessValue":0, "goalhasgenes":False}

        :param crossover_func: This will be how you crossover. If it is None then we will choose it for you.``Note that you will have to provide your own
        settings. I can't read your mind.``

        :param selection_func: This will be how you select the fittest population. If it is None then we will choose it for you. ``Note that you will have to provide your own
        settings. I can't read your mind.``

        :param mutation_func: This will be how you mutate your population. If it is None then we will choose it for you. ``Note that you will have to provide your own
        settings. I can't read your mind.``
        """
        self.keywords = ["isList", "pophasgenes", "fitnessValue", "goalhasgenes"]
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
                        self.pophasgenes = True
                    else:
                        self.pophasgenes = False

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
                self.scores = custom_fitness(self.population, self.goal, self.fitness, self.pophasgenes, self.ghg)
                print(self.scores)
                User_Env = Enviroment(self.goal, self.crossover_prob)
                for generation in range(self.generations):
                    self.scores = custom_fitness(self.population, self.goal, self.fitness, self.pophasgenes, self.ghg)
                    self.best = min(self.scores)
                    self.best_score = self.scores[self.scores.index(self.best)]
                    self.output = self.population[self.scores.index(self.best)]
                    print('Gen[%1s], Best Score:%2s, Output -> %3s'%(generation, str(self.best_score), str(self.output)))
                    if mutation_func == None:
                        if crossover_func == None:
                            if selection_func == None:
                                self.population = ValueEncodingMut(User_Env.crossover(User_Env.tournament_selection(self.population, self.scores, 3), self.goal),self.prob)
                    else:
                        self.population = settings
                        
class NeuralNetwork:
    """
    ``THIS FEATURE IS IN DEVELOPMENT!``
    \n Here are some keywords ->
    \n layer(number): Determine the layer function.
    \n Example -> 
    \n NeuralNetwork(
        layer1=func,
        layer2=func2,
        layer3=func3
    )
    """
    def __init__(self, **attrs):
        self.layers = []
        for i in attrs:
            if f"layer{i}" in attrs:
                self.layers.append(attrs[f"layer{i}"])
                print(self.layers)
