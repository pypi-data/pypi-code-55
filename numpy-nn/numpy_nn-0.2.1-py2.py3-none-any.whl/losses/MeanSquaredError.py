import numpy as np


class MeanSquaredError():

    def __call__(self, y, y_pred):
        self.last_y_pred = y_pred
        self.last_y = y

        assert y_pred.shape == y.shape
        self.last_loss = np.sum(np.square(y-y_pred), axis=0)/y_pred.shape[0]
        return self.last_loss

    def gradient(self):
        self.dL_dy = -2*(self.last_y - self.last_y_pred)/self.last_y.shape[0]
        return self.dL_dy

class MSE(MeanSquaredError):
    def __init__(self):
        pass