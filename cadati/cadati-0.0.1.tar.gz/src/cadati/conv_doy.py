# Copyright (c) 2020, TU Wien, Department of Geodesy and Geoinformation
# Distributed under the MIT License (see LICENSE.txt)

"""
Module provides functions related to day of year conversions.
"""


import numpy as np

from cadati.jd_date import jd2cal
from cadati.np_date import dt2cal
from cadati.check_date import is_leap_year

# leap year
days_past = np.array([0, 31, 60, 91, 121, 152, 182, 213,
                      244, 274, 305, 335, 366])


def doy(month, day, year=None):
    """
    Calculation of day of year. If year is provided it will be tested for
    leap years.

    Parameters
    ----------
    month : numpy.ndarray or int32
        Month.
    day : numpy.ndarray or int32
        Day.
    year : numpy.ndarray or int32, optional
        Year.

    Returns
    -------
    day_of_year : numpy.ndarray or int32
        Day of year.
    """
    day_of_year = days_past[month - 1] + day

    if year is not None:
        nonleap_years = np.invert(is_leap_year(year))
        day_of_year = (day_of_year -
                       nonleap_years.astype('int') +
                       np.logical_and(
                           day_of_year < 60, nonleap_years).astype('int'))

    return day_of_year


def clim_jd2ts(clim, jd):
    """
    Convert climatology array into time series array for given timestamps
    (expressed as julian dates). All years are interpreted as leap
    years (i.e. 1-366).

    Parameters
    ----------
    clim : numpy.ndarray
        Climatology array with 366 entries.
    jd : numpy.float64
        Timestamps in julian dates.

    Returns
    -------
    ts : numpy.ndarray
        Climatology as time series for given time stamps.
    """
    if clim.shape[-1] != 366:
        raise ValueError('Last dimension of clim array is not 366')

    return clim[jd2cal(jd, doy_respect_nonleap_year=False)[..., 7]-1]


def clim_dt2ts(clim, dt):
    """
    Convert climatology array into time series array for given timestamps
    (expressed as julian dates). All years are interpreted as leap
    years (i.e. 1-366).

    Parameters
    ----------
    clim : numpy.ndarray
        Climatology array with 366 entries.
    dt : numpy.datetime64
        Time stamps in numpy.datetime64 dates.

    Returns
    -------
    ts : numpy.ndarray
        Climatology as time series for given time stamps.
    """
    if clim.shape[-1] != 366:
        raise ValueError('Last dimension of clim array is not 366')

    return clim[dt2cal(dt, doy_respect_nonleap_year=False)[..., 7]-1]
