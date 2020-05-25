"""
Provides different strategies for population selection
"""
from random import seed, random

from .range_dict import RangeDict


def build_roullete(population):
    """
    Returns a RangeDict with keys related to the value's probability of
    being chosen in a Roullete Selection

    Args:
        population (dict): A dictionary whose keys are the individuals in the
            population and the keys are their fitness value

    >>> build_roullete({"a": 10, "b": 10, "c": 20})
    {(0, 0.25): "a", (0.25, 0.5): "b", (0.5, 1): "c"}
    """
    sum_probabilities = sum(population.values())
    averaged_probs = {k: v / sum_probabilities for k, v in population.items()}

    start = 0
    result = RangeDict()

    for value, prob in averaged_probs.items():
        result[(start, start + prob)] = value
        start += prob

    return result


def roullete(population, random_seed=None):
    """
    Uses a classic roullete strategy for selection. Every individual has a
    probability of being selected equal to

    (its goal value)/(the sum of all goal values)

    Args:
        population (dict): A dictionary whose keys are the individuals in the
            population and the keys are their fitness value
        random_seed (int, optional): if supplied, Python PRNG's seed is set to
            it. Use **only** if you need a total reproducible behavior such
            as in testing.

    Returns:
        One selected member
    """
    # This is safe because if the seed is None, Python will use a default behavior
    seed(random_seed)

    # pylint: disable=fixme
    # TODO: Cache this call somehow. LRU, maybe. Difficulty: dicts are non hashable
    population_range = build_roullete(population)

    return population_range[random()]
