import numpy as np
from ..layers import Layer

class ELU(Layer):
    '''
    '''
    def forward(self, x, alpha=0.01):
        self.alpha = alpha
        self.last_x = x
        self.result = np.where( x > 0, x, alpha*(np.exp(x) - 1)  )
        return self.result

    def __call__(self, x, alpha=0.01):
        return self.forward(x, alpha)

    def backward(self, dL_dy):
        x = self.last_x
        self.dy_dx = np.where(x > 0, 1, self.alpha*np.exp(x))
        return self.dy_dx * dL_dy

class elu(ELU):
    def __init__(self):
        pass
