import numpy as np

class Adam():

    def __init__(self, lr = 0.09, beta_1 = 0.85, beta_2 = 0.9, epsilon=0.05):
        self.lr= lr
        self.beta_1 = beta_1
        self.beta_2 = beta_2
        self.epsilon = epsilon
        self.time_step = 1

    def set_parameters(self, params):
        self.parmeters = params
        v_values = {}
        s_values = {}
        for key in params.keys():
            v_values[key] = 0
            s_values[key] = 0
        self.v_values = v_values
        self.s_values = s_values

    def __call__(self, param, dL, param_name):
        v = self.v_values[param_name]
        s = self.s_values[param_name]
        beta1 = self.beta_1
        beta2 = self.beta_2

        new_v = beta1 * v + (1-beta1)*dL
        new_s = beta2 * s + (1-beta2)*(dL**2)

        self.s_values[param_name] = new_s
        self.v_values[param_name] = new_v

        # corrections
        v_fix = new_v/(1-beta1**self.time_step)
        s_fix = new_s/(1-beta2**self.time_step)

        self.time_step += 1

        return param - self.lr * v_fix/(np.sqrt(s_fix) + self.epsilon)
