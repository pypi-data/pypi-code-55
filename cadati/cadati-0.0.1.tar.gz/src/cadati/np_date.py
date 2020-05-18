# Copyright (c) 2020, TU Wien, Department of Geodesy and Geoinformation
# Distributed under the MIT License (see LICENSE.txt)

"""
Module contains function to convert numpy.datetime64 into other date formats.
"""

import numpy as np

from cadati.check_date import is_leap_year

ref_dt = np.datetime64('1970-01-01')
ref_jd = 2440587.5  # julian date on 1970-01-01 00:00:00


# leap year
days_past = np.array([0, 31, 60, 91, 121, 152, 182, 213,
                      244, 274, 305, 335, 366])


def dt2jd(dt):
    """
    Convert numpy.datetime to julian dates.

    Parameters
    ----------
    dt : numpy.ndatetime64
        numpy.ndarray of datetime64

    Returns
    -------
    jd : numpy.float64
        Array of julian dates.
    """
    return (dt - ref_dt)/np.timedelta64(1, 'D') + ref_jd


def dt2cal(dt, doy_respect_nonleap_year=True):
    """
    Convert array of datetime64 to a calendar array of year, month, day, hour,
    minute, seconds, microsecond and day of year with these quantites indexed
    on the last axis.

    Parameters
    ----------
    dt : numpy.datetime64
        numpy.ndarray of datetime64[ms] of arbitrary shape
    doy_respect_nonleap_year : bool, optional
        If True (default), leap years vary between 1-366 and non-leap
        years 1-365. If False, doy varies between 1-366 for all years.

    Returns
    -------
    cal_dt : numpy.uint32 (..., 8)
        calendar array with last axis representing year, month, day, hour,
        minute, second, millisecond, day of year
    """
    cal_dt = np.empty(dt.shape + (8,), dtype="u4")

    Y, M, D, h, m, s = [dt.astype("M8[{}]".format(x)) for x in "YMDhms"]
    cal_dt[..., 0] = Y + 1970
    cal_dt[..., 1] = (M - Y) + 1
    cal_dt[..., 2] = (D - M) + 1
    cal_dt[..., 3] = (dt - D).astype("m8[h]")
    cal_dt[..., 4] = (dt - h).astype("m8[m]")
    cal_dt[..., 5] = (dt - m).astype("m8[s]")
    cal_dt[..., 6] = (dt - s).astype("m8[ms]")
    cal_dt[..., 7] = days_past[cal_dt[..., 1] - 1] + cal_dt[..., 2]

    if doy_respect_nonleap_year:
        nonleap_years = np.invert(is_leap_year(cal_dt[..., 0]))
        cal_dt[..., 7] = cal_dt[..., 7] - nonleap_years + np.logical_and(
            cal_dt[..., 7] < 60, nonleap_years)

    return cal_dt
