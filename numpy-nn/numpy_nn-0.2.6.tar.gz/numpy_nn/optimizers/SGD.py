import numpy as np

class SGD():

    def __init__(self, lr = 5e-3):
        self.lr= lr

    def __call__(self, param, dL, param_name=None):
        return param - self.lr * dL

    def set_parameters(self, params, param_name=None):
        self.parmeters = params