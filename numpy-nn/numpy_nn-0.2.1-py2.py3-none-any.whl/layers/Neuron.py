'''
This module defines a layer of fully connected Neurons.
'''
import numpy as np
from .Layer import Layer

class Neuron(Layer):
    '''
    A Basic layer of neurons which fully connects to the next layer.
    '''
    def __init__(self, num_inputs, num_outputs):
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs

        self.weights = np.random.standard_normal((num_inputs, num_outputs))
        self.biases = np.random.standard_normal(num_outputs)

    def forward(self, x):
        self.last_input = x
        self.result = np.dot(x, self.weights) + self.biases
        return self.result

    def __call__(self, x):
        return self.forward(x)

    def backward(self, dL_dy):
        dy_db = np.ones(dL_dy.shape[0]).astype('float32')
        dy_dw = self.last_input.T
        dy_dx = self.weights.T

        self.dL_db = np.dot(dy_db, dL_dy)
        self.dL_dw = np.dot(dy_dw, dL_dy)

        self.dL_dx = np.dot(dL_dy, dy_dx)

        return self.dL_dx

    def optimize(self):
        self.weights = self.optimizer(self.weights, self.dL_dw)
        self.biases = self.optimizer(self.biases, self.dL_db)
