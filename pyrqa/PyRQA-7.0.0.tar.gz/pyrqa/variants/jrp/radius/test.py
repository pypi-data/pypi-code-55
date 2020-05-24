#!/usr/bin/env python

"""
Testing joint recurrence plot implementations.
"""

import numpy as np
import unittest

from pyrqa.analysis_type import Classic, \
    Cross
from pyrqa.neighbourhood import FixedRadius, \
    RadiusCorridor
from pyrqa.selector import SingleSelector
from pyrqa.tests.joint import JointTestCase
from pyrqa.time_series import TimeSeries

from pyrqa.variants.jrp.radius.baseline import Baseline
from pyrqa.variants.jrp.radius.engine import Engine

from pyrqa.variants.jrp.radius.column_materialisation_byte import ColumnMaterialisationByte
from pyrqa.variants.jrp.radius.row_materialisation_byte import RowMaterialisationByte

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


class JRPClassicClassicFixedRadiusFixedRadiusTestCase(JointTestCase):
    """
    Tests for JRP, Classic x Classic, Fixed Radius x Fixed Radius.
    """
    @classmethod
    def setUpTimeSeriesLength(cls):
        """
        Set up time series length.

        :cvar time_series_length_minimum: Minimum length of time series.
        :cvar time_series_length_maximum: Maximum length of time series.
        :cvar time_series_length: Length of time series.
        """
        cls.time_series_length_minimum = pow(2, 7)
        cls.time_series_length_maximum = pow(2, 8)

        cls.time_series_length = np.random.randint(cls.time_series_length_minimum,
                                                   cls.time_series_length_maximum)

    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Time series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_1_x.
        :cvar time_series_2_x: Time series consisting random floating point values.
        :cvar time_series_2_y: Same time series as time_series_2_x.
        """
        cls.time_series_1_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_1_y = cls.time_series_1_x

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        cls.time_series_2_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_2_y = cls.time_series_2_x

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

    @classmethod
    def setUpAnalysisType(cls):
        """
        Set up analysis type.

        :cvar analysis_type_1: Classic analysis type.
        :cvar analysis_type_2: Classic analysis type.
        """
        cls.analysis_type_1 = Classic
        cls.analysis_type_2 = Classic

    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood_1: Fixed Radius neighbourhood condition.
        :cvar neighbourhood_2: Fixed Radius neighbourhood condition.
        """
        cls.neighbourhood_1 = FixedRadius(np.random.uniform(.1, 1.))
        cls.neighbourhood_2 = FixedRadius(np.random.uniform(.1, 1.))

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
            engine = Engine(settings,
                            opencl=opencl,
                            verbose=False,
                            edge_length=edge_length,
                            selector=selector,
                            variants=VARIANTS,
                            variants_kwargs=variants_kwargs)

            result = engine.run()

            self.compare_recurrence_plot_results(result_baseline,
                                                 result)
        else:
            for variant in VARIANTS:
                engine = Engine(settings,
                                opencl=opencl,
                                verbose=False,
                                edge_length=edge_length,
                                selector=selector,
                                variants=(variant,),
                                variants_kwargs=variants_kwargs)

                result = engine.run()

                self.compare_recurrence_plot_results(result_baseline,
                                                     result,
                                                     variant=variant)


class JRPClassicClassicFixedRadiusRadiusCorridorTestCase(JRPClassicClassicFixedRadiusFixedRadiusTestCase):
    """
    Tests for JRP, Classic x Classic, Fixed Radius x Radius Corridor.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood_1: Fixed Radius neighbourhood condition.
        :cvar neighbourhood_2: Radius corridor neighbourhood condition.
        """
        cls.neighbourhood_1 = FixedRadius(np.random.uniform(.1, 1.))

        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_2 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)


class JRPClassicClassicRadiusCorridorFixedRadiusTestCase(JRPClassicClassicFixedRadiusFixedRadiusTestCase):
    """
    Tests for JRP, Classic x Classic, Radius Corridor x Fixed Radius.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood_1: Radius corridor neighbourhood condition.
        :cvar neighbourhood_2: Fixed radius neighbourhood condition.
        """
        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_1 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)

        cls.neighbourhood_2 = FixedRadius(np.random.uniform(.1, 1.))


