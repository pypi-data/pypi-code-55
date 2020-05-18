# Copyright (c) 2020, TU Wien, Department of Geodesy and Geoinformation
# Distributed under the MIT License (see LICENSE.txt)

"""
Module provides function to convert julian dates into other date formats.
"""


import datetime
import numpy as np

from cadati.np_date import dt2cal
from cadati.check_date import is_leap_year


# leap year
days_past = np.array([0, 31, 60, 91, 121, 152, 182, 213,
                      244, 274, 305, 335, 366])


def julday(month, day, year, hour=0, minute=0, second=0):
    """
    Julian date from month, day, and year.
    Adapted from "Numerical Recipes in C', 2nd edition, pp. 11

    Parameters
    ----------
    month : numpy.ndarray or int32
        Month.
    day : numpy.ndarray or int32
        Day.
    year : numpy.ndarray or int32
        Year.
    hour : numpy.ndarray or int32, optional
        Hour.
    minute : numpy.ndarray or int32, optional
        Minute.
    second : numpy.ndarray or int32, optional
        Second.

    Returns
    -------
    jd : numpy.ndarray or float64
        Julian day.
    """
    month = np.array(month)
    day = np.array(day)

    in_jan_feb = month <= 2
    jy = year - in_jan_feb
    jm = month + 1 + in_jan_feb * 12

    jd = np.int32(np.floor(365.25 * jy) +
                  np.floor(30.6001 * jm) + (day + 1720995.0))
    ja = np.int32(0.01 * jy)
    jd += 2 - ja + np.int32(0.25 * ja)

    jd = jd + hour / 24.0 - 0.5 + minute / 1440.0 + second / 86400.0

    return jd


def caldat(jd):
    """
    Calendar date (month, day, year) from julian date, inverse of 'julday()'
    Return value:  month, day, and year in the Gregorian calendar.

    Adapted from "Numerical Recipes in C', 2nd edition, pp. 11

    Works only for years past 1582!

    Parameters
    ----------
    jd : numpy.ndarray or float64
        Julian day.

    Returns
    -------
    month : numpy.ndarray or int32
        Month.
    day : numpy.ndarray or int32
        Day.
    year : numpy.ndarray or int32
        Year.
    """
    jn = np.int32(((np.array(jd) + 0.000001).round()))

    jalpha = np.int32(((jn - 1867216) - 0.25) / 36524.25)
    ja = jn + 1 + jalpha - (np.int32(0.25 * jalpha))
    jb = ja + 1524
    jc = np.int32(6680.0 + ((jb - 2439870.0) - 122.1) / 365.25)
    jd2 = np.int32(365.0 * jc + (0.25 * jc))
    je = np.int32((jb - jd2) / 30.6001)

    day = jb - jd2 - np.int32(30.6001 * je)
    month = je - 1
    month = (month - 1) % 12 + 1
    year = jc - 4715
    year = year - (month > 2)

    return month, day, year


def julian2datetime(jd, tz=None):
    """
    Converts julian date to python datetime. Default is not time zone aware.

    Parameters
    ----------
    julian : float64
        Julian date.

    Returns
    -------
    dt : datetime
        Datetime object.
    """
    year, month, day, hour, minute, second, microsecond = julian2date(jd)

    if type(jd) == np.array or type(jd) == np.memmap or \
            type(jd) == np.ndarray or type(jd) == np.flatiter:
        return np.array([datetime.datetime(y, m, d, h, mi, s, ms, tz)
                         for y, m, d, h, mi, s, ms in
                         zip(np.atleast_1d(year),
                             np.atleast_1d(month),
                             np.atleast_1d(day),
                             np.atleast_1d(hour),
                             np.atleast_1d(minute),
                             np.atleast_1d(second),
                             np.atleast_1d(microsecond))])

    return datetime.datetime(year, month, day,
                             hour, minute, second, microsecond, tz)


def julian2num(jd):
    """
    Convert a matplotlib date to a Julian days.

    Parameters
    ----------
    jd : numpy.ndarray : int32
        Julian days.
    Returns
    -------
    num : numpy.ndarray : int32
        Number of days since 0001-01-01 00:00:00 UTC *plus* *one*.
    """
    return jd - 1721424.5


def num2julian(num):
    """
    Convert a Julian days to a matplotlib date.

    Parameters
    ----------
    num : numpy.ndarray : int32
        Number of days since 0001-01-01 00:00:00 UTC *plus* *one*.
    Returns
    -------
    jd : numpy.ndarray : int32
        Julian days.
    """
    return num + 1721424.5


