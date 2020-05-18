# Copyright (c) 2020, TU Wien, Department of Geodesy and Geoinformation
# Distributed under the MIT License (see LICENSE.txt)

"""
Module provides function to check dates.
"""


import numpy as np


def is_leap_year(year):
    """
    Check if year is a leap year.

    Parameters
    ----------
    year : numpy.ndarray or int32
        Years.

    Returns
    -------
    leap_year : numpy.ndarray or boolean
        Returns true if year is a leap year.
    """
    return np.logical_or(np.logical_and(year % 4 == 0, year % 100 != 0),
                         year % 400 == 0)
