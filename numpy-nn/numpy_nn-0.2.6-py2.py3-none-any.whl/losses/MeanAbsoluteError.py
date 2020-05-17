import numpy as np


class MeanAbsoluteError():

    def __call__(self, y, y_pred):
        self.last_y_pred = y_pred
        self.last_y = y

        assert y_pred.shape == y.shape
        sums = np.sum(np.abs( y_pred - y ), axis=0)
        n = y.shape[0]
        
        self.last_loss = sums/n        
        return self.last_loss

    def gradient(self):
        self.dL_dy = self.last_y_pred > self.last_y
        self.dL_dy = self.dL_dy.astype(int)
        self.dL_dy[ self.dL_dy == 0 ] = -1 
        return self.dL_dy

class MAE(MeanAbsoluteError):

    def __init__(self):
        pass