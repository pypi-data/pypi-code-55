#!/usr/bin/env python

"""
Testing recurrence plot implementations according to the fixed radius and radius corridor neighbourhood.
"""

import numpy as np
import unittest

from pyrqa.analysis_type import Classic, \
    Cross
from pyrqa.neighbourhood import FixedRadius, \
    RadiusCorridor
from pyrqa.selector import SingleSelector
from pyrqa.tests.classic import ClassicTestCase
from pyrqa.tests.cross import CrossTestCase
from pyrqa.time_series import TimeSeries
from pyrqa.variants.rp.radius.baseline import Baseline
from pyrqa.variants.rp.radius.engine import Engine

from pyrqa.variants.rp.radius.column_materialisation_byte import \
    ColumnMaterialisationByte
from pyrqa.variants.rp.radius.row_materialisation_byte import \
    RowMaterialisationByte

VARIANTS = (ColumnMaterialisationByte,
            RowMaterialisationByte)

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2020 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"


class RPClassicFixedRadiusTestCase(ClassicTestCase):
    """
    Tests for RP, Classic, Fixed Radius.
    """
    @classmethod
    def setUpTimeSeriesLength(cls):
        """
        Set up time series length.

        :cvar time_series_length: Length of time series.
        """
        cls.time_series_length = np.random.randint(pow(2, 7),
                                                   pow(2, 8))

    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series: Time series consisting random floating point values.
        """
        cls.time_series = TimeSeries(np.random.rand(cls.time_series_length))

    @classmethod
    def setUpAnalysisType(cls):
        """
        Set up analysis type.

        :cvar analysis_type: Classic analysis type.
        """
        cls.analysis_type = Classic

    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood: Fixed radius Neighbourhood condition.
        """
        cls.neighbourhood = FixedRadius(np.random.uniform(.1, 1.))

    @classmethod
    def setUpMinimumEdgeLength(cls):
        """
        Set up minimum edge length.

        :return: Minimum edge length.
        """
        cls.minimum_edge_length = pow(2, 5)

    @classmethod
    def setUpClass(cls):
        """
        Set up test case.
        """
        cls.setUpTimeSeriesLength()
        cls.setUpTimeSeries()
        cls.setUpAnalysisType()
        cls.setUpNeighbourhood()
        cls.setUpMinimumEdgeLength()

    def perform_recurrence_analysis_computations(self,
                                                 settings,
                                                 opencl=None,
                                                 verbose=False,
                                                 edge_length=None,
                                                 selector=SingleSelector(),
                                                 variants_kwargs=None,
                                                 all_variants=False):
        if opencl:
            opencl.reset()

        baseline = Baseline(settings,
                            verbose=verbose)

        result_baseline = baseline.run()

        if all_variants:
            execution_engine = Engine(settings,
                                      opencl=opencl,
                                      verbose=False,
                                      edge_length=edge_length,
                                      selector=selector,
                                      variants=VARIANTS,
                                      variants_kwargs=variants_kwargs)

            result = execution_engine.run()

            self.compare_recurrence_plot_results(result_baseline,
                                                 result)
        else:
            for variant in VARIANTS:
                execution_engine = Engine(settings,
                                          opencl=opencl,
                                          verbose=False,
                                          edge_length=edge_length,
                                          selector=selector,
                                          variants=(variant,),
                                          variants_kwargs=variants_kwargs)

                result = execution_engine.run()

                self.compare_recurrence_plot_results(result_baseline,
                                                     result,
                                                     variant=variant)


class RPClassicRadiusCorridorTestCase(RPClassicFixedRadiusTestCase):
    """
    Tests for RP, Classic, Radius Corridor.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood: Radius corridor neighbourhood condition.
        """
        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood = RadiusCorridor(inner_radius=inner_radius,
                                           outer_radius=outer_radius)


class RPCrossFixedRadiusTestCase(CrossTestCase):
    """
    Tests for RP, Cross, Fixed Radius.
    """
    @classmethod
    def setUpTimeSeriesLength(cls):
        """
        Set up time series length.

        :cvar time_series_length_x: Length of time_series_x.
        :cvar time_series_length_y: Length of time_series_y.
        """
        cls.time_series_length_x = np.random.randint(pow(2, 7),
                                                     pow(2, 8))
        cls.time_series_length_y = np.random.randint(pow(2, 7),
                                                     pow(2, 8))

    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_x: Time series consisting random floating point values.
        :cvar time_series_y: Time series consisting random floating point values.
        """
        cls.time_series_x = TimeSeries(np.random.rand(cls.time_series_length_x))
        cls.time_series_y = TimeSeries(np.random.rand(cls.time_series_length_y))

        cls.time_series = (cls.time_series_x,
                           cls.time_series_y)

    @classmethod
    def setUpAnalysisType(cls):
        """
        Set up analysis type.

        :cvar analysis_type: Cross analysis type.
        """
        cls.analysis_type = Cross

    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood: Fixed radius neighbourhood.
        """
        cls.neighbourhood = FixedRadius(np.random.uniform(.1, 1.))

    @classmethod
    def setUpMinimumEdgeLength(cls):
        """
        Set up minimum edge length.

        :return: Minimum edge length.
        """
        cls.minimum_edge_length = pow(2, 5)

    @classmethod
    def setUpClass(cls):
        """
        Set up test case.
        """
        cls.setUpTimeSeriesLength()
        cls.setUpTimeSeries()
        cls.setUpAnalysisType()
        cls.setUpNeighbourhood()
        cls.setUpMinimumEdgeLength()

    def perform_recurrence_analysis_computations(self,
                                                 settings,
                                                 opencl=None,
                                                 verbose=False,
                                                 edge_length=None,
                                                 selector=SingleSelector(),
                                                 variants_kwargs=None,
                                                 all_variants=False):
        if opencl:
            opencl.reset()

        baseline = Baseline(settings,
                            verbose=verbose)

        result_baseline = baseline.run()

        if all_variants:
            execution_engine = Engine(settings,
                                      opencl=opencl,
                                      verbose=False,
                                      edge_length=edge_length,
                                      selector=selector,
                                      variants=VARIANTS,
                                      variants_kwargs=variants_kwargs)

            result = execution_engine.run()

            self.compare_recurrence_plot_results(result_baseline,
                                                 result)
        else:
            for variant in VARIANTS:
                execution_engine = Engine(settings,
                                          opencl=opencl,
                                          verbose=False,
                                          edge_length=edge_length,
                                          selector=selector,
                                          variants=(variant,),
                                          variants_kwargs=variants_kwargs)

                result = execution_engine.run()

                self.compare_recurrence_plot_results(result_baseline,
                                                     result,
                                                     variant=variant)


class RPCrossRadiusCorridorTestCase(RPCrossFixedRadiusTestCase):
    """
    Tests for RP, Cross, Radius Corridor.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood: Radius Corridor neighbourhood condition.
        """
        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood = RadiusCorridor(inner_radius=inner_radius,
                                           outer_radius=outer_radius)


if __name__ == "__main__":
    unittest.main()