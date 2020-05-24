#!/usr/bin/env python

"""
Testing recurrence quantification analysis implementations according to the fixed radius and radius corridor neighbourhood condition.
"""

import numpy as np
import unittest

from pyrqa.neighbourhood import RadiusCorridor
from pyrqa.selector import SingleSelector
from pyrqa.variants.rp.radius.test import RPClassicFixedRadiusTestCase, \
    RPCrossFixedRadiusTestCase
from pyrqa.variants.rqa.radius.baseline import Baseline
from pyrqa.variants.rqa.radius.engine import Engine

from pyrqa.variants.rqa.radius.column_materialisation_bit_no_recycling import ColumnMaterialisationBitNoRecycling
from pyrqa.variants.rqa.radius.column_materialisation_bit_recycling import ColumnMaterialisationBitRecycling
from pyrqa.variants.rqa.radius.column_materialisation_byte_no_recycling import ColumnMaterialisationByteNoRecycling
from pyrqa.variants.rqa.radius.column_materialisation_byte_recycling import ColumnMaterialisationByteRecycling
from pyrqa.variants.rqa.radius.column_no_materialisation import ColumnNoMaterialisation
from pyrqa.variants.rqa.radius.row_materialisation_bit_no_recycling import RowMaterialisationBitNoRecycling
from pyrqa.variants.rqa.radius.row_materialisation_bit_recycling import RowMaterialisationBitRecycling
from pyrqa.variants.rqa.radius.row_materialisation_byte_no_recycling import RowMaterialisationByteNoRecycling
from pyrqa.variants.rqa.radius.row_materialisation_byte_recycling import RowMaterialisationByteRecycling
from pyrqa.variants.rqa.radius.row_no_materialisation import RowNoMaterialisation

VARIANTS = (ColumnMaterialisationBitNoRecycling,
            ColumnMaterialisationBitRecycling,
            ColumnMaterialisationByteNoRecycling,
            ColumnMaterialisationByteRecycling,
            ColumnNoMaterialisation,
            RowMaterialisationBitNoRecycling,
            RowMaterialisationBitRecycling,
            RowMaterialisationByteNoRecycling,
            RowMaterialisationByteRecycling,
            RowNoMaterialisation)

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2020 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"


class RQAClassicFixedRadiusTestCase(RPClassicFixedRadiusTestCase):
    """
    Tests for RQA, Classic, Fixed Radius.
    """
    @classmethod
    def setUpTimeSeriesLength(cls):
        """
        Set up time series length.

        :cvar time_series_length: Length of time series.
        """
        cls.time_series_length = np.random.randint(pow(2, 7),
                                                   pow(2, 8))

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

        if not edge_length:
            edge_length = settings.max_number_of_vectors

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

            self.compare_rqa_results(result_baseline,
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

                self.compare_rqa_results(result_baseline,
                                         result,
                                         variant=variant)


class RQAClassicRadiusCorridorTestCase(RQAClassicFixedRadiusTestCase):
    """
    Tests for RQA, Classic, Radius Corridor.
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


class RQACrossFixedRadiusTestCase(RPCrossFixedRadiusTestCase):
    """
    Tests for RQA, Cross, Fixed Radius.
    """
    @classmethod
    def setUpTimeSeriesLength(cls):
        """
        Set up time series length.

        :cvar time_series_length: Length of time series.
        """
        cls.time_series_length_x = np.random.randint(pow(2, 7),
                                                     pow(2, 8))
        cls.time_series_length_y = np.random.randint(pow(2, 7),
                                                     pow(2, 8))

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

        if not edge_length:
            edge_length = settings.max_number_of_vectors

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

            self.compare_rqa_results(result_baseline,
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

                self.compare_rqa_results(result_baseline,
                                         result,
                                         variant=variant)


class RQACrossRadiusCorridorTestCase(RQACrossFixedRadiusTestCase):
    """
    Tests for RQA, Cross, Radius Corridor.
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


if __name__ == "__main__":
    unittest.main()