#!/usr/bin/env python

"""
Join matrices.

Recurrence matrix materialisation: Yes
Similarity value representation: Byte
"""

import numpy as np
import pyopencl as cl

from pyrqa.exceptions import SubMatrixNotProcessedException
from pyrqa.opencl import OpenCL
from pyrqa.runtimes import OperatorRuntimes

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2020 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"


def join_matrices(data_type,
                  sub_matrix,
                  sub_matrix_1_buffer,
                  sub_matrix_2_buffer,
                  device,
                  context,
                  command_queue,
                  kernels,
                  return_sub_matrix_data=False):
    """
    :param data_type: Data type.
    :param sub_matrix: Sub matrix.
    :param sub_matrix_1_buffer: OpenCL buffer for first sub matrix.
    :param sub_matrix_2_buffer: OpenCL buffer for second sub matrix.
    :param device: OpenCL device.
    :param context: OpenCL context.
    :param command_queue: OpenCL command queue.
    :param kernels: OpenCL kernels.
    :param return_sub_matrix_data: Shall the sub matrix data be returned?
    :return: return_sub_matrix_data==False: OpenCL sub matrix buffer, runtimes / return_sub_matrix_data==True: Sub matrix data, runtimes.
    """
    transfer_to_device_events = []
    execute_computations_events = []
    transfer_from_device_events = []

    join_matrices_kernel = kernels[0]

    # Create Buffer for joined matrix
    if sub_matrix.size_byte(data_type) > device.max_mem_alloc_size:
        raise SubMatrixNotProcessedException("Calculation aborted: The size of the sub matrix is too large.")

    joined_sub_matrix_buffer = cl.Buffer(context,
                                         cl.mem_flags.READ_WRITE,
                                         int(sub_matrix.size_byte(data_type)))

    command_queue.finish()

    # Execute join matrices kernel
    kernel_args = [sub_matrix_1_buffer,
                   sub_matrix_2_buffer,
                   np.uint32(sub_matrix.dim_x),
                   joined_sub_matrix_buffer]

    global_work_size = [int(sub_matrix.dim_x + (device.max_work_group_size - (sub_matrix.dim_x % device.max_work_group_size))),
                        int(sub_matrix.dim_y)]

    OpenCL.set_kernel_args(join_matrices_kernel,
                           kernel_args)

    local_work_size = None

    execute_computations_events.append(cl.enqueue_nd_range_kernel(command_queue,
                                                                  join_matrices_kernel,
                                                                  global_work_size,
                                                                  local_work_size))

    command_queue.finish()

    if return_sub_matrix_data:
        # Read from buffer
        sub_matrix.set_empty_data_byte(data_type)

        transfer_from_device_events.append(cl.enqueue_copy(command_queue,
                                                           sub_matrix.data,
                                                           joined_sub_matrix_buffer,
                                                           device_offset=0,
                                                           wait_for=None,
                                                           is_blocking=False))

        command_queue.finish()

    # Determine runtimes
    runtimes = OperatorRuntimes()
    runtimes.transfer_to_device += OpenCL.convert_events_runtime(transfer_to_device_events)
    runtimes.execute_computations += OpenCL.convert_events_runtime(execute_computations_events)
    runtimes.transfer_from_device += OpenCL.convert_events_runtime(transfer_from_device_events)

    return joined_sub_matrix_buffer, \
        runtimes
