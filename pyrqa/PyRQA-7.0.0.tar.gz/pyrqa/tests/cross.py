#!/usr/bin/env python

"""
Tests for cross variant testing.
"""

import sys
import unittest

import numpy as np

from pyrqa.analysis_type import Cross
from pyrqa.metric import EuclideanMetric, \
    MaximumMetric, \
    TaxicabMetric
from pyrqa.opencl import OpenCL
from pyrqa.selector import SingleSelector
from pyrqa.settings import Settings
from pyrqa.tests.classic import ClassicTestCase
from pyrqa.time_series import TimeSeries

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2020 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"


class CrossTestCase(ClassicTestCase):
    """
    Tests for cross recurrence analysis.
    """
    def test_embedding_parameters(self):
        """
        Test using different than the default recurrence analysis settings.
        """
        for metric in [EuclideanMetric,
                       MaximumMetric,
                       TaxicabMetric]:
            embedding_dimension = np.random.randint(1, 10)
            time_delay = np.random.randint(1, 10)

            time_series_x = TimeSeries(self.time_series_x.data,
                                       dtype=self.time_series_x.dtype,
                                       embedding_dimension=embedding_dimension,
                                       time_delay=time_delay)

            time_series_y = TimeSeries(self.time_series_y.data,
                                       dtype=self.time_series_y.dtype,
                                       embedding_dimension=embedding_dimension,
                                       time_delay=time_delay)

            settings = Settings((time_series_x,
                                 time_series_y),
                                analysis_type=self.analysis_type,
                                neighbourhood=self.neighbourhood,
                                similarity_measure=metric)

            self.perform_recurrence_analysis_computations(settings,
                                                          selector=SingleSelector(loop_unroll_factors=(1,)))

    @unittest.skipIf("--all" not in sys.argv, "Activate the test using the argument '--all'.")
    def test_precision_float(self):
        """
        Test floating points single precision.
        """
        for metric in [EuclideanMetric,
                       MaximumMetric,
                       TaxicabMetric]:
            time_series_x = TimeSeries(self.time_series_x.data,
                                       dtype=np.float32)
            time_series_y = TimeSeries(self.time_series_y.data,
                                       dtype=np.float32)

            settings = Settings((time_series_x,
                                 time_series_y),
                                analysis_type=self.analysis_type,
                                neighbourhood=self.neighbourhood,
                                similarity_measure=metric)

            self.perform_recurrence_analysis_computations(settings,
                                                          verbose=True)

    @unittest.skipIf("--all" not in sys.argv, "Activate the test using the argument '--all'.")
    @unittest.expectedFailure
    def test_precision_half(self):
        """
        Test floating points half precision.
        """
        for metric in [EuclideanMetric,
                       MaximumMetric,
                       TaxicabMetric]:
            time_series_x = TimeSeries(self.time_series_x.data,
                                       dtype=np.float16)
            time_series_y = TimeSeries(self.time_series_y.data,
                                       dtype=np.float16)

            settings = Settings((time_series_x,
                                 time_series_y),
                                analysis_type=self.analysis_type,
                                neighbourhood=self.neighbourhood,
                                similarity_measure=metric)

            self.perform_recurrence_analysis_computations(settings,
                                                          verbose=True)

    @unittest.skipIf("--all" not in sys.argv, "Activate the test using the argument '--all'.")
    @unittest.expectedFailure
    def test_precision_double(self):
        """
        Test floating points double precision.
        """
        for metric in [EuclideanMetric,
                       MaximumMetric,
                       TaxicabMetric]:
            time_series_x = TimeSeries(self.time_series_x.data,
                                       dtype=np.float64)
            time_series_y = TimeSeries(self.time_series_y.data,
                                       dtype=np.float64)

            settings = Settings((time_series_x,
                                 time_series_y),
                                analysis_type=Cross,
                                neighbourhood=self.neighbourhood,
                                similarity_measure=metric)

            self.perform_recurrence_analysis_computations(settings,
                                                          verbose=True)

    @unittest.skipIf("--all" not in sys.argv, "Activate the test using the argument '--all'.")
    @unittest.expectedFailure
    def test_multiple_devices_per_platform(self):
        """
        Test using all compute devices per OpenCL platform available.
        """
        if sys.version_info.major == 2:
            itr = OpenCL.get_device_ids_per_platform_id().iteritems()
        if sys.version_info.major == 3:
            itr = OpenCL.get_device_ids_per_platform_id().items()

        for platform_id, device_ids in itr:
            opencl = OpenCL(platform_id=platform_id,
                            device_ids=device_ids)

            for metric in [EuclideanMetric,
                           MaximumMetric,
                           TaxicabMetric]:
                settings = Settings(self.time_series,
                                    analysis_type=self.analysis_type,
                                    neighbourhood=self.neighbourhood,
                                    similarity_measure=metric)

                self.perform_recurrence_analysis_computations(settings,
                                                              opencl=opencl,
                                                              edge_length=np.int(np.ceil(
                                                                  np.float(settings.max_number_of_vectors) / len(
                                                                      device_ids))),
                                                              selector=SingleSelector(loop_unroll_factors=(1,)))