def julian2date(jd, return_doy=False, doy_leap_year=True):
    """
    Calendar date from julian date. Works only for years past 1582.

    Parameters
    ----------
    jd : numpy.ndarray
        Julian day.
    return_doy : bool
        Add day of year to output.
    doy_leap_year : bool, optional
        Flag if leap year has to be respected or not (default: True).

    Returns
    -------
    year : numpy.ndarray
        Year.
    month : numpy.ndarray
        Month.
    day : numpy.ndarray
        Day.
    hour : numpy.ndarray
        Hour.
    minute : numpy.ndarray
        Minute.
    second : numpy.ndarray
        Second.
    day_of_year : numpy.ndarray
        Day of year. Only returned when return_doy is set to True.
    """
    min_julian = 2299160
    max_julian = 1827933925

    is_single_value = False
    if type(jd) in (float, int):
        is_single_value = True

    julian = np.atleast_1d(np.array(jd, dtype=float))

    if np.min(julian) < min_julian or np.max(julian) > max_julian:
        raise ValueError("Value of Julian date is out of allowed range.")

    jn = (np.round(julian + 0.0000001)).astype(np.int32)

    jalpha = (((jn - 1867216) - 0.25) / 36524.25).astype(np.int32)
    ja = jn + 1 + jalpha - (np.int32(0.25 * jalpha))
    jb = ja + 1524
    jc = (6680.0 + ((jb - 2439870.0) - 122.1) / 365.25).astype(np.int32)
    jd2 = (365.0 * jc + (0.25 * jc)).astype(np.int32)
    je = ((jb - jd2) / 30.6001).astype(np.int32)

    day = jb - jd2 - np.int64(30.6001 * je)
    month = je - 1
    month = (month - 1) % 12 + 1
    year = jc - 4715
    year = year - (month > 2)

    fraction = (julian + 0.5 - jn).astype(np.float64)
    eps = (np.float64(1e-12) * np.abs(jn)).astype(np.float64)
    eps.clip(min=np.float64(1e-12), max=None)
    hour = (fraction * 24. + eps).astype(np.int64)
    hour.clip(min=0, max=23)
    fraction -= hour / 24.
    minute = (fraction * 1440. + eps).astype(np.int64)
    minute = minute.clip(min=0, max=59)
    second = (fraction - minute / 1440.) * 86400.
    second = second.clip(min=0, max=None)
    microsecond = ((second - np.int32(second)) * 1e6).astype(np.int32)
    microsecond = microsecond.clip(min=0, max=999999)
    second = second.astype(np.int32)
    if is_single_value:
        year, month, day, hour, minute, second, microsecond = (
            year.item(), month.item(), day.item(), hour.item(),
            minute.item(), second.item(), microsecond.item())

    if return_doy:
        day_of_year = days_past[month - 1] + day

        if doy_leap_year:
            nonleap_years = np.invert(is_leap_year(year))
            day_of_year = day_of_year - nonleap_years + np.logical_and(
                day_of_year < 60, nonleap_years)

        if is_single_value:
            day_of_year = day_of_year.item()

        return year, month, day, hour, minute, second, microsecond, day_of_year
    else:
        return year, month, day, hour, minute, second, microsecond


def jd2dt(jd):
    """
    Convert array of julian dates to numpy.datetime64[ms] array.

    Parameters
    ----------
    jd : numpy.float64
        Array of julian dates.

    Returns
    -------
    dt : numpy.datetime64[ms]
        Array of dates in datetime64[ms] format.
    """
    dt = ((((jd - 2440587.5)*24.*3600.*1e6).astype('datetime64[us]')
           + np.timedelta64(500, 'us')).astype('datetime64[ms]'))

    return dt


def jd2cal(jd, doy_respect_nonleap_year=True):
    """
    Convert array of julian dates to a calendar array of year, month, day, hour,
    minute, seconds, millisecond, day of year, with these quantites indexed
    on the last axis.

    Parameters
    ----------
    dt : numpy.ndatetime64
        numpy.ndarray of datetime64[ms] of arbitrary shape
    doy_respect_nonleap_year : bool, optional
        If True (default), leap years vary between 1-366 and non-leap
        years 1-365. If False, doy varies between 1-366 for all years.

    Returns
    -------
    cal_dt : numpy.uint32 (..., 8)
        calendar array with last axis representing year, month, day, hour,
        minute, second, microsecond, day of year.
    """
    return dt2cal(jd2dt(jd), doy_respect_nonleap_year)


def jd2doy(jd, doy_respect_nonleap_year=True):
    """
    Convert julian date to day of year.

    Parameters
    ----------
    jd : numpy.float64
        Array of julian dates.
    doy_respect_nonleap_year : bool, optional
        If True (default), leap years vary between 1-366 and non-leap
        years 1-365. If False, doy varies between 1-366 for all years.

    Returns
    -------
    doy : numpy.int64
        Day of year.
    """
    return jd2cal(jd, doy_respect_nonleap_year)[..., 7]
