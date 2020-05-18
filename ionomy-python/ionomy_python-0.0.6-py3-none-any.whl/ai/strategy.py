import time
import numpy as np

class Deep_Evolution_Strategy:
    inputs = None

    def __init__(
        self,
        weights,
        reward_function,
        population_size,
        sigma,
        learning_rate
    ) -> None:
        self.weights = weights
        self.reward_function = reward_function
        self.population_size = population_size
        self.sigma = sigma
        self.learning_rate = learning_rate

    def _get_weight_from_population(self, weights, population) -> list:
        return [
            weights[index] + self.sigma * p for index, p in enumerate(population)
        ]

    def get_weights(self):
        return self.weights

    def train(self, epoch: int = 100, print_every: int = 1):
        lasttime = time.time()
        for i in range(epoch):
            population = [
                [
                    np.random.randn(*w.shape) for w in self.weights
                ] for _ in range(self.population_size)
            ]
            rewards = np.zeros(self.population_size)
            for k in range(self.population_size):
                weights_population = self._get_weight_from_population(
                    self.weights, population[k]
                )
                rewards[k] = self.reward_function(weights_population)
            rewards = (rewards - np.mean(rewards)) / np.std(rewards)
            for index, w in enumerate(self.weights):
                self.weights[index] = (
                    w + self.learning_rate / (self.population_size * self.sigma)
                    * np.dot(np.array([p[index] for p in population]).T, rewards).T
                )
            if (i + 1) % print_every == 0:
                print(f'iter {i + 1}. reward: {self.reward_function(self.weights)}')
        print('time taken to train:', time.time() - lasttime, 'seconds')