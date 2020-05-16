import numpy as np

class SGD():

    def __init__(self, lr = 5e-3):
        self.lr= lr

    def __call__(self, param, dL):
        return param - self.lr * dL