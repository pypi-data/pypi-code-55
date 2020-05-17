import numpy as np

class CrossEntropyLoss():
    '''
    Cross Entropy Loss class that takes in real output and predictions which are probabilities and returns the loss.
    '''
    def __call__(self, y, y_pred):
        self.last_y_pred = y_pred
        self.last_y = y
        assert y_pred.shape == y.shape

        n = y.shape[0]
        loss = - np.nansum( y * np.log(y_pred)) / n
        self.last_loss = loss
        return self.last_loss

    def gradient(self):
        y = self.last_y
        y_pred = self.last_y_pred
        n = y.shape[0]
        self.dL_dy = (y_pred - y)/n
        return self.dL_dy

class CE(CrossEntropyLoss):

    def __init__(self):
        pass