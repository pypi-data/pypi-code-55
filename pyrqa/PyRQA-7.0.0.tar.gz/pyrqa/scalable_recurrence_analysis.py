#!/usr/bin/env python

"""
Recurrence analysis
"""

import math
import sys

import numpy as np

from pyrqa.analysis_type import Joint
from pyrqa.neighbourhood import Unthresholded
from pyrqa.processing_order import Bulk, \
    Diagonal, \
    Vertical
from pyrqa.utils import SettableSettings, \
    Verbose

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2020 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"


if sys.version_info.major == 2:
    import Queue as queue
if sys.version_info.major == 3:
    import queue


class RP(SettableSettings,
         Verbose):
    """
    Recurrence Plot.

    :ivar recurrence_matrix: Recurrence matrix.
    """
    def __init__(self,
                 settings,
                 verbose):
        SettableSettings.__init__(self,
                                  settings)
        Verbose.__init__(self,
                         verbose)

        self.__initialise()

    def __initialise(self):
        """
        Initialise the instance variables.
        """
        if self.settings.analysis_type is not Joint and isinstance(self.settings.neighbourhood, Unthresholded):
            self.recurrence_matrix = np.zeros((self.settings.number_of_vectors_y,
                                               self.settings.number_of_vectors_x),
                                              dtype=self.settings.dtype)
        else:
            self.recurrence_matrix = np.zeros((self.settings.number_of_vectors_y,
                                               self.settings.number_of_vectors_x),
                                              dtype=np.uint8)

    def reset(self):
        """
        Reset the instance variables.
        """
        self.__initialise()


class RQA(SettableSettings,
          Verbose):
    """
    Recurrence quantification analysis.

    :ivar recurrence_points: Local recurrence points.
    :ivar diagonal_frequency_distribution: Frequency distribution of diagonal lines.
    :ivar vertical_frequency_distribution: Frequency distribution of vertical lines.
    :ivar white_vertical_frequency_distribution: Frequency distribution of white vertical lines.
    """
    def __init__(self,
                 settings,
                 verbose):
        SettableSettings.__init__(self,
                                  settings)
        Verbose.__init__(self,
                         verbose)

        self.__initialise()

    def __initialise(self):
        """
        Initialise the instance variables.
        """
        self.recurrence_points = self.get_empty_recurrence_points()
        self.diagonal_frequency_distribution = self.get_empty_global_frequency_distribution()
        self.vertical_frequency_distribution = self.get_empty_global_frequency_distribution()
        self.white_vertical_frequency_distribution = self.get_empty_global_frequency_distribution()

    def reset(self):
        """
        Reset the instance variables.
        """
        self.__initialise()

    def get_empty_recurrence_points(self):
        """
        Get empty recurrence points.

        :return: Empty recurrence points.
        :rtype: 1D array.
        """
        size = self.settings.number_of_vectors_x if \
            self.settings.number_of_vectors_x > self.settings.number_of_vectors_y else \
            self.settings.number_of_vectors_y

        return np.zeros(size,
                        dtype=np.uint32)

    def get_empty_global_frequency_distribution(self):
        """
        Get empty frequency distribution.

        :returns: Empty global frequency distribution.
        :rtype: 1D array.
        """
        return np.zeros(self.settings.max_number_of_vectors,
                        dtype=np.uint64)

    def extent_diagonal_frequency_distribution(self):
        """
        Extent the content of the diagonal frequency distribution.
        """
        if self.settings.is_matrix_symmetric:
            self.diagonal_frequency_distribution += self.diagonal_frequency_distribution
            if not self.settings.theiler_corrector:
                self.diagonal_frequency_distribution[-1] -= 1


class SubMatrix(object):
    """
    Sub matrix.

    :ivar partition_index_x: X index of sub matrix in partitioned global recurrence matrix.
    :ivar partition_index_y: Y index of sub matrix in partitioned global recurrence matrix.
    :ivar start_x: Global index for first vector (X dimension).
    :ivar start_y: Global index for first vector (Y dimension).
    :ivar dim_x: Number of vectors (X dimension).
    :ivar dim_y: Number of vectors (Y dimension).
    """
    def __init__(self,
                 partition_index_x,
                 partition_index_y,
                 start_x,
                 start_y,
                 dim_x,
                 dim_y):
        self.partition_index_x = partition_index_x
        self.partition_index_y = partition_index_y
        self.start_x = start_x
        self.start_y = start_y
        self.dim_x = dim_x
        self.dim_y = dim_y

        self.data = None

    @property
    def diagonal_offset(self):
        """
        Offset for detecting diagonal lines.
        """
        if self.partition_index_x < self.partition_index_y:
            return 1

        return 0

    @property
    def elements(self):
        """
        Number of matrix elements.
        """
        return self.dim_x * self.dim_y

    @staticmethod
    def bits_per_element(data_type):
        """
        Bits per element.

        :param data_type: Data type.
        :return: Bits per element.
        """
        return np.dtype(data_type).itemsize * 8

    def elements_byte(self):
        """
        Number of elements based on byte representation.
        """
        return self.dim_x * self.dim_y

    def elements_bit(self, data_type):
        """
        Number of elements based on bit representation.

        :param data_type: Data type.
        :return: Number of elements.
        """
        return self.dim_x * math.ceil(float(self.dim_y) / self.bits_per_element(data_type))

    def size_byte(self, data_type):
        """
        Size based on byte representation.

        :param data_type: Data type.
        :return: Size.
        """
        return self.elements_byte() * np.dtype(data_type).itemsize

    def size_bit(self, data_type):
        """
        Size based on bit representation.

        :param data_type: Data type.
        :return: Size.
        """
        return self.elements_bit(data_type) * np.dtype(data_type).itemsize

    def set_empty_data_byte(self, data_type):
        """
        Set empty data based on byte representation.

        :param data_type: Data type.
        :return: Empty data.
        """
        self.data = np.zeros(self.elements_byte(), dtype=data_type)

    def set_empty_data_bit(self, data_type):
        """
        Set empty data based on bit representation.

        :param data_type: Data type.
        :return: Empty data.
        """
        self.data = np.zeros(self.elements_bit(data_type), dtype=data_type)

    def __str__(self):
        return "Sub Matrix\n" \
               "----------\n" \
               "\n" \
               "Partition Index X: %d\n" \
               "Partition Index Y: %d\n" \
               "Start X: %d\n" \
               "Start Y: %d\n"\
               "Dim X: %d\n" \
               "Dim Y: %d\n" % (self.partition_index_x,
                                self.partition_index_y,
                                self.start_y,
                                self.start_x,
                                self.dim_x,
                                self.dim_y)


