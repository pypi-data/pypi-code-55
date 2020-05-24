#!/usr/bin/env python

"""
Engine for conducting recurrence quantification analysis based on the fixed radius and radius corridor neighbourhood condition.
"""

import copy
import numpy as np

from pyrqa.processing_order import Diagonal
from pyrqa.scalable_recurrence_analysis import RQA, \
    Carryover
from pyrqa.result import RQAResult
from pyrqa.selector import SingleSelector
from pyrqa.variants.engine import BaseEngine
from pyrqa.variants.rqa.radius.column_materialisation_byte_no_recycling import ColumnMaterialisationByteNoRecycling

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2020 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"


class Engine(BaseEngine,
             RQA,
             Carryover):
    """
    Engine for conducting recurrence quantification analysis (RQA).

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
                 variants=(ColumnMaterialisationByteNoRecycling,),
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
        RQA.__init__(self,
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

        self.device_vertical_frequency_distribution = {}
        self.device_white_vertical_frequency_distribution = {}
        self.device_diagonal_frequency_distribution = {}

        for device in self.opencl.devices:
            self.device_selector[device] = copy.deepcopy(self.selector)
            self.device_selector[device].setup(device,
                                               self.settings,
                                               self.opencl,
                                               self.variants,
                                               self.variants_kwargs)

            self.device_vertical_frequency_distribution[device] = self.get_empty_global_frequency_distribution()
            self.device_white_vertical_frequency_distribution[device] = self.get_empty_global_frequency_distribution()
            self.device_diagonal_frequency_distribution[device] = self.get_empty_global_frequency_distribution()

    def reset(self):
        """
        Reset the global data structures.
        """
        RQA.reset(self)
        Carryover.reset(self)

        self.__initialise()

    def get_empty_local_frequency_distribution(self):
        """
        Get empty local frequency distribution.

        :returns: Empty local frequency distribution.
        """
        return np.zeros(self.settings.max_number_of_vectors,
                        dtype=np.uint32)

    @staticmethod
    def recurrence_points_start(sub_matrix):
        """
        Start index of the sub matrix specific segment within the global recurrence point array.

        :param sub_matrix: Sub matrix.
        :return: Recurrence points start.
        """
        return sub_matrix.start_x

    @staticmethod
    def recurrence_points_end(sub_matrix):
        """
        End index of the sub matrix specific segment within the global recurrence point array.

        :param sub_matrix: Sub matrix.
        :return: Recurrence points end.
        """
        return sub_matrix.start_x + sub_matrix.dim_x

    def get_recurrence_points(self,
                              sub_matrix):
        """
        Get the sub matrix specific segment within the global recurrence points array.

        :param sub_matrix: Sub matrix.
        :returns: Sub array of the global recurrence points array.
        """
        start = self.recurrence_points_start(sub_matrix)
        end = self.recurrence_points_end(sub_matrix)

        return self.recurrence_points[start:end]

    def set_recurrence_points(self,
                              sub_matrix):
        """
        Set the sub matrix specific segment within the global recurrence points array.

        :param sub_matrix: Sub matrix.
        """
        start = self.recurrence_points_start(sub_matrix)
        end = self.recurrence_points_end(sub_matrix)

        self.recurrence_points[start:end] = sub_matrix.recurrence_points

    @staticmethod
    def vertical_length_carryover_start(sub_matrix):
        """
        Start index of the sub matrix specific segment within the global vertical length carryover array.

        :param sub_matrix: Sub matrix.
        :return: Vertical length carryover start.
        """
        return sub_matrix.start_x

    @staticmethod
    def vertical_length_carryover_end(sub_matrix):
        """
        End index of the sub matrix specific segment within the global vertical length carryover array.

        :param sub_matrix: Sub matrix.
        :return: Vertical length carryover end.
        """
        return sub_matrix.start_x + sub_matrix.dim_x

    def get_vertical_length_carryover(self,
                                      sub_matrix):
        """
        Get the sub matrix specific segment within the global vertical length carryover array.

        :param sub_matrix: Sub matrix.
        :returns: Sub array of the global vertical length carryover array.
        """
        start = self.vertical_length_carryover_start(sub_matrix)
        end = self.vertical_length_carryover_end(sub_matrix)

        return self.vertical_length_carryover[start:end]

    def set_vertical_length_carryover(self,
                                      sub_matrix):
        """
        Set the sub matrix specific segment within the global vertical length carryover array.

        :param sub_matrix: Sub matrix
        """
        start = self.vertical_length_carryover_start(sub_matrix)
        end = self.vertical_length_carryover_end(sub_matrix)

        self.vertical_length_carryover[start:end] = sub_matrix.vertical_length_carryover

    @staticmethod
    def white_vertical_length_carryover_start(sub_matrix):
        """
        Start index of the sub matrix specific segment of the global white vertical length carryover array.

        :param sub_matrix: Sub matrix.
        :return: White vertical length carryover start.
        """
        return sub_matrix.start_x

    @staticmethod
    def white_vertical_length_carryover_end(sub_matrix):
        """
        End index of the sub matrix specific segment of the global white vertical length carryover array.

        :param sub_matrix: Sub matrix.
        :return: White vertical length carryover end.
        """
        return sub_matrix.start_x + sub_matrix.dim_x

    def get_white_vertical_length_carryover(self,
                                            sub_matrix):
        """
        Get the sub matrix specific segment of the global white vertical length carryover array.

        :param sub_matrix: Sub matrix.
        :returns: Sub array of the global white vertical length carryover array.
        """
        start = self.white_vertical_length_carryover_start(sub_matrix)
        end = self.white_vertical_length_carryover_end(sub_matrix)

        return self.white_vertical_length_carryover[start:end]

    def set_white_vertical_length_carryover(self,
                                            sub_matrix):
        """
        Set the sub matrix specific segment of the global white vertical length carryover array.

        :param sub_matrix: Sub matrix.
        """
        start = self.white_vertical_length_carryover_start(sub_matrix)
        end = self.white_vertical_length_carryover_end(sub_matrix)

        self.white_vertical_length_carryover[start:end] = sub_matrix.white_vertical_length_carryover

    def diagonal_length_carryover_start(self,
                                        sub_matrix):
        """
        Start index of the sub matrix specific segment of the global diagonal length carryover array.

        :param sub_matrix: Sub matrix.
        :return: Diagonal length carryover start.
        """
        if self.settings.is_matrix_symmetric:
            if sub_matrix.partition_index_x < sub_matrix.partition_index_y:
                return sub_matrix.start_y - (sub_matrix.start_x + sub_matrix.dim_x)

            return sub_matrix.start_x - sub_matrix.start_y

        return (self.settings.number_of_vectors_y - 1) + (sub_matrix.start_x - sub_matrix.dim_y + 1) - sub_matrix.start_y

    def diagonal_length_carryover_end(self,
                                      sub_matrix):
        """
        End index of the sub matrix specific segment of the global diagonal length carryover array.

        :param sub_matrix: Sub matrix
        :return: Diagonal length carryover end.
        """
        if self.settings.is_matrix_symmetric:
            return self.diagonal_length_carryover_start(sub_matrix) + sub_matrix.dim_x

        return self.diagonal_length_carryover_start(sub_matrix) + (sub_matrix.dim_x + sub_matrix.dim_y - 1)

    def get_diagonal_length_carryover(self,
                                      sub_matrix):
        """
        Get the sub matrix specific segment of the global diagonal length carryover array.

        :param sub_matrix: Sub matrix.
        :returns: Sub array of global diagonal length carryover array.
        """
        start = self.diagonal_length_carryover_start(sub_matrix)
        end = self.diagonal_length_carryover_end(sub_matrix)

        return self.diagonal_length_carryover[start:end]

    def set_diagonal_length_carryover(self,
                                      sub_matrix):
        """
        Set the sub matrix specific segment of the global diagonal length carryover array.

        :param sub_matrix: Sub matrix.
        """
        start = self.diagonal_length_carryover_start(sub_matrix)
        end = self.diagonal_length_carryover_end(sub_matrix)

        self.diagonal_length_carryover[start:end] = sub_matrix.diagonal_length_carryover

    def post_process_length_carryovers(self):
        """
        Post process length carryover buffers.
        """
        for line_length in self.diagonal_length_carryover[self.diagonal_length_carryover > 0]:
            self.diagonal_frequency_distribution[line_length - 1] += 1

        for line_length in self.vertical_length_carryover[self.vertical_length_carryover > 0]:
            self.vertical_frequency_distribution[line_length - 1] += 1

        for line_length in self.white_vertical_length_carryover[self.white_vertical_length_carryover > 0]:
            self.white_vertical_frequency_distribution[line_length - 1] += 1

    @staticmethod
    def get_diagonal_offset(sub_matrix):
        """
        Get diagonal offset.

        :param sub_matrix: Sub matrix.
        :return: Diagonal offset.
        """
        if sub_matrix.partition_index_x < sub_matrix.partition_index_y:
            return 1

        return 0

    def extend_sub_matrix(self,
                          sub_matrix):
        """
        Extend the sub matrix by related data from the global data structures.

        :param sub_matrix: Sub matrix to extend.
        """
        sub_matrix.recurrence_points = self.get_recurrence_points(sub_matrix)

        sub_matrix.vertical_length_carryover = self.get_vertical_length_carryover(sub_matrix)
        sub_matrix.white_vertical_length_carryover = self.get_white_vertical_length_carryover(sub_matrix)
        sub_matrix.diagonal_length_carryover = self.get_diagonal_length_carryover(sub_matrix)

        sub_matrix.vertical_frequency_distribution = self.get_empty_local_frequency_distribution()
        sub_matrix.white_vertical_frequency_distribution = self.get_empty_local_frequency_distribution()
        sub_matrix.diagonal_frequency_distribution = self.get_empty_local_frequency_distribution()

    def update_global_data_structures(self,
                                      device,
                                      sub_matrix):
        self.set_recurrence_points(sub_matrix)

        self.set_vertical_length_carryover(sub_matrix)
        self.set_white_vertical_length_carryover(sub_matrix)
        self.set_diagonal_length_carryover(sub_matrix)

        self.device_vertical_frequency_distribution[device] += sub_matrix.vertical_frequency_distribution
        self.device_white_vertical_frequency_distribution[device] += sub_matrix.white_vertical_frequency_distribution
        self.device_diagonal_frequency_distribution[device] += sub_matrix.diagonal_frequency_distribution

    def run(self):
        self.reset()

        self.run_device_selection()

        self.post_process_length_carryovers()

        for device in self.opencl.devices:
            self.diagonal_frequency_distribution += self.device_diagonal_frequency_distribution[device]
            self.vertical_frequency_distribution += self.device_vertical_frequency_distribution[device]
            self.white_vertical_frequency_distribution += self.device_white_vertical_frequency_distribution[device]

        if self.settings.is_matrix_symmetric:
            self.extent_diagonal_frequency_distribution()

        return RQAResult(self.settings,
                         self.matrix_runtimes,
                         recurrence_points=self.recurrence_points,
                         diagonal_frequency_distribution=self.diagonal_frequency_distribution,
                         vertical_frequency_distribution=self.vertical_frequency_distribution,
                         white_vertical_frequency_distribution=self.white_vertical_frequency_distribution)
