"""
gmlp.mutations
==============
Used for mutating your population. ``More mutations are to come in future versions.``
"""
import random


def value_encoding_mutation(population, mutation_prob):
    """
    Value Encoding Mutation.

    :param population: the population you will be mutating

    :param mutation_prob: the mutation probability usually .15 but you'll have to see what's best for you.
    """
    for pop in range(len(population)):
        if random.random() < mutation_prob:
            random_population_org = random.randint(0, len(population)-1)
            popped_org = population.pop(random_population_org)
            for c in range(len(popped_org)):
                if random.random() < .5:
                    popped_org[c] += 1
                else:
                    popped_org[c] -= 1
            population.insert(random_population_org, popped_org)
    return population
