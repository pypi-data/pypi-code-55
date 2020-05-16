import numpy as np
from ..layers import Layer

class Sigmoid(Layer):
    '''
    Learn more about Sigmoid Function here: https://en.wikipedia.org/wiki/Sigmoid_function
    '''

    def forward(self, x):
        self.last_x = x
        self.result = 1.0 / (1.0 + np.exp(-x))
        return self.result

    def __call__(self, x):
        return self.forward(x)

    def backward(self, dL_dy):
        self.dy_dx = self.result * (1 - self.result)
        return self.dy_dx * dL_dy

class sigmoid(Layer):
    def __init__(self):
        pass