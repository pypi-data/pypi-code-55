# Copyright (c) 2020, TU Wien, Department of Geodesy and Geoinformation
# Distributed under the MIT License (see LICENSE.txt)

"""
Module contains function to convert calendar array [Y,M,D,h,m,s,ms] into
other date formats.
"""


import numpy as np

from cadati.np_date import dt2jd
from cadati.check_date import is_leap_year

# leap year
days_past = np.array([0, 31, 60, 91, 121, 152, 182, 213,
                      244, 274, 305, 335, 366])


def cal2dt(cal_dt):
    """
    Convert a calender array (year, month, day, hour, minute, seconds,
    millisecond) to a numpy.datetime64.

    Parameters
    ----------
    cal_dt : numpy.uint32 (..., 7)
        calendar array with last axis representing year, month, day, hour,
        minute, second, microsecond.

    Returns
    -------
    dt : numpy.datetime64
        numpy datetime64 array.
    """
    nonleap_years = np.invert(is_leap_year(cal_dt[..., 0]))
    md = days_past[cal_dt[..., 1].astype(np.int)-1]

    rel_days = cal_dt[..., 2]*24*3600*1e3 + cal_dt[..., 3]*3600*1e3 \
        + cal_dt[..., 4]*60*1e3 + cal_dt[..., 5] * 1e3 + cal_dt[..., 6]

    fd = (md - nonleap_years + np.logical_and(
        md < 60, nonleap_years)-1)*24*3600*1e3 + rel_days

    years = np.array(cal_dt[..., 0]-1970, dtype='datetime64[Y]')
    dt = years + (np.array(fd, dtype='datetime64[ms]') - np.datetime64('1970'))

    return dt


def cal2jd(cal_dt):
    """
    Convert a calender array (year, month, day, hour, minute, seconds,
    millisecond) to an array of julian dates.

    Parameters
    ----------
    cal_dt : numpy.uint32 (..., 7)
        calendar array with last axis representing year, month, day, hour,
        minute, second, microsecond.

    Returns
    -------
    jd : numpy.float64
        Array of julian dates.
    """
    return dt2jd(cal2dt(cal_dt))
