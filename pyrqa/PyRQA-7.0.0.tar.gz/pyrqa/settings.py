#!/usr/bin/env python

"""
Settings
"""

import os

import numpy as np

from pyrqa.analysis_type import Classic, \
    Joint
from pyrqa.metric import EuclideanMetric
from pyrqa.neighbourhood import FixedRadius, \
    FAN
from pyrqa.time_series import TimeSeries
from pyrqa.exceptions import InvalidTimeSeriesInputException, \
    InvalidSettingsException, \
    DeviatingEmbeddingDimensionException, \
    DeviatingTimeDelayException, \
    DeviatingFloatingPointPrecisionException

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2020 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"

DTYPE_TO_CLASS_MAPPING = {np.dtype('float16'): np.float16,
                          np.dtype('float32'): np.float32,
                          np.dtype('float64'): np.float64}


class Settings(object):
    """
    Settings of recurrence analysis computations.

    :ivar time_series: Time series to be analyzed.
    :ivar analysis_type: Type of recurrence analysis.
    :ivar similarity_measure: Similarity measure, e.g., EuclideanMetric.
    :ivar neighbourhood: Neighbourhood for detecting neighbours, e.g., FixedRadius(1.0).
    :ivar theiler_corrector: Theiler corrector.
    """
    def __init__(self,
                 time_series,
                 analysis_type=Classic,
                 similarity_measure=EuclideanMetric,
                 neighbourhood=FixedRadius(),
                 theiler_corrector=1):
        self.time_series_x = self.get_time_series(time_series,
                                                  0)
        self.time_series_y = self.get_time_series(time_series,
                                                  1)

        self.analysis_type = analysis_type
        self.similarity_measure = similarity_measure
        self.neighbourhood = neighbourhood
        self.theiler_corrector = theiler_corrector

    @staticmethod
    def get_time_series(time_series,
                        ind):
        """
        Get single time series object.

        :param time_series: One or multiple time series.
        :param ind: Index of time series to retrieve.
        :return: Single time series object.
        """
        if type(time_series) is TimeSeries:
            return time_series
        elif (type(time_series) is tuple or type(time_series) is list) and len(time_series) == 2:
            return time_series[ind]
        else:
            raise InvalidTimeSeriesInputException(
                "Either a single time series or tuple/list of two time series should be passed as argument.")

    @property
    def time_series_x(self):
        """
        Get time series on x axis.

        :return: Time series on x axis.
        """
        try:
            return self.__time_series_x
        except Exception:
            return None

    @time_series_x.setter
    def time_series_x(self,
                      time_series_x):
        """
        Set time series on x axis.

        :param time_series_x: Time series on x axis.
        """
        if not type(time_series_x) == TimeSeries:
            raise InvalidTimeSeriesInputException("Time series x is not of type TimeSeries.")

        self.__time_series_x = time_series_x

    @property
    def time_series_y(self):
        """
        Get time series on y axis.

        :return: Time series on y axis.
        """
        try:
            return self.__time_series_y
        except Exception:
            return None

    @time_series_y.setter
    def time_series_y(self,
                      time_series_y):
        """
        Set time series on y axis.

        :param time_series_y: Time series on y axis.
        """
        if not type(time_series_y) == TimeSeries:
            raise InvalidTimeSeriesInputException("Time series y is not of type TimeSeries.")

        self.__time_series_y = time_series_y

    @property
    def embedding_dimension(self):
        """
        Get embedding dimension.

        :return: Embedding dimension.
        """
        if not self.time_series_x.embedding_dimension == self.time_series_y.embedding_dimension:
            raise DeviatingEmbeddingDimensionException(
                "Embedding dimension '%d' of time series x deviates from embedding dimension '%d' of time series y." % (
                    self.time_series_x.embedding_dimension,
                    self.time_series_y.embedding_dimension))

        return self.time_series_x.embedding_dimension

    @property
    def time_delay(self):
        """
        Get time delay.

        :return: Time delay.
        """
        if not self.time_series_x.time_delay == self.time_series_y.time_delay:
            raise DeviatingTimeDelayException(
                "Time delay '%d' of time series x deviates from time delay '%d' of time series y." % (
                    self.time_series_x.time_delay,
                    self.time_series_y.time_delay))

        return self.time_series_x.time_delay

    @property
    def number_of_vectors_x(self):
        """
        Number of vectors of the time series on the x axis.

        :return: Number of vectors of the time series on the x axis.
        """
        return self.time_series_x.number_of_vectors

    @property
    def number_of_vectors_y(self):
        """
        Number of vectors of the time series on the y axis.

        :return: Number of vectors of the time series on the y axis.
        """
        return self.time_series_y.number_of_vectors

    @property
    def max_number_of_vectors(self):
        """
        Get maximum of vectors.

        :return: Maximum number of vectors.
        """
        if self.time_series_x and self.time_series_y:
            if self.time_series_x.length > self.time_series_y.length:
                return self.time_series_x.number_of_vectors
            else:
                return self.time_series_y.number_of_vectors
        elif not self.time_series_x:
            raise InvalidTimeSeriesInputException("Missing time series x.")
        elif not self.time_series_y:
            raise InvalidTimeSeriesInputException("Missing time series y.")

    @property
    def base_path(self):
        """
        Base path of the project.
        """
        return os.path.dirname(os.path.abspath(__file__))

    @property
    def is_matrix_symmetric(self):
        """
        Is the recurrence matrix symmetric?
        """
        return self.similarity_measure.is_symmetric() and \
               not isinstance(self.neighbourhood, FAN) and \
               self.analysis_type is Classic

    @property
    def create_matrix_operator_name(self):
        """
        Get prefix of the name of the kernel function to create the recurrence matrix.

        :rtype: String.
        """
        return "create_matrix"

    @property
    def detect_vertical_lines_operator_name(self):
        """
        Get prefix of the name of the kernel function to detect vertical lines.

        :rtype: String.
        """
        return "detect_vertical_lines"

    @property
    def detect_diagonal_lines_operator_name(self):
        """
        Get prefix of the name of the kernel function to detect diagonal lines.

        :rtype: String.
        """
        if self.is_matrix_symmetric:
            return "detect_diagonal_lines_symmetric"

        return "detect_diagonal_lines"

    @staticmethod
    def get_kernel_function_name(operator_name,
                                 neighbourhood_name,
                                 similarity_measure_name):
        """
        Get the full name of the kernel function to select.

        :param operator_name: Name of the operator.
        :param neighbourhood_name: Name of the neighbourhood.
        :param similarity_measure_name: Name of the similarity measure.
        :rtype: String.
        """
        if neighbourhood_name and similarity_measure_name:
            return "_".join([operator_name,
                             neighbourhood_name,
                             similarity_measure_name])

        return operator_name

    @property
    def create_matrix_kernel_name(self):
        """
        Full name of the kernel function to create the recurrence matrix

        :rtype: String.
        """
        return self.get_kernel_function_name(self.create_matrix_operator_name,
                                             self.neighbourhood.name,
                                             self.similarity_measure.name)

    @property
    def detect_vertical_lines_kernel_name(self):
        """
        Full name of the kernel function to detect vertical lines.

        :rtype: String.
        """
        return self.get_kernel_function_name(self.detect_vertical_lines_operator_name,
                                             self.neighbourhood.name,
                                             self.similarity_measure.name)

    @property
    def detect_diagonal_lines_kernel_name(self):
        """
        Full name of the kernel function to detect diagonal lines.

        :rtype: String.
        """
        return self.get_kernel_function_name(self.detect_diagonal_lines_operator_name,
                                             self.neighbourhood.name,
                                             self.similarity_measure.name)

    @property
    def kernels_sub_dir(self):
        """
        Get the path of the kernel sub directory.

        :rtype: String.
        """
        return self.similarity_measure.name

    @property
    def dtype(self):
        """
        Floating point data type for the time series.
        """
        if not self.time_series_x.dtype == self.time_series_y.dtype:
            raise DeviatingFloatingPointPrecisionException(
                "Dtype '%s' of time series x deviates from dtype '%s' of time series y." % (self.time_series_x.dtype,
                                                                                            self.time_series_y.dtype))

        return DTYPE_TO_CLASS_MAPPING[self.time_series_x.data.dtype]

    @staticmethod
    def clear_buffer_kernel_name(data_type):
        """
        Get name of the kernel function used to clear a buffer.

        :param data_type: Data type that is used to represent the data values.
        :return: Name of clear buffer kernel.
        :rtype: String.
        """
        return "clear_buffer_%s" % data_type.__name__

    def __str__(self):
        return "Recurrence Analysis Settings\n" \
               "----------------------------\n" \
               "Analysis type: %s\n" \
               "Similarity measure: %s\n" \
               "Neighbourhood: %s\n" \
               "Theiler corrector: %d\n" \
               "Matrix symmetry: %r\n" % (self.analysis_type,
                                          self.similarity_measure.__name__,
                                          self.neighbourhood,
                                          self.theiler_corrector,
                                          self.is_matrix_symmetric)


