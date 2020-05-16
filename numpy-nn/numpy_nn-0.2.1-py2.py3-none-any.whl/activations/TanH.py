import numpy as np
from ..layers import Layer

class TanH(Layer):
    '''
    '''
    def forward(self, x):
        self.last_x = x
        self.result = (np.exp(x) - np.exp(-x))/(np.exp(x) + np.exp(-x))
        return self.result

    def __call__(self, x):
        return self.forward(x)

    def backward(self, dL_dy):
        self.dy_dx = 1 - self.result**2
        return self.dy_dx * dL_dy

class tanh(TanH):
    def __init__(self):
        pass
