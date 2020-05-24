#!/usr/bin/env python

"""
Testing recurrence plot implementations according to the unthresholded neighbourhood condition.
"""

import unittest

from pyrqa.neighbourhood import Unthresholded
from pyrqa.variants.rp.unthresholded.baseline import Baseline
from pyrqa.variants.rp.unthresholded.engine import Engine
from pyrqa.selector import SingleSelector
from pyrqa.variants.rp.radius.test import RPClassicFixedRadiusTestCase, \
    RPCrossFixedRadiusTestCase

from pyrqa.variants.rp.unthresholded.column_materialisation_float import \
    ColumnMaterialisationFloat
from pyrqa.variants.rp.unthresholded.row_materialisation_float import \
    RowMaterialisationFloat

VARIANTS = (ColumnMaterialisationFloat,
            RowMaterialisationFloat)

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2020 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"


class RPClassicUnthresholdedTestCase(RPClassicFixedRadiusTestCase):
    """
    Tests for RP, Classic, Unthresholded.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood: Unthresholded neighbourhood condition.
        """
        cls.neighbourhood = Unthresholded()

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

            self.compare_unthresholded_recurrence_plot_results(result_baseline,
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

                self.compare_unthresholded_recurrence_plot_results(result_baseline,
                                                                   result,
                                                                   variant=variant)


class RPCrossUnthresholdedTestCase(RPCrossFixedRadiusTestCase):
    """
    Tests for RP, Cross, Unthresholded.
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up test.

        :cvar neighbourhood: Unthresholded neighbourhood condition.
        """
        cls.neighbourhood = Unthresholded()

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

            self.compare_unthresholded_recurrence_plot_results(result_baseline,
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

                self.compare_unthresholded_recurrence_plot_results(result_baseline,
                                                                   result,
                                                                   variant=variant)


if __name__ == "__main__":
    unittest.main()
