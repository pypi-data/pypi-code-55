#!/usr/bin/env python

"""
Time Series.
"""

import numpy as np

from pyrqa.exceptions import UnsupportedDataTypeException

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2020 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"

SUPPORTED_DATA_TYPES = (np.dtype('float16'),
                        np.dtype('float32'),
                        np.dtype('float64'))


class TimeSeries(object):
    """
    Time series.
    The reconstruction of vectors is conducted using the time delay method.

    :ivar dtype: Data type of the time series data.
    :ivar data: Time series data.
    :ivar embedding_dimension: Embedding dimension.
    :ivar time_delay: Time delay.
    """
    def __init__(self,
                 data,
                 dtype=np.float32,
                 embedding_dimension=2,
                 time_delay=2):
        self.dtype = dtype
        self.data = data
        self.embedding_dimension = embedding_dimension
        self.time_delay = time_delay

    @property
    def dtype(self):
        return self.__dtype

    @dtype.setter
    def dtype(self,
              dtype):
        if dtype not in SUPPORTED_DATA_TYPES:
            raise UnsupportedDataTypeException("Data type '%s' is not supported. Please select either numpy data type float16, float32 or float64." % dtype)

        self.__dtype = dtype

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self,
             data):
        self.__data = np.array(data, dtype=self.dtype)

    @property
    def length(self):
        """
        Length of data.
        """
        return len(self.data)

    @property
    def offset(self):
        """
        Time series offset based on embedding dimension and time delay.
        """
        return (self.embedding_dimension - 1) * self.time_delay

    @property
    def number_of_vectors(self):
        """
        Number of vectors based on the offset.
        """
        if self.length - self.offset < 0:
            return 0

        return self.length - self.offset

    def get_vectors(self,
                    start,
                    count):
        """
        Get vectors from the original time series.

        :param start: Start index within the original time series.
        :param count: Number of data points to be extracted.
        :returns: Extracted vectors.
        """
        recurrence_vectors = []

        for dim in np.arange(self.embedding_dimension):
            offset = dim * self.time_delay
            recurrence_vectors.append(self.data[(start + offset):(start + offset + count)])

        return np.array(recurrence_vectors,
                        dtype=self.dtype).transpose().ravel()

    def get_sub_series(self,
                       start,
                       count):
        """
        Get sub time series from the original time series.

        :param start: Start index within the original time series.
        :param count: Number of data points to be extracted.
        :returns: Extracted sub time series.
        """
        return self.data[start:start + count + self.offset]