class JRPClassicClassicRadiusCorridorRadiusCorridorTestCase(JRPClassicClassicFixedRadiusFixedRadiusTestCase):
    """
    Tests for JRP, Classic x Classic, Radius Corridor x Radius Corridor.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood_1: Radius corridor neighbourhood condition.
        :cvar neighbourhood_2: Radius corridor neighbourhood condition.
        """
        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_1 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)

        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_2 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)


class JRPClassicCrossFixedRadiusFixedRadiusTestCase(JRPClassicClassicFixedRadiusFixedRadiusTestCase):
    """
    Tests for JRP, Classic x Cross, Fixed Radius x Fixed Radius.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Time series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_1_x.
        :cvar time_series_2_x: Time series consisting random floating point values.
        :cvar time_series_2_y: Time series consisting random floating point values.
        """
        cls.time_series_1_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_1_y = cls.time_series_1_x

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        cls.time_series_2_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_2_y = TimeSeries(np.random.rand(cls.time_series_length))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

    @classmethod
    def setUpAnalysisType(cls):
        """
        Set up analysis type.

        :cvar analysis_type_1: Classic analysis type.
        :cvar analysis_type_2: Cross analysis type.
        """
        cls.analysis_type_1 = Classic
        cls.analysis_type_2 = Cross


class JRPClassicCrossFixedRadiusRadiusCorridorTestCase(JRPClassicCrossFixedRadiusFixedRadiusTestCase):
    """
    Tests for JRP, Classic x Cross, Fixed Radius x Radius Corridor.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood_1: Fixed Radius neighbourhood condition.
        :cvar neighbourhood_2: Radius corridor neighbourhood condition.
        """
        cls.neighbourhood_1 = FixedRadius(np.random.uniform(.1, 1.))

        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_2 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)


class JRPClassicCrossRadiusCorridorFixedRadiusTestCase(JRPClassicCrossFixedRadiusFixedRadiusTestCase):
    """
    Tests for JRP, Classic x Cross, Radius Corridor x Fixed Radius.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood_1: Radius corridor neighbourhood condition.
        :cvar neighbourhood_2: Fixed radius neighbourhood condition.
        """
        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_1 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)

        cls.neighbourhood_2 = FixedRadius(np.random.uniform(.1, 1.))


class JRPClassicCrossRadiusCorridorRadiusCorridorTestCase(JRPClassicCrossFixedRadiusFixedRadiusTestCase):
    """
    Tests for JRP, Classic x Cross, Radius Corridor x Radius Corridor.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood_1: Radius corridor neighbourhood condition.
        :cvar neighbourhood_2: Radius corridor neighbourhood condition.
        """
        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_1 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)

        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_2 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)


class JRPCrossClassicFixedRadiusFixedRadiusTestCase(JRPClassicClassicFixedRadiusFixedRadiusTestCase):
    """
    Tests for JRP, Cross x Classic, Fixed Radius x Fixed Radius.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Time series consisting random floating point values.
        :cvar time_series_1_y: Time series consisting random floating point values.
        :cvar time_series_2_x: Time series consisting random floating point values.
        :cvar time_series_2_y: Time series consisting random floating point values.
        """
        cls.time_series_1_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_1_y = TimeSeries(np.random.rand(cls.time_series_length))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        cls.time_series_2_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_2_y = cls.time_series_2_x

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

    @classmethod
    def setUpAnalysisType(cls):
        """
        Set up analysis type.

        :cvar analysis_type_1: Cross analysis type.
        :cvar analysis_type_2: Classic analysis type.
        """
        cls.analysis_type_1 = Cross
        cls.analysis_type_2 = Classic


class JRPCrossClassicFixedRadiusRadiusCorridorTestCase(JRPCrossClassicFixedRadiusFixedRadiusTestCase):
    """
    Tests for JRP, Cross x Classic, Fixed Radius x Radius Corridor.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood_1: Fixed radius neighbourhood condition.
        :cvar neighbourhood_2: Radius corridor neighbourhood condition.
        """
        cls.neighbourhood_1 = FixedRadius(np.random.uniform(.1, 1.))

        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_2 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)


