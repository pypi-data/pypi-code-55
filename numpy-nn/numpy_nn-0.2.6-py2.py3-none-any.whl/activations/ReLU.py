import numpy as np
from ..layers import Layer

class ReLU(Layer):
    '''
    '''

    def forward(self, x):
        self.last_x = x
        self.result = np.maximum(0, x)
        return self.result

    def __call__(self, x):
        return self.forward(x)

    def backward(self, dL_dy):
        self.dy_dx = self.last_x
        self.dy_dx[self.dy_dx <= 0 ] = 0
        self.dy_dx[self.dy_dx > 0] = 1
        return self.dy_dx * dL_dy

class relu(ReLU):
    def __init__(self):
        pass