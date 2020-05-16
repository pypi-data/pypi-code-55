import torch


class Accuracy():
    """ Computes the accuracy metric """

    def __init__(self):
        self.name = "acc"

    def __call__(self, y_hat, y):
        return (torch.argmax(y_hat, axis=1) == y).sum().item() / len(y)