class JRPCrossClassicRadiusCorridorFixedRadiusTestCase(JRPCrossClassicFixedRadiusFixedRadiusTestCase):
    """
    Tests for JRP, Cross x Classic, Radius Corridor x Fixed Radius.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood_1: Radius corridor neighbourhood condition.
        :cvar neighbourhood_2: Fixed radius neighbourhood condition.
        """
        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_1 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)

        cls.neighbourhood_2 = FixedRadius(np.random.uniform(.1, 1.))


class JRPCrossClassicRadiusCorridorRadiusCorridorTestCase(JRPCrossClassicFixedRadiusFixedRadiusTestCase):
    """
    Tests for JRP, Cross x Classic, Radius Corridor x Radius Corridor.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood_1: Radius corridor neighbourhood condition.
        :cvar neighbourhood_2: Radius corridor neighbourhood condition.
        """
        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_1 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)

        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_2 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)


class JRPCrossCrossFixedRadiusFixedRadiusTestCase(JRPClassicClassicFixedRadiusFixedRadiusTestCase):
    """
    Tests for JRP, Cross x Cross, Fixed Radius x Fixed Radius.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length_x: Length of time series regarding X axis.
        :cvar time_series_length_y: Length of time series regarding Y axis.
        :cvar time_series_1_x: Time series consisting random floating point values.
        :cvar time_series_1_y: Time series consisting random floating point values.
        :cvar time_series_1: Tuple consisting of time_series_1_x and time_series_1_y.
        :cvar time_series_2_x: Time series consisting random floating point values.
        :cvar time_series_2_y: Time series consisting random floating point values.
        :cvar time_series_2: Tuple consisting of time_series_2_x and time_series_2_y.
        """
        cls.time_series_length_x = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)
        cls.time_series_length_y = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)

        cls.time_series_1_x = TimeSeries(np.random.rand(cls.time_series_length_x))
        cls.time_series_1_y = TimeSeries(np.random.rand(cls.time_series_length_y))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        cls.time_series_2_x = TimeSeries(np.random.rand(cls.time_series_length_x))
        cls.time_series_2_y = TimeSeries(np.random.rand(cls.time_series_length_y))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

    @classmethod
    def setUpAnalysisType(cls):
        """
        Set up analysis type.

        :cvar analysis_type_1: Cross analysis type.
        :cvar analysis_type_2: Cross analysis type.
        """
        cls.analysis_type_1 = Cross
        cls.analysis_type_2 = Cross


class JRPCrossCrossFixedRadiusRadiusCorridorTestCase(JRPCrossCrossFixedRadiusFixedRadiusTestCase):
    """
    Tests for JRP, Cross x Cross, Fixed Radius x Radius Corridor.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood_1: Fixed radius neighbourhood condition.
        :cvar neighbourhood_2: Radius corridor neighbourhood condition.
        """
        cls.neighbourhood_1 = FixedRadius(np.random.uniform(.1, 1.))

        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_2 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)


class JRPCrossCrossRadiusCorridorFixedRadiusTestCase(JRPCrossCrossFixedRadiusFixedRadiusTestCase):
    """
    Tests for JRP, Cross x Cross, Radius Corridor x Fixed Radius.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood_1: Radius corridor neighbourhood condition.
        :cvar neighbourhood_2: Fixed radius neighbourhood condition.
        """
        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_1 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)

        cls.neighbourhood_2 = FixedRadius(np.random.uniform(.1, 1.))


class JRPCrossCrossRadiusCorridorRadiusCorridorTestCase(JRPCrossCrossFixedRadiusFixedRadiusTestCase):
    """
    Tests for JRP, Cross x Cross, Radius Corridor x Radius Corridor.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood_1: Radius corridor neighbourhood condition.
        :cvar neighbourhood_2: Radius corridor neighbourhood condition.
        """
        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_1 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)

        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_2 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)


if __name__ == "__main__":
    unittest.main()
