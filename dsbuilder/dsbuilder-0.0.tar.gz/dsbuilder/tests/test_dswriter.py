"""
Tests for DSWriter class
"""

import unittest
from unittest.mock import MagicMock
from dsbuilder.dswriter import DSWriter
from dsbuilder.version import __version__


'''___Authorship___'''
__author__ = "Sam Hunt"
__created__ = "18/5/2020"
__version__ = __version__
__maintainer__ = "Sam Hunt"
__email__ = "sam.hunt@npl.co.uk"
__status__ = "Development"

# todo - write test for csv writer
# todo - write test for end to end writer use


class TestDSWriter(unittest.TestCase):

    def test__write_netcdf(self):

        ds = MagicMock()
        path = "test.nc"

        DSWriter._write_netcdf(ds, path)

        ds.to_netcdf.assert_called_once_with(path, encoding={}, engine='netcdf4', format='netCDF4')


if __name__ == '__main__':
    unittest.main()
