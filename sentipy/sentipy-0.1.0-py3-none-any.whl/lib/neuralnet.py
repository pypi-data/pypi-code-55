import numpy as np

from sentipy.lib import activations


class Neuron:

    def _get_activation(self, func_name):
        return {
            'tansig': activations.tanh,
            'linear': activations.linear
        }.get(func_name)

    def __init__(self, weights: np.ndarray, bias: float, activation: str):
        self.weights = weights
        self.bias = bias
        self.activation_func = self._get_activation(activation)

    def forward(self, input_arr: np.ndarray) -> np.float:
        """

        :param input_arr:
        :return:
        """
        activation_potential = self.calculate_potential(input_arr)
        return self.activation_func(activation_potential)

    def calculate_potential(self, input_arr):
        return np.dot(input_arr, self.weights) + self.bias