class JointSettings(object):
    """
    Settings of joint recurrence analysis computations.

    :ivar settings_1: Settings of the first (cross) recurrence matrix.
    :ivar settings_2: Settings of the second (cross) recurrence matrix.
    """
    def __init__(self,
                 settings_1,
                 settings_2):
        self.settings_1 = settings_1
        self.settings_2 = settings_2

        self.validate_settings()

    def validate_settings(self):
        """
        Validation of the settings.

        :rtype: Boolean
        """
        if not self.settings_1.time_series_x.number_of_vectors == self.settings_2.time_series_x.number_of_vectors:
            raise InvalidSettingsException(
                "Different values regarding the number of vectors of the time series on the x axis are inconsistent.")
        if not self.settings_1.time_series_y.number_of_vectors == self.settings_2.time_series_y.number_of_vectors:
            raise InvalidSettingsException(
                "The number of vector of the time series on the y axis are inconsistent.")
        return True

    @property
    def analysis_type(self):
        """
        Analysis type of the joint recurrence analysis.

        :return: Analysis type of the joint recurrence analysis
        """
        return Joint

    @property
    def join_matrices_operator_name(self):
        """
        Full name of the kernel function to join matrices.

        :rtype: String.
        """
        return "join_matrices"

    @property
    def is_matrix_symmetric(self):
        """
        Is the joint recurrence matrix symmetric?

        :rtype: Boolean.
        """
        if self.settings_1.is_matrix_symmetric and self.settings_2.is_matrix_symmetric:
            return True
        else:
            return False

    @property
    def dtype(self):
        """
        Data type of the time series data.

        :rtype: Data type.
        """
        if self.settings_1.dtype == self.settings_2.dtype:
            return self.settings_1.dtype
        else:
            raise InvalidSettingsException("Different values regarding dtype.")

    @property
    def theiler_corrector(self):
        """
        Theiler corrector.

        :rtype: Integer.
        """
        if self.settings_1.theiler_corrector == self.settings_2.theiler_corrector:
            return self.settings_1.theiler_corrector
        else:
            raise InvalidSettingsException("Different values regarding theiler_corrector.")

    @property
    def detect_vertical_lines_operator_name(self):
        """
        Name of the operator to detect vertical lines.

        :rtype: String.
        """

        if self.settings_1.detect_vertical_lines_operator_name == self.settings_2.detect_vertical_lines_operator_name:
            return self.settings_1.detect_vertical_lines_operator_name
        else:
            raise InvalidSettingsException("Different values regarding detect_vertical_lines_operator_name.")

    @property
    def detect_diagonal_lines_operator_name(self):
        """
        Name of the operator to detect diagonal lines.

        :rtype: String.
        """
        if self.settings_1.detect_diagonal_lines_operator_name == self.settings_2.detect_diagonal_lines_operator_name:
            return self.settings_1.detect_diagonal_lines_operator_name
        else:
            return "detect_diagonal_lines"

    @property
    def number_of_vectors_x(self):
        """
        Number of vectors of the time series on the x axis.

        :rtype: Integer.
        """
        if self.settings_1.time_series_x.number_of_vectors == self.settings_2.time_series_x.number_of_vectors:
            return self.settings_1.time_series_x.number_of_vectors
        else:
            raise InvalidSettingsException(
                "Different values regarding the number of vectors of the time series on the x axis are inconsistent.")

    @property
    def number_of_vectors_y(self):
        """
        Number of vectors of the time series on the y axis.

        :rtype: Integer.
        """
        if self.settings_1.time_series_y.number_of_vectors == self.settings_2.time_series_y.number_of_vectors:
            return self.settings_1.time_series_y.number_of_vectors
        else:
            raise InvalidSettingsException(
                "The number of vector of the time series on the y axis are inconsistent.")

    @property
    def max_number_of_vectors(self):
        """
        Maximum number of vectors of first and second settings object.

        :rtype: Integer.
        """
        if self.settings_1.max_number_of_vectors == self.settings_2.max_number_of_vectors:
            return self.settings_1.max_number_of_vectors
        else:
            raise InvalidSettingsException("Different values regarding detect_diagonal_lines_operator_name.")

    @property
    def kernels_sub_dir(self):
        """
        Get the path of the kernel sub directory.

        :rtype: String.
        """
        return self.settings_1.kernels_sub_dir, \
            self.settings_2.kernels_sub_dir

    def clear_buffer_kernel_name(self,
                                 data_type):
        """
        Get name of the kernel function used to clear a buffer.

        :param data_type: Data type that is used to represent the data values.
        :return: Name of clear buffer kernel.
        :rtype: String.
        """
        if self.settings_1.clear_buffer_kernel_name(data_type) == self.settings_2.clear_buffer_kernel_name(data_type):
            return "clear_buffer_%s" % data_type.__name__
        else:
            raise InvalidSettingsException("Different values regarding clear_buffer_kernel_name.")

    def __str__(self):
        return "Joint Recurrence Analysis Settings\n" \
               "==================================\n" \
               "Analysis type: %s\n" \
               "First recurrence matrix:\n\n%s\n\n" \
               "Second recurrence matrix:\n\n%s\n\n" \
               "Theiler corrector: %d\n" \
               "Matrix symmetry: %r\n" % (self.analysis_type,
                                          self.settings_1.__str__(),
                                          self.settings_2.__str__(),
                                          self.theiler_corrector,
                                          self.is_matrix_symmetric)
