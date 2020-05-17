import numpy as np


def softmax(s):
    """
    Implementation of the softmax function

    Parameters
    ----------
    s : ndarray

    Returns
    -------
    a : ndarray
    """
    s -= np.max(s)  # For numerical stability

    return np.exp(s) / np.sum(np.exp(s))


def cross_entropy(preds, targets) -> float:
    """
    Compute the cross-entropy

    Parameters
    ----------
    preds : ndarray
        Predicted value
    targets : ndarray
        True value

    Returns
    -------
    CE : float
    """
    preds = np.clip(preds, a_min=1e-7, a_max=None)  # prevent log(0)
    return -np.sum(targets * np.log(preds), axis=0)


def sigmoid(s):
    """
    Parameters
    ----------
    s : ndarray

    Returns
    -------
    a : ndarray
    The sigmoid of the input
    """
    return 1 / (1 + np.exp(-s))


def binary_cross_entropy(preds, targets) -> float:
    """
    Compute the cross-entropy

    Parameters
    ----------
    preds : ndarray
        Predicted value
    targets : ndarray
        True value

    Returns
    -------
    bce : float
    """
    preds = np.clip(preds, a_min=1e-7, a_max=None)  # prevent log(0)
    return -np.sum(targets * np.log(preds) + (1 - targets) * np.log(1 - preds))
