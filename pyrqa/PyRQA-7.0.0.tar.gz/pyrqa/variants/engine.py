#!/usr/bin/env python

"""
Execution engine for conducting recurrence quantification analysis using the fixed radius neighbourhood.
"""

import sys
import time

from threading import Thread

from pyrqa.exceptions import SubMatrixNotProcessedException
from pyrqa.opencl import OpenCL
from pyrqa.processing_order import Diagonal
from pyrqa.scalable_recurrence_analysis import SubMatrices, Verbose
from pyrqa.runtimes import MatrixRuntimes, \
    FlavourRuntimesMonolithic
from pyrqa.selector import SingleSelector

if sys.version_info.major == 2:
    import Queue as queue
if sys.version_info.major == 3:
    import queue

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2020 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"


class BaseEngine(SubMatrices,
                 Verbose):
    """
    Execution engine for conducting recurrence quantification analysis (RQA).

    :ivar settings: Settings.
    :ivar verbose: Should additional information should be provided during conducting the computations?
    :ivar edge_length: Default edge length of the sub matrices.
    :ivar processing_order: Processing order of the sub matrices.
    :ivar opencl: OpenCL environment.
    :ivar use_profiling_events_time: Should OpenCL profiling events used for time measurements?
    """

    def __init__(self,
                 settings,
                 verbose=False,
                 edge_length=10240,
                 processing_order=Diagonal,
                 opencl=None,
                 use_profiling_events_time=True):
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
        SubMatrices.__init__(self,
                             settings,
                             edge_length,
                             processing_order)
        Verbose.__init__(self,
                         verbose)
        self.opencl = opencl
        self.use_profiling_events_time = use_profiling_events_time
        self.matrix_runtimes = MatrixRuntimes(self.number_of_partitions_x,
                                              self.number_of_partitions_y)
        self.device_selector = {}

    def validate_opencl(self):
        """
        Validate OpenCL object handed over as a parameter in constructor.
        """
        if not self.opencl:
            self.opencl = OpenCL(verbose=self.verbose)

    def extend_sub_matrix(self,
                          sub_matrix):
        """
        Extend the sub matrix by related data from the global data structures.

        :param sub_matrix: Sub matrix to extend.
        """
        pass

    def get_selector(self,
                     device):
        """
        Get selector for a specific device.

        :param device: OpenCL device.
        :return selector: Selector for the device
        """
        return self.device_selector[device]

    def update_global_data_structures(self,
                                      device,
                                      sub_matrix):
        """
        Update global data structures with values that are computed regarding a specific sub matrix.

        :param device: OpenCL device.
        :param sub_matrix: Sub matrix that has been analysed.
        """
        pass

    def process_sub_matrix_queue(self,
                                 **kwargs):
        """
        Processing of a single sub matrix queue.
        A single queue refers to a specific sub matrix processing level.
        All sub matrices belonging to the same level can be processed simultaneously.

        :param kwargs: Keyword arguments.
        """
        device = kwargs['device']
        sub_matrix_queue = kwargs['sub_matrix_queue']

        while True:
            try:
                # Get sub matrix from queue
                sub_matrix = sub_matrix_queue.get(False)

                # Extend sub matrix
                self.extend_sub_matrix(sub_matrix)

                # Process sub matrix
                sub_matrix_processed = False
                flavour = None
                flavour_runtimes = None

                while not sub_matrix_processed:
                    flavour = self.get_selector(device).get_flavour()

                    try:
                        start_time = time.time()
                        flavour_runtimes = flavour.variant_instance.process_sub_matrix(sub_matrix)
                        end_time = time.time()

                        if not self.use_profiling_events_time:
                            flavour_runtimes = FlavourRuntimesMonolithic(execute_computations=end_time - start_time)

                        sub_matrix_processed = True
                        self.get_selector(device).increment_sub_matrix_count()
                    except SubMatrixNotProcessedException as error:
                        if self.get_selector(device).__class__ == SingleSelector:
                            self.print_out(error)
                            flavour_runtimes = FlavourRuntimesMonolithic()
                            break

                # Update flavour runtimes
                flavour.update_runtimes(sub_matrix,
                                        flavour_runtimes)

                # Update matrix runtimes
                self.matrix_runtimes.update_sub_matrix(sub_matrix,
                                                       flavour_runtimes)

                # Update global data structures
                self.update_global_data_structures(device,
                                                   sub_matrix)

            except queue.Empty:
                break

    def run_single_device(self):
        """
        Perform the computations using only a single OpenCL compute device.
        No separate thread is launched.
        """
        for sub_matrix_queue in self.sub_matrix_queues:
            self.process_sub_matrix_queue(device=self.opencl.devices[0],
                                          sub_matrix_queue=sub_matrix_queue)

    def run_multiple_devices(self):
        """
        Perform the computations using multiple OpenCL compute devices.
        One thread per OpenCL compute device is launched.
        """
        for sub_matrix_queue in self.sub_matrix_queues:
            threads = []

            for device in self.opencl.devices:
                kwargs = {'device': device,
                          'sub_matrix_queue': sub_matrix_queue}

                thread = Thread(target=self.process_sub_matrix_queue,
                                kwargs=kwargs)

                thread.start()

                threads.append(thread)

            for thread in threads:
                thread.join()

    def run_device_selection(self):
        """
        Perform the computations based on the devices specified in the OpenCL environment.
        """
        if not self.opencl.devices:
            print('No device specified!')
            return 0
        elif len(self.opencl.devices) == 1:
            self.run_single_device()
        elif len(self.opencl.devices) > 1:
            self.run_multiple_devices()

    def run(self):
        """
        Perform the computations.
        """
        pass
