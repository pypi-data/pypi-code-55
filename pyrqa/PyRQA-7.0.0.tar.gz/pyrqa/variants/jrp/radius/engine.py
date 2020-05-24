#!/usr/bin/env python

"""
Engine for creating joined recurrence plots.
"""

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2020 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"

from pyrqa.variants.rp.radius.engine import Engine as EngineRadius
from pyrqa.variants.jrp.radius.column_materialisation_byte import ColumnMaterialisationByte
from pyrqa.processing_order import Diagonal
from pyrqa.selector import SingleSelector


class Engine(EngineRadius):
    """
    Engine for creating joint recurrence plots (URP).

    :ivar settings: Settings.
    :ivar opencl: OpenCL environment.
    :ivar verbose: Should additional information should be provided during conducting the computations?
    :ivar edge_length: Default edge length of the sub matrices.
    :ivar processing_order: Processing order of the sub matrices.
    :ivar selector: Flavour selection approach.
    :ivar variants: List of RQA implementation variants.
    :ivar variants_kwargs: Dictionary of RQA implementation variants keyword arguments.
    :ivar use_profiling_events_time: Should OpenCL profiling events used for time measurements?
    """
    def __init__(self,
                 settings,
                 edge_length=10240,
                 processing_order=Diagonal,
                 verbose=False,
                 opencl=None,
                 use_profiling_events_time=True,
                 selector=SingleSelector(loop_unroll_factors=(1,)),
                 variants=(ColumnMaterialisationByte,),
                 variants_kwargs=None):
        """
        :param settings: Settings.
        :param edge_length: Default edge length of the sub matrices.
        :param processing_order: Processing order of the sub matrices.
        :param verbose: Should additional information should be provided during conducting the computations?
        :param opencl: OpenCL environment.
        :param use_profiling_events_time: Should OpenCL profiling events used for time measurements?
        :param selector: Flavour selection approach.
        :param variants: List of RQA implementation variants.
        :param variants_kwargs: Dictionary of RQA implementation variants keyword arguments.
        """
        EngineRadius.__init__(self,
                              settings,
                              edge_length=edge_length,
                              processing_order=processing_order,
                              verbose=verbose,
                              opencl=opencl,
                              use_profiling_events_time=use_profiling_events_time,
                              selector=selector,
                              variants=variants,
                              variants_kwargs=variants_kwargs)
