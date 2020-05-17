import numpy as np

class Momentum():

    def __init__(self, lr = 5e-3, beta = 0.9):
        self.lr= lr
        self.beta = beta

    def set_parameters(self, params):
        self.parmeters = params
        run_values = {}
        for key in params.keys():
            run_values[key] = 0
        self.run_values = run_values

    def __call__(self, param, dL, param_name):
        value = self.run_values[param_name]
        beta = self.beta
        new_value = beta * value + (1-beta)*dL
        self.run_values[param_name] = new_value
        return param - self.lr * new_value