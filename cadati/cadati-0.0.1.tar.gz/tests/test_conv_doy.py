# Copyright (c) 2020, TU Wien, Department of Geodesy and Geoinformation
# Distributed under the MIT License (see LICENSE.txt)

"""
Module testing the different datetime conversion.
"""

import unittest
import numpy as np
import pandas as pd

from cadati.conv_doy import clim_jd2ts, clim_dt2ts


class TestClim2TsFunctions(unittest.TestCase):

    def setUp(self):

        self.clim = np.arange(1, 367)
        dates = pd.date_range('2001-01-01', '2011-12-31 23:59:59', freq='1D')
        self.jd = dates.to_julian_date().values
        self.dt = dates.to_numpy()

        nly_clim = np.hstack((np.arange(1, 60), np.arange(61, 367)))
        self.ref_ts = np.hstack((nly_clim, nly_clim, nly_clim, self.clim,
                                 nly_clim, nly_clim, nly_clim, self.clim,
                                 nly_clim, nly_clim, nly_clim))

    def test_clim_jd2ts(self):
        """
        Test conversion of climatology into time series using julian dates.
        """
        ts = clim_jd2ts(self.clim, self.jd)
        np.testing.assert_array_equal(ts, self.ref_ts)

    def test_clim_dt2ts(self):
        """
        Test conversion of climatology into time series using numpy.datetime64.
        """
        ts = clim_dt2ts(self.clim, self.dt)
        np.testing.assert_array_equal(ts, self.ref_ts)


if __name__ == '__main__':
    unittest.main()
