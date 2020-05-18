# Copyright (c) 2020, TU Wien, Department of Geodesy and Geoinformation
# Distributed under the MIT License (see LICENSE.txt)

"""
Module testing the different datetime conversion.
"""

import unittest
import datetime

import numpy as np
import pandas as pd
import numpy.testing as nptest

from cadati.cal_date import cal2jd, cal2dt
from cadati.np_date import dt2cal, dt2jd
from cadati.jd_date import jd2cal, jd2dt, jd2doy
from cadati.jd_date import julian2datetime, julian2date, julday, caldat


class TestDateFunctions(unittest.TestCase):

    def setUp(self):

        years = np.arange(2000, 2012)
        months = np.arange(1, 13)
        days = np.arange(1, 13)
        hours = np.arange(0, 12)
        minutes = np.linspace(0, 55, 12, dtype=int)
        seconds = np.linspace(0, 55, 12, dtype=int)
        mseconds = np.linspace(0, 990, 12, dtype=int)

        self.ref_cal = np.transpose(np.vstack((
            years, months, days, hours, minutes, seconds, mseconds)))

        df = pd.DataFrame({'year': years, 'month': months, 'day': days,
                           'hour': hours, 'minute': minutes,
                           'second': seconds, 'ms': mseconds})
        dates = pd.DataFrame(range(len(df)), index=pd.to_datetime(df))

        self.ref_dt = dates.index.to_numpy()
        self.ref_jd = dates.index.to_julian_date().values
        self.ref_doy = dates.index.dayofyear

    def test_cal2jd(self):
        """
        Test convert calender array to julian dates.
        """
        jd = cal2jd(self.ref_cal)
        np.testing.assert_array_equal(jd, self.ref_jd)

    def test_cal2dt(self):
        """
        Test convert calender array to numpy.datetime64.
        """
        dt = cal2dt(self.ref_cal)
        np.testing.assert_array_equal(dt, self.ref_dt)

    def test_jd2dt(self):
        """
        Test convert julian dates to numpy.datetime64.
        """
        dt = jd2dt(self.ref_jd)
        np.testing.assert_array_equal(dt, self.ref_dt)

    def test_jd2cal(self):
        """
        Test convert julian dates to calender dates.
        """
        cal = jd2cal(self.ref_jd)
        np.testing.assert_array_equal(cal[:, :7], self.ref_cal)
        np.testing.assert_array_equal(cal[:, 7], self.ref_doy)

    def test_dt2jd(self):
        """
        Test convert numpy.datetime64 to julian dates.
        """
        jd = dt2jd(self.ref_dt)
        np.testing.assert_array_equal(jd, self.ref_jd)

    def test_dt2cal(self):
        """
        Test convert numpy.datetime64 to calender array.
        """
        cal = dt2cal(self.ref_dt)
        np.testing.assert_array_equal(cal[:, :7], self.ref_cal)
        np.testing.assert_array_equal(cal[:, 7], self.ref_doy)

    def test_jd2doy(self):
        """
        Test convert julian dates to day of year.
        """
        doy = jd2doy(self.ref_jd)
        np.testing.assert_array_equal(doy, self.ref_doy)


def test_julday():
    """
    Test julday.
    """
    jd = julday(5, 25, 2016, 10, 20, 11)
    jd_should = 2457533.9306828701
    nptest.assert_almost_equal(jd, jd_should)


def test_julday_arrays():
    """
    Test julday.
    """
    jds = julday(np.array([5, 5]),
                 np.array([25, 25]),
                 np.array([2016, 2016]),
                 np.array([10, 10]),
                 np.array([20, 20]),
                 np.array([11, 11]))
    jds_should = np.array([2457533.93068287,
                           2457533.93068287])
    nptest.assert_almost_equal(jds, jds_should)


def test_julday_single_arrays():
    """
    Test julday.
    """
    jds = julday(np.array([5]), np.array([25]), np.array([2016]),
                 np.array([10]), np.array([20]), np.array([11]))

    jds_should = np.array([2457533.93068287])
    nptest.assert_almost_equal(jds, jds_should)


def test_caldat():
    """
    Test caldat.
    """
    month, day, year = caldat(2457533.93068287)

    assert month == 5
    assert day == 25
    assert year == 2016


def test_caldat_array():
    """
    Test caldat.
    """
    month, day, year = caldat(np.array([2457533.93068287, 2457533.93068287]))

    nptest.assert_almost_equal(month, np.array([5, 5]))
    nptest.assert_almost_equal(day, np.array([25, 25]))
    nptest.assert_almost_equal(year, np.array([2016, 2016]))


def test_julian2date():
    """
    Test julian2date.
    """
    year, month, day, hour, minute, second, ms = julian2date(
        2457533.9306828701)

    assert type(year) == int
    assert year == 2016
    assert month == 5
    assert day == 25
    assert hour == 10
    assert minute == 20
    assert second == 10
    assert ms == 999976

    year, month, day, hour, minute, second, ms = julian2date(
        2454515.40972)

    assert year == 2008
    assert month == 2
    assert day == 18
    assert hour == 21
    assert minute == 49
    assert second == 59
    assert ms == 807989


def test_julian2date_single_array():
    """
    Test julian2date single array.
    """
    year, month, day, hour, minute, second, micro = julian2date(
        np.array([2457533.9306828701]))

    assert type(year) == np.ndarray
    assert year == 2016
    assert month == 5
    assert day == 25
    assert hour == 10
    assert minute == 20
    assert second == 10
    assert micro == 999976


def test_julian2date_array():
    """
    Test julian2date.
    """
    year, month, day, hour, minute, second, micro = julian2date(
        np.array([2457533.9306828701, 2457533.9306828701]))

    nptest.assert_almost_equal(year, np.array([2016, 2016]))
    nptest.assert_almost_equal(month, np.array([5, 5]))
    nptest.assert_almost_equal(day, np.array([25, 25]))
    nptest.assert_almost_equal(hour, np.array([10, 10]))
    nptest.assert_almost_equal(minute, np.array([20, 20]))
    nptest.assert_almost_equal(second, np.array([10, 10]))
    nptest.assert_almost_equal(micro, np.array([999976, 999976]))


def test_julian2datetime():
    """
    Test julian2datetime.
    """
    dt = julian2datetime(2457533.9306828701)
    dt_should = datetime.datetime(2016, 5, 25, 10, 20, 10, 999976)
    assert dt == dt_should

    dt = julian2datetime(2457173.8604166666)
    dt_should = datetime.datetime(2015, 5, 31, 8, 39)
    assert dt == dt_should


def test_julian2datetime_single_array():
    """
    Test julian2datetime for single array.
    """
    dt = julian2datetime(np.array([2457533.9306828701]))
    dt_should = np.array([datetime.datetime(2016, 5, 25, 10, 20, 10, 999976)])

    assert type(dt) == np.ndarray
    assert np.all(dt == dt_should)


def test_julian2datetime_array():
    """
    Test julian2datetime array conversion.
    """
    dt = julian2datetime(np.array([2457533.9306828701,
                                   2457533.9306828701]))
    dts = datetime.datetime(2016, 5, 25, 10, 20, 10, 999976)
    dt_should = np.array([dts, dts])

    assert type(dt) == np.ndarray
    assert np.all(dt == dt_should)


if __name__ == '__main__':
    unittest.main()
