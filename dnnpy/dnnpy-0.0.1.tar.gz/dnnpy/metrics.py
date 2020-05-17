import numpy as np


def accuracy(y, y_hat):
    """
    Parameters
    ----------
    y : ndarray
        True value
    y_hat : ndarray
        Predicted value
    Returns
    -------
    accuracy : float
    """
    s = np.mean([a == b for a in y for b in y_hat])

    return s/len(y)


def mean_squared_error(y, y_hat):
    """
    Parameters
    ----------
    y : ndarray
        True value
    y_hat : ndarray
        Predicted value
    Returns
    -------
    mse : float
    """
    return np.mean(np.power(y - y_hat, 2))


def mean_absolute_error(y, y_hat):
    """
    Parameters
    ----------
    y : ndarray
        True value
    y_hat : ndarray
        Predicted value
    Returns
    -------
    mae : float
    """
    return np.mean(np.abs(y - y_hat))
