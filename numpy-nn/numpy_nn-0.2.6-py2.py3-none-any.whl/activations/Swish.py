import numpy as np
from ..layers import Layer

class Swish(Layer):
    '''
    Learn more about Sigmoid Function here: https://en.wikipedia.org/wiki/Sigmoid_function
    '''

    def forward(self, x):
        self.last_x = x
        self.sigma = 1.0 / (1.0 + np.exp(-x))
        self.result = x * self.sigma
        return self.result

    def __call__(self, x):
        return self.forward(x)

    def backward(self, dL_dy):
        sigma = self.sigma
        x = self.last_x
        self.dy_dx = sigma + x*sigma*(1-sigma)
        return self.dy_dx * dL_dy

class swish(Swish):
    def __init__(self):
        pass