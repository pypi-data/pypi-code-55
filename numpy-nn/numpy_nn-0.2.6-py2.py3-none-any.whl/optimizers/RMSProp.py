import numpy as np

class RMSProp():

    def __init__(self, lr = 0.09, beta = 0.85, epsilon=0.0005):
        self.lr= lr
        self.beta = beta
        self.epsilon = epsilon

    def set_parameters(self, params):
        self.parmeters = params
        run_values = {}
        for key in params.keys():
            run_values[key] = 0
        self.run_values = run_values

    def __call__(self, param, dL, param_name):
        value = self.run_values[param_name]
        beta = self.beta
        new_value = beta * value + (1-beta)*(dL**2)
        self.run_values[param_name] = new_value
        return param - self.lr * dL/(np.sqrt(new_value) + self.epsilon)
