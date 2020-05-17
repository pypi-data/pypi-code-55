import numpy as np
from ..layers import Layer

class Softmax(Layer):
    '''
    Implemented based on the following Stakcoverflow solution.
    https://stackoverflow.com/questions/54976533/derivative-of-softmax-function-in-python
    '''
    def forward(self, x):
        self.last_x = x
        shiftx = x - np.max(x)
        exps = np.exp(shiftx)
        result = exps/np.sum(exps)
        self.result = result
        return self.result

    def __call__(self, x):
        return self.forward(x)

    def backward(self, dL_dy):
        x = self.last_x
        self.dy_dx = np.diagflat(x) - np.dot(x, x.T)
        return self.dy_dx * dL_dy

class softmax(Softmax):
    def __init__(self):
        pass
