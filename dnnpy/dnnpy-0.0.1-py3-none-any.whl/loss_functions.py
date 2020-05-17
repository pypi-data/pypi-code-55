import numpy as np
from . import LossFunction
from .fun_utils import *


class MSELoss(LossFunction):
    """Implementation of Mean squared error loss"""
    def forward(self, y_hat: np.ndarray, y_true: np.ndarray) -> float:
        """
        Parameters
        ----------
        y_hat : ndarray
            Predicted value
        y_true : ndarray
            True value
        Returns
        -------
        loss : float
            Mean squared error
        """
        mse = 0.5 * np.square(y_true - y_hat).mean()

        self.y_hat = y_hat.copy()
        self.y_true = y_true.copy()

        return mse

    def backward(self) -> np.ndarray:
        """
        Returns
        -------
        grad : ndarray
            The gradient of the output wrt to the loss
        """
        if (self.y_hat is None) or (self.y_true is None):
            raise RuntimeError("You have to call the .forward() function first")

        grad = self.y_hat - self.y_true

        return grad

    def compute_loss(self, y_hat: np.ndarray, y_true: np.ndarray):
        return 0.5 * np.square(y_true - y_hat).mean()


class CrossEntropyLoss(LossFunction):
    """Implementation of Cross-entropy loss"""
    def forward(self, y_hat: np.ndarray, y_true: np.ndarray) -> float:
        """
        Parameters
        ----------
        y_hat : ndarray
            Predicted value
        y_true : ndarray
            True value
        Returns
        -------
        loss : float
            Cross-Entropy Loss
        """
        preds = softmax(y_hat)

        self.y_hat = preds.copy()
        self.y_true = y_true.copy()

        return cross_entropy(preds, y_true)

    def backward(self) -> np.ndarray:
        """
        Returns
        -------
        grad : ndarray
            The gradient of the output wrt to the loss
        """
        if (self.y_hat is None) or (self.y_true is None):
            raise RuntimeError("You have to call the .forward() function first")

        grad = self.y_hat - self.y_true

        return grad

    def compute_loss(self, y_hat: np.ndarray, y_true: np.ndarray):
        preds = softmax(y_hat)
        return cross_entropy(preds, y_true)


class MAELoss(LossFunction):
    """Implementation of Mean Absolute Error loss"""
    def forward(self, y_hat: np.ndarray, y_true: np.ndarray) -> float:
        """
        Parameters
        ----------
        y_hat : ndarray
            Predicted value
        y_true : ndarray
            True value
        Returns
        -------
        loss : float
            Mean absolute error
        """
        mae = np.abs(y_true - y_hat).mean()

        self.y_hat = y_hat.copy()
        self.y_true = y_true.copy()

        return mae

    def backward(self) -> np.ndarray:
        """
        Returns
        -------
        grad : ndarray
            The gradient of the output wrt to the loss
        """
        if (self.y_hat is None) or (self.y_true is None):
            raise RuntimeError("You have to call the .forward() function first")

        grad = 1 * (self.y_hat > self.y_true) - 1 * (self.y_hat < self.y_true)

        return grad

    def compute_loss(self, y_hat: np.ndarray, y_true: np.ndarray):
        return np.abs(y_true - y_hat).mean()


class BinaryCrossEntropyLoss(LossFunction):
    """Implementation of Bonary Cross-entropy loss"""
    def forward(self, y_hat: np.ndarray, y_true: np.ndarray) -> float:
        """
        Parameters
        ----------
        y_hat : ndarray
            Predicted value
        y_true : ndarray
            True value
        Returns
        -------
        loss : float
            Binary cross-entropyLoss
        """
        preds = sigmoid(y_hat)

        self.y_hat = preds.copy()
        self.y_true = y_true.copy()

        return binary_cross_entropy(preds, y_true)

    def backward(self) -> np.ndarray:
        """
        Returns
        -------
        grad : ndarray
            The gradient of the output wrt to the loss
        """
        if (self.y_hat is None) or (self.y_true is None):
            raise RuntimeError("You have to call the .forward() function first")

        grad = self.y_hat - self.y_true

        return grad

    def compute_loss(self, y_hat: np.ndarray, y_true: np.ndarray):
        preds = sigmoid(y_hat)
        return binary_cross_entropy(preds, y_true)


class RMSELoss(LossFunction):
    """Implementation of Root Mean Squared Error Loss"""
    def forward(self, y_hat: np.ndarray, y_true: np.ndarray) -> float:
        """
        Parameters
        ----------
        y_hat : ndarray
            Predicted value
        y_true : ndarray
            True value
        Returns
        -------
        loss : int
            Root mean squared error
        """
        rmse = np.sqrt((y_true - y_hat) ** 2).mean()

        self.y_hat = y_hat.copy()
        self.y_true = y_true.copy()

        return rmse

    def backward(self) -> np.ndarray:
        """
        Returns
        -------
        grad : ndarray
            The gradient of the output wrt to the loss
        """
        if (self.y_hat is None) or (self.y_true is None):
            raise RuntimeError("You have to call the .forward() function first")

        grad = (self.y_hat - self.y_true) / (np.sqrt((self.y_true - self.y_hat) ** 2))

        return grad


class HuberLoss(LossFunction):
    """Implementation of Huber loss"""
    def __init__(self, delta=1):
        self.delta = delta

        super().__init__()

    def forward(self, y_hat: np.ndarray, y_true: np.ndarray) -> float:
        """
        Parameters
        ----------
        y_hat : ndarray
            Predicted value
        y_true : ndarray
            True value
        Returns
        -------
        loss : float
            Huber Loss
        """
        hloss = ((0.5 * (y_true - y_hat) ** 2) * (np.abs(y_true - y_hat) <= self.delta) + (
                self.delta * np.abs(y_true - y_hat) - 0.5 * self.delta ** 2) * (
                         np.abs(y_true - y_hat) >= self.delta)).mean()

        self.y_hat = y_hat.copy()
        self.y_true = y_true.copy()

        return hloss

    def backward(self) -> np.ndarray:
        """
        Returns
        -------
        grad : ndarray
            The gradient of the output wrt to the loss
        """

        if (self.y_hat is None) or (self.y_true is None):
            raise RuntimeError("You have to call the .forward() function first")

        grad = (self.y_true - self.y_hat) * (np.abs(self.y_true - self.y_hat) <= self.delta) + self.delta * (
                1 * (self.y_hat > self.y_true) - 1 * (self.y_hat < self.y_true)) * (
                       np.abs(self.y_true - self.y_hat) >= self.delta)

        return grad
