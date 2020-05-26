"""
Defines the main Genetic Algorithm Solver class
"""
from itertools import combinations
from math import ceil, floor
from random import choices, random, seed

# pylint: disable=too-many-instance-attributes
class GASolver:
    """
    A simple Genetic Algorithm Solver. It accepts an initial population, and several
    callables to define goal, mutation and crossovers.

    Args:

        initial_pop (list): The elements of the initial population.

        goal (function): A function that accepts one member of the population
            and returns its current value.
        target_value (numeric): The value you're looking for. When the goal(x)
            for any member x of the population is equal to this, the solution
            has been found.

        mutation (function): A callable that accepts one member of the population
            and returns a mutated value of that member.
        prob_mutation (float, 0 <= prob_mutation <= 1)): The probability of a
            mutation occur in any individual. Every time that the `mutation`
            function is invoked, there's `prob_mutation` chance of it actually
            DOING anything.

        crossover_: (function): A callable that takes 2 arguments that are current
            solutions and crosses them over, returning a new one

        selector: (function): A function that receives a dictionary containing
            the current population and their fitness values and returns one
            selected individual. Some of the classic selection functions
            can be found in the `pop_selectors` submodule
        selection_rate (float, 0 <= selection_rate <= 1): the rate of individuals
            in the current population that will be selected to reproduce and
            compose the next. Defaults to 0.5

        max_steps (int, optional): If supplied, the solver will iterate for at
            most `max_steps`. The default is 0, which is the value that disable
            the limit in steps.

        random_seed (int, optional): If provided, the seed of Python's PRNG will
            be set to this. In practice you _only_ want to set this value when
            you need reproducible runs. Useful for testing
    """

    __current_state = []

    # pylint: disable=too-many-arguments, bad-continuation
    def __init__(
        self,
        initial_pop,
        goal,
        target_value,
        mutation,
        prob_mutation,
        crossover_,
        selector,
        selection_rate=0.5,
        max_steps=0,
        random_seed=None,
    ):
        self.population = initial_pop

        self.goal = goal
        self.target_value = target_value

        self.mutation = mutation
        self.prob_mutation = prob_mutation

        self.crossover_ = crossover_

        self.selector = selector
        self.selection_rate = selection_rate

        self.max_steps = max_steps
        self.steps = 0

        self.random_seed = random_seed

    @property
    def current_state(self):
        """
        Current state computes the status of the current
        population by applying the goal function to
        all of its members
        """
        # pylint: disable=fixme
        # TODO: Cache this somehow
        self.__current_state = {indiv: self.goal(indiv) for indiv in self.population}

        return self.__current_state

    @property
    def best_fit(self):
        """
        Returns the individuals with the best fitness value and that value.
        """
        best_value = max(self.current_state.values())
        bests = tuple(
            indiv for indiv in self.population if self.goal(indiv) == best_value
        )
        return (bests, best_value)

    @property
    def solution_found(self):
        """
        Returns True if any member of the current population
        has goal(x) == target_value
        """
        meets_target = [x == self.target_value for x in self.current_state.values()]
        return any(meets_target)

    @property
    def solutions(self):
        """
        Returns the member of the current population where
        goal(individual) == target_value
        """
        solutions = [
            indiv for indiv in self.population if self.goal(indiv) == self.target_value
        ]

        return solutions

    def mutate(self, individual):
        """
        Mutate tries to apply the mutation function, but it actually
        does anything only a few times, determined by `prob_mutation`
        """
        seed(self.random_seed)
        if random() < self.prob_mutation:
            return self.mutation(individual)

        return individual

    def mutate_pop(self):
        """
        Runs the entire population through `mutate`. Note that not _every_ time
        that mutate is called it actually does anything. Check `mutate's` doc
        for details
        """
        self.population = [self.mutate(x) for x in self.population]

    def crossover(self, sol_a, sol_b):
        """
        Calls the crossover function with the parameters
        `sol_a` and `sol_b` and returns the given sibling
        """
        return self.crossover_(sol_a, sol_b)

    def select(self, replace=True):
        """
        Selects a new population using the given selector function. This
        new population will have

            size = ceil(current_population * selection_rate)

        If `replace` is True, the current population
        will be replaced by the new one.
        """
        seed(self.random_seed)

        new_pop_size = ceil(len(self) * self.selection_rate)

        new_pop = [
            self.selector(self.current_state, random_seed=self.random_seed)
            for _ in range(new_pop_size)
        ]

        if replace:
            self.population = new_pop

        return new_pop

    def __iter__(self):
        """
        Implementing the iterable protocol.
        GASolver is an iterable itself!
        """
        return self

    def __next__(self):
        """
        GASolver is an iterable that will execute until a solution is found or,
        optionally, until a max number of steps is reached. That max number
        may be defined in the `max_steps` property.

        A `step` is built as follows:

            1. The current population is selected by the `selector` function.
               This will select a fixed `selection_rate` of the current
               population and *replace* it by the selected members

            2. Random couples are selected to reproduce using the `crossover`
               function. We select as much couples as needed to replace the size
               of the population. That is, if `selection_rate` is 0.3, the previous
               step will have selected 30% of the original population and we need
               as much as 70% of the original to restore the original size.

            3. All the selected couples are crossed over and create new siblings

            4. The selected members of the current population and the siblings
               make the new population

            5. All the population suffers mutation by the `mutate` function
        """
        if self.solution_found or self.max_steps and self.steps >= self.max_steps:
            raise StopIteration

        sibling_len = floor((1 - self.selection_rate) * len(self))

        self.select()
        all_couples = list(combinations(self.population, 2))
        couples = choices(all_couples, k=sibling_len)
        siblings = [self.crossover(c[0], c[1]) for c in couples]
        self.population.extend(siblings)
        self.mutate_pop()

        self.steps += 1

        return self.current_state

    def __len__(self):
        """
        A solvers len() is its population's len()
        """
        return len(self.population)
