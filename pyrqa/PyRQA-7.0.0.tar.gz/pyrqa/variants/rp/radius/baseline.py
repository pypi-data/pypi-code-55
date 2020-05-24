#!/usr/bin/env python

"""
Baseline recurrence plot implementation according to the fixed radius and radius corridor neighbourhood condition.
"""

import time

import numpy as np

from pyrqa.scalable_recurrence_analysis import RP
from pyrqa.result import RPResult
from pyrqa.runtimes import MatrixRuntimes, \
    FlavourRuntimesMonolithic

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2020 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"


class Baseline(RP):
    """
    See module description regarding computational properties.
    """
    def __init__(self,
                 settings,
                 verbose=True):
        """
        :param settings: Settings.
        :param verbose: Shall detailed information be printed out during the processing.
        """
        RP.__init__(self,
                    settings=settings,
                    verbose=verbose)

    def reset(self):
        RP.reset(self)

    def create_matrix(self):
        """
        Create matrix
        """
        for index_x in np.arange(self.settings.number_of_vectors_x):

            for index_y in np.arange(self.settings.number_of_vectors_y):

                distance = self.settings.similarity_measure.get_distance_time_series(self.settings.time_series_x.data,
                                                                                     self.settings.time_series_y.data,
                                                                                     self.settings.embedding_dimension,
                                                                                     self.settings.time_series_x.time_delay,
                                                                                     self.settings.time_series_y.time_delay,
                                                                                     index_x,
                                                                                     index_y)

                if self.settings.neighbourhood.contains(distance):
                    self.recurrence_matrix[index_y][index_x] = 1

    def run(self):
        self.reset()

        start = time.time()
        self.create_matrix()
        end = time.time()

        variant_runtimes = FlavourRuntimesMonolithic(execute_computations=end - start)

        number_of_partitions_x = 1
        number_of_partitions_y = 1
        matrix_runtimes = MatrixRuntimes(number_of_partitions_x,
                                         number_of_partitions_y)
        matrix_runtimes.update_index(0,
                                     0,
                                     variant_runtimes)

        result = RPResult(self.settings,
                          matrix_runtimes,
                          recurrence_matrix=self.recurrence_matrix)

        return result
