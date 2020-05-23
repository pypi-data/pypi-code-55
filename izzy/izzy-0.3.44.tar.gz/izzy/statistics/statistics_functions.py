"""
statistics.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

import numpy as np


def histogram():
    """
    https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.histogram.html
    https://numpy.org/doc/1.18/reference/generated/numpy.histogram.html
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_histogram.html

    Returns
    -------

    """

    pass


def pmf(a, bins=10, cumulative=False):
    """
    Probability mass function.

    https://en.wikipedia.org/wiki/Probability_mass_function

    Parameters
    ----------
    a : ArrayLike
    bins : int or ArrayLike
    cumulative : bool

    Returns
    -------

    """

    values, edges = np.histogram(a, bins=bins)
    values /= len(a)
    if cumulative:
        values = np.cumsum(values)
    return values, edges


def pdf(a, bins=10):
    """
    Probability densitry function.

    https://en.wikipedia.org/wiki/Probability_density_function

    Parameters
    ----------
    a : ArrayLike
    bins : int or ArrayLike

    Returns
    -------

    """

    return np.histogram(a, bins=bins, density=True)


_factor = 20. / np.log(2.)
_offset = 600. - np.log(50.) * _factor

def prob2score(p, offset=_offset, factor=_factor):
    """
    Convert a probability to a numeric score grounded in `offset` with a `factor` to indicate how many points impact
    the odds.

    Parameters
    ----------
    p : float or ArrayLike
        Probability
    offset : float
        Offset to apply to score. For instance, we set the offset so a score of 600 corresponds with 1:50 odds.
        (Default: 600 - ln(50)*20/ln(2) = 487.123).
    factor : float
        Factor to indicate how many points impact the odds. For instance, the factor is set so that 20 points double
        the odds. (Default: 20/ln(2) = 28.8539).

    Returns
    -------
    float or np.ndarray
        Score
    """

    if np.min(p) < 0 or np.max(p) > 1.:
        raise AttributeError('probability must be between 0 and 1')

    return offset + np.log(1. / p - 1.) * factor


def score2prob(score, offset=_offset, factor=_factor):
    """
    Convert a probability to a numeric score grounded in `offset` with a `factor` to indicate how many points impact
    the odds.

    Parameters
    ----------
    score : float or ArrayLike
        Score
    offset : float
        Offset to apply to score. For instance, we set the offset so a score of 600 corresponds with 1:50 odds.
        (Default: 600 - ln(50)*20/ln(2) = 487.123).
    factor : float
        Factor to indicate how many points impact the odds. For instance, the factor is set so that 20 points double
        the odds. (Default: 20/ln(2) = 28.8539).

    Returns
    -------
    float or np.ndarray
        Probability
    """

    return 1. / (1. + np.exp((score - offset) / factor))

