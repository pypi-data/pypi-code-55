#!/usr/bin/env python

"""
Engine for creating recurrence plots based on the fixed radius and radius corridor neighbourhood condition.
"""

import copy

from pyrqa.scalable_recurrence_analysis import RP, \
    Carryover
from pyrqa.variants.engine import BaseEngine
from pyrqa.variants.rp.radius.column_materialisation_byte import ColumnMaterialisationByte
from pyrqa.processing_order import Diagonal
from pyrqa.result import RPResult
from pyrqa.selector import SingleSelector

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2020 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"


class Engine(BaseEngine,
             RP,
             Carryover):
    """
    Engine for creating recurrence plots (RP).

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
        BaseEngine.__init__(self,
                            settings,
                            edge_length=edge_length,
                            processing_order=processing_order,
                            verbose=verbose,
                            opencl=opencl,
                            use_profiling_events_time=use_profiling_events_time)
        RP.__init__(self,
                    settings,
                    verbose)
        Carryover.__init__(self,
                           settings,
                           verbose)

        self.selector = selector
        self.variants = variants
        self.variants_kwargs = variants_kwargs if variants_kwargs else {}

        self.__initialise()

    def __initialise(self):
        """
        Initialise the compute device-specific global data structures.
        """
        self.validate_opencl()

        self.device_selector = {}

        for device in self.opencl.devices:
            self.device_selector[device] = copy.deepcopy(self.selector)
            self.device_selector[device].setup(device,
                                               self.settings,
                                               self.opencl,
                                               self.variants,
                                               self.variants_kwargs)

    def reset(self):
        """
        Reset the global data structures.
        """
        RP.reset(self)
        Carryover.reset(self)

        self.__initialise()

    def set_sub_matrix_data(self,
                            sub_matrix):
        """
        Set sub matrix data in global recurrence matrix.

        :param sub_matrix: Sub matrix.
        """
        sub_matrix.data = sub_matrix.data.reshape(sub_matrix.dim_y, sub_matrix.dim_x)
        self.recurrence_matrix[sub_matrix.start_y:sub_matrix.start_y + sub_matrix.dim_y, sub_matrix.start_x:sub_matrix.start_x + sub_matrix.dim_x] = sub_matrix.data

    def update_global_data_structures(self,
                                      device,
                                      sub_matrix):
        self.set_sub_matrix_data(sub_matrix)

    def run(self):
        self.reset()

        self.run_device_selection()

        return RPResult(self.settings,
                        self.matrix_runtimes,
                        recurrence_matrix=self.recurrence_matrix)