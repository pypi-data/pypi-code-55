#!/usr/bin/env python

"""
Tests for joint variant testing.
"""

import random
import sys
import unittest

import numpy as np

from pyrqa.metric import EuclideanMetric, \
    MaximumMetric, \
    TaxicabMetric
from pyrqa.opencl import OpenCL
from pyrqa.selector import SingleSelector, \
    EpsilonGreedySelector, \
    VWGreedySelector, \
    EpsilonDecreasingSelector, \
    EpsilonFirstSelector
from pyrqa.settings import Settings, \
    JointSettings
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

METRICS = (EuclideanMetric,
           MaximumMetric,
           TaxicabMetric)


class JointTestCase(ClassicTestCase):
    """
    Tests for joint recurrence analysis.
    """
    def test_default(self):
        """
        Test using the default recurrence analysis settings.
        """
        for _ in range(3):
            settings_1 = Settings(self.time_series_1,
                                  analysis_type=self.analysis_type_1,
                                  neighbourhood=self.neighbourhood_1,
                                  similarity_measure=random.choice(METRICS))

            settings_2 = Settings(self.time_series_2,
                                  analysis_type=self.analysis_type_2,
                                  neighbourhood=self.neighbourhood_2,
                                  similarity_measure=random.choice(METRICS))

            settings = JointSettings(settings_1,
                                     settings_2)

            self.perform_recurrence_analysis_computations(settings,
                                                          selector=SingleSelector(loop_unroll_factors=(1,)))

    def test_optimisations_enabled(self):
        """
        Test using the default recurrence analysis settings while enabling optimisations.
        """
        for _ in range(3):
            settings_1 = Settings(self.time_series_1,
                                  analysis_type=self.analysis_type_1,
                                  neighbourhood=self.neighbourhood_1,
                                  similarity_measure=random.choice(METRICS))

            settings_2 = Settings(self.time_series_2,
                                  analysis_type=self.analysis_type_2,
                                  neighbourhood=self.neighbourhood_2,
                                  similarity_measure=random.choice(METRICS))

            settings = JointSettings(settings_1,
                                     settings_2)

            self.perform_recurrence_analysis_computations(settings,
                                                          selector=SingleSelector(loop_unroll_factors=(1,)),
                                                          variants_kwargs={'optimisations_enabled': True})

    def test_partition(self):
        """
        Test partition of recurrence matrix.
        """
        for _ in range(3):
            settings_1 = Settings(self.time_series_1,
                                  analysis_type=self.analysis_type_1,
                                  neighbourhood=self.neighbourhood_1,
                                  similarity_measure=random.choice(METRICS))

            settings_2 = Settings(self.time_series_2,
                                  analysis_type=self.analysis_type_2,
                                  neighbourhood=self.neighbourhood_2,
                                  similarity_measure=random.choice(METRICS))

            settings = JointSettings(settings_1,
                                     settings_2)

            self.perform_recurrence_analysis_computations(settings,
                                                          edge_length=np.random.randint(self.minimum_edge_length,
                                                                                        settings.max_number_of_vectors),
                                                          selector=SingleSelector(loop_unroll_factors=(1,)))

    def test_embedding_parameters(self):
        """
        Test using different than the default recurrence analysis settings.
        """
        for metric in [EuclideanMetric,
                       MaximumMetric,
                       TaxicabMetric]:
            embedding_dimension = np.random.randint(1, 10)
            time_delay = np.random.randint(1, 10)

            time_series_1_x = TimeSeries(self.time_series_1_x.data,
                                         dtype=self.time_series_1_x.dtype,
                                         embedding_dimension=embedding_dimension,
                                         time_delay=time_delay)

            time_series_1_y = TimeSeries(self.time_series_1_y.data,
                                         dtype=self.time_series_1_y.dtype,
                                         embedding_dimension=embedding_dimension,
                                         time_delay=time_delay)

            settings_1 = Settings((time_series_1_x,
                                   time_series_1_y),
                                  analysis_type=self.analysis_type_1,
                                  neighbourhood=self.neighbourhood_1,
                                  similarity_measure=random.choice(METRICS))

            time_series_2_x = TimeSeries(self.time_series_2_x.data,
                                         dtype=self.time_series_2_x.dtype,
                                         embedding_dimension=embedding_dimension,
                                         time_delay=time_delay)

            time_series_2_y = TimeSeries(self.time_series_2_y.data,
                                         dtype=self.time_series_2_y.dtype,
                                         embedding_dimension=embedding_dimension,
                                         time_delay=time_delay)

            settings_2 = Settings((time_series_2_x,
                                   time_series_2_y),
                                  analysis_type=self.analysis_type_2,
                                  neighbourhood=self.neighbourhood_2,
                                  similarity_measure=random.choice(METRICS))

            settings = JointSettings(settings_1,
                                     settings_2)

            self.perform_recurrence_analysis_computations(settings,
                                                          selector=SingleSelector(loop_unroll_factors=(1,)))

    def test_loop_unroll(self):
        """
        Test using different than the default loop unroll parameter assignment.
        """
        for _ in range(3):
            settings_1 = Settings(self.time_series_1,
                                  analysis_type=self.analysis_type_1,
                                  neighbourhood=self.neighbourhood_1,
                                  similarity_measure=random.choice(METRICS))

            settings_2 = Settings(self.time_series_2,
                                  analysis_type=self.analysis_type_2,
                                  neighbourhood=self.neighbourhood_2,
                                  similarity_measure=random.choice(METRICS))

            settings = JointSettings(settings_1,
                                     settings_2)

            choices = np.array([1, 2, 4, 8, 16])

            self.perform_recurrence_analysis_computations(settings,
                                                          verbose=True,
                                                          selector=SingleSelector(loop_unroll_factors=(choices[np.random.randint(0, choices.size - 1)],)))

    def test_selector_epsilon_greedy(self):
        """
        Test epsilon greedy selection strategy.
        """
        for _ in range(3):
            settings_1 = Settings(self.time_series_1,
                                  analysis_type=self.analysis_type_1,
                                  neighbourhood=self.neighbourhood_1,
                                  similarity_measure=random.choice(METRICS))

            settings_2 = Settings(self.time_series_2,
                                  analysis_type=self.analysis_type_2,
                                  neighbourhood=self.neighbourhood_2,
                                  similarity_measure=random.choice(METRICS))

            settings = JointSettings(settings_1,
                                     settings_2)

            explore = np.arange(1, 11)

            self.perform_recurrence_analysis_computations(settings,
                                                          edge_length=np.random.randint(self.minimum_edge_length, settings.max_number_of_vectors),
                                                          selector=EpsilonGreedySelector(explore=explore[np.random.randint(0, explore.size)]),
                                                          all_variants=True)

    def test_selector_vw_greedy(self):
        """
        Test vw greedy selection strategy.
        """
        for _ in range(3):
            settings_1 = Settings(self.time_series_1,
                                  analysis_type=self.analysis_type_1,
                                  neighbourhood=self.neighbourhood_1,
                                  similarity_measure=random.choice(METRICS))

            settings_2 = Settings(self.time_series_2,
                                  analysis_type=self.analysis_type_2,
                                  neighbourhood=self.neighbourhood_2,
                                  similarity_measure=random.choice(METRICS))

            settings = JointSettings(settings_1,
                                     settings_2)

            explore = np.arange(1, 11)
            factor = np.arange(1, 4)

            self.perform_recurrence_analysis_computations(settings,
                                                          edge_length=np.random.randint(self.minimum_edge_length, settings.max_number_of_vectors),
                                                          selector=VWGreedySelector(explore=explore[np.random.randint(0, explore.size)],
                                                                                    factor=factor[np.random.randint(0, factor.size)]),
                                                          all_variants=True)

    def test_selector_epsilon_decreasing(self):
        """
        Test epsilon decreasing selection strategy.
        """
        for _ in range(3):
            settings_1 = Settings(self.time_series_1,
                                  analysis_type=self.analysis_type_1,
                                  neighbourhood=self.neighbourhood_1,
                                  similarity_measure=random.choice(METRICS))

            settings_2 = Settings(self.time_series_2,
                                  analysis_type=self.analysis_type_2,
                                  neighbourhood=self.neighbourhood_2,
                                  similarity_measure=random.choice(METRICS))

            settings = JointSettings(settings_1,
                                     settings_2)

            explore = np.arange(1, 11)
            delta = np.arange(1, 6)

            self.perform_recurrence_analysis_computations(settings,
                                                          edge_length=np.random.randint(self.minimum_edge_length, settings.max_number_of_vectors),
                                                          selector=EpsilonDecreasingSelector(explore=explore[np.random.randint(0, explore.size)],
                                                                                             delta=delta[np.random.randint(0, delta.size)]),
                                                          all_variants=True)

    def test_selector_epsilon_first(self):
        """
        Test epsilon first selection strategies.
        """
        for _ in range(3):
            settings_1 = Settings(self.time_series_1,
                                  analysis_type=self.analysis_type_1,
                                  neighbourhood=self.neighbourhood_1,
                                  similarity_measure=random.choice(METRICS))

            settings_2 = Settings(self.time_series_2,
                                  analysis_type=self.analysis_type_2,
                                  neighbourhood=self.neighbourhood_2,
                                  similarity_measure=random.choice(METRICS))

            settings = JointSettings(settings_1,
                                     settings_2)

            explore = np.arange(1, 11)

            self.perform_recurrence_analysis_computations(settings,
                                                          edge_length=np.random.randint(self.minimum_edge_length, settings.max_number_of_vectors),
                                                          selector=EpsilonFirstSelector(explore=explore[np.random.randint(0, explore.size)]),
                                                          all_variants=True)

    @unittest.skipIf("--all" not in sys.argv, "Activate the test using the argument '--all'.")
    def test_precision_float(self):
        """
        Test floating points single precision.
        """
        for _ in range(3):
            time_series_1_x = TimeSeries(self.time_series_1_x.data,
                                         dtype=np.float32)
            time_series_1_y = TimeSeries(self.time_series_1_y.data,
                                         dtype=np.float32)

            settings_1 = Settings((time_series_1_x,
                                   time_series_1_y),
                                  analysis_type=self.analysis_type_1,
                                  neighbourhood=self.neighbourhood_1,
                                  similarity_measure=random.choice(METRICS))

            time_series_2_x = TimeSeries(self.time_series_2_x.data,
                                         dtype=np.float32)
            time_series_2_y = TimeSeries(self.time_series_2_y.data,
                                         dtype=np.float32)

            settings_2 = Settings((time_series_2_x,
                                   time_series_2_y),
                                  analysis_type=self.analysis_type_2,
                                  neighbourhood=self.neighbourhood_2,
                                  similarity_measure=random.choice(METRICS))

            settings = JointSettings(settings_1,
                                     settings_2)

            self.perform_recurrence_analysis_computations(settings,
                                                          verbose=True)

    @unittest.skipIf("--all" not in sys.argv, "Activate the test using the argument '--all'.")
    @unittest.expectedFailure
    def test_precision_half(self):
        """
        Test floating points half precision.
        """
        for _ in range(3):
            time_series_1_x = TimeSeries(self.time_series_1_x.data,
                                         dtype=np.float16)
            time_series_1_y = TimeSeries(self.time_series_1_y.data,
                                         dtype=np.float16)

            settings_1 = Settings((time_series_1_x,
                                   time_series_1_y),
                                  analysis_type=self.analysis_type_1,
                                  neighbourhood=self.neighbourhood_1,
                                  similarity_measure=random.choice(METRICS))

            time_series_2_x = TimeSeries(self.time_series_2_x.data,
                                         dtype=np.float16)
            time_series_2_y = TimeSeries(self.time_series_2_y.data,
                                         dtype=np.float16)

            settings_2 = Settings((time_series_2_x,
                                   time_series_2_y),
                                  analysis_type=self.analysis_type_2,
                                  neighbourhood=self.neighbourhood_2,
                                  similarity_measure=random.choice(METRICS))

            settings = JointSettings(settings_1,
                                     settings_2)

            self.perform_recurrence_analysis_computations(settings,
                                                          verbose=True)

    @unittest.skipIf("--all" not in sys.argv, "Activate the test using the argument '--all'.")
    @unittest.expectedFailure
    def test_precision_double(self):
        """
        Test floating points double precision.
        """
        for _ in range(3):
            time_series_1_x = TimeSeries(self.time_series_1_x.data,
                                         dtype=np.float64)
            time_series_1_y = TimeSeries(self.time_series_1_y.data,
                                         dtype=np.float64)

            settings_1 = Settings((time_series_1_x,
                                   time_series_1_y),
                                  analysis_type=self.analysis_type_1,
                                  neighbourhood=self.neighbourhood_1,
                                  similarity_measure=random.choice(METRICS))

            time_series_2_x = TimeSeries(self.time_series_2_x.data,
                                         dtype=np.float64)
            time_series_2_y = TimeSeries(self.time_series_2_y.data,
                                         dtype=np.float64)

            settings_2 = Settings((time_series_2_x,
                                   time_series_2_y),
                                  analysis_type=self.analysis_type_2,
                                  neighbourhood=self.neighbourhood_2,
                                  similarity_measure=random.choice(METRICS))

            settings = JointSettings(settings_1,
                                     settings_2)

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

            for _ in range(3):
                settings_1 = Settings(self.time_series_1,
                                      analysis_type=self.analysis_type_1,
                                      neighbourhood=self.neighbourhood_1,
                                      similarity_measure=random.choice(METRICS))

                settings_2 = Settings(self.time_series_2,
                                      analysis_type=self.analysis_type_2,
                                      neighbourhood=self.neighbourhood_2,
                                      similarity_measure=random.choice(METRICS))

                settings = JointSettings(settings_1,
                                         settings_2)

                self.perform_recurrence_analysis_computations(settings,
                                                              opencl=opencl,
                                                              edge_length=np.int(np.ceil(
                                                                  np.float(settings.max_number_of_vectors) / len(
                                                                      device_ids))),
                                                              selector=SingleSelector(loop_unroll_factors=(1,)))