class SubMatrices(SettableSettings):
    """
    Processing of sub matrices.

    :ivar edge_length: Inital edge length of sub matrix.
    :ivar processing_order: Processing order of the sub matrices.
    """
    def __init__(self,
                 settings,
                 edge_length,
                 processing_order):

        SettableSettings.__init__(self, settings)

        if edge_length:
            self.edge_length = edge_length
        else:
            self.edge_length = self.settings.max_number_of_vectors

        self.processing_order = processing_order

        self.sub_matrix_queues = None
        self.number_of_partitions_x = None
        self.number_of_partitions_y = None

        self.__initialise()

    def __initialise(self):
        """
        Initialise the instance variables.
        """
        self.create_sub_matrices()

    def reset(self):
        """
        Reset the instance variables.
        """
        self.__initialise()

    def create_sub_matrices(self):
        """
        Create sub matrices according to the given processing order.
        Each task queue represents an execution level.
        """
        max_edge_length = math.pow(2, 16) - 1
        self.edge_length = max_edge_length if self.edge_length > max_edge_length else self.edge_length

        self.number_of_partitions_x = int(
            math.ceil(float(self.settings.number_of_vectors_x) / self.edge_length))
        self.number_of_partitions_y = int(
            math.ceil(float(self.settings.number_of_vectors_y) / self.edge_length))

        self.sub_matrix_queues = []

        for partition_index_x in np.arange(self.number_of_partitions_x):

            for partition_index_y in np.arange(self.number_of_partitions_y):

                if partition_index_x == self.number_of_partitions_x - 1:
                    dim_x = self.settings.number_of_vectors_x - partition_index_x * self.edge_length
                    start_x = partition_index_x * self.edge_length
                else:
                    dim_x = self.edge_length
                    start_x = partition_index_x * dim_x

                if partition_index_y == self.number_of_partitions_y - 1:
                    dim_y = self.settings.number_of_vectors_y - partition_index_y * self.edge_length
                    start_y = partition_index_y * self.edge_length
                else:
                    dim_y = self.edge_length
                    start_y = partition_index_y * dim_y

                sub_matrix = SubMatrix(partition_index_x,
                                       partition_index_y,
                                       start_x,
                                       start_y,
                                       dim_x,
                                       dim_y)

                queue_index = None
                if self.processing_order == Diagonal:
                    queue_index = partition_index_x + partition_index_y

                elif self.processing_order == Vertical:
                    queue_index = partition_index_y

                elif self.processing_order == Bulk:
                    queue_index = 0

                if len(self.sub_matrix_queues) <= queue_index:
                    self.sub_matrix_queues.append(queue.Queue())

                self.sub_matrix_queues[queue_index].put(sub_matrix)


class Carryover(SettableSettings,
                Verbose):
    """
    Perform recurrence quantification analysis based on multiple sub matrices

    :ivar diagonal_length_carryover: Diagonal line length carryover.
    :ivar vertical_length_carryover: Vertical line length carryover.
    :ivar white_vertical_length_carryover: White vertical line length carryover.
    """
    def __init__(self, settings, verbose):
        SettableSettings.__init__(self, settings)
        Verbose.__init__(self, verbose)

        self.__initialise()

    def __initialise(self):
        """
        Initialise the instance variables.
        """
        if self.settings.is_matrix_symmetric:
            self.diagonal_length_carryover = np.zeros(
                self.settings.number_of_vectors_x,
                dtype=np.uint32)
        else:
            self.diagonal_length_carryover = np.zeros(
                self.settings.number_of_vectors_x + self.settings.number_of_vectors_y - 1,
                dtype=np.uint32)

        self.vertical_length_carryover = np.zeros(self.settings.number_of_vectors_x,
                                                  dtype=np.uint32)

        self.white_vertical_length_carryover = np.zeros(self.settings.number_of_vectors_x,
                                                        dtype=np.uint32)

    def reset(self):
        """
        Reset the instance variables.
        """
        self.__initialise()
