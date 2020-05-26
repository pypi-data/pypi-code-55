# SPDX-FileCopyrightText: 2016 European Molecular Biology Laboratory (EMBL)
# SPDX-FileCopyrightText: 2017-2018 Christopher Kerr
#
# SPDX-License-Identifier: LGPL-3.0-or-later

__copyright__ = "Christopher Kerr"
__license__ = "LGPLv3+"

import numpy as np
from pyopencl import array as cl_array

from .util import ClProgram, with_some_queue


class Intensity(ClProgram):
    """Functions for calculating the scattering intensity from Alm arrays."""

    def __init__(self, worksize, context=None):
        self.worksize = worksize
        super(Intensity, self).__init__('intensity.cl',
                                        options=['-DWORKSIZE=%d' % worksize],
                                        context=context)

    @with_some_queue
    def __call__(self, alm, queue=None):
        """Calculate the scattering intensity from the given ALM array.

        The intensity at each S point is the sum of the squared magnitude of
        all [L,M] indices at that S point.
        """
        assert alm.context == self.context
        assert (alm.NS % self.worksize) == 0
        assert queue is not None
        NS = alm.NS
        LMAX = alm.LMAX
        worksize = self.worksize

        int_dev = cl_array.empty(queue, (NS,), dtype='f4')

        ev = self.program.alm_intensity(queue,
                                        (NS,),
                                        (worksize,),
                                        np.uint32(LMAX),
                                        alm.data,
                                        int_dev.data)
        return ev, int_dev

    @with_some_queue
    def cross(self, alm, blm, queue=None):
        """Calculate the cross scattering between ALM and BLM."""
        assert alm.context == self.context
        assert blm.context == self.context
        assert (alm.NS % self.worksize) == 0
        assert blm.NS == alm.NS
        assert queue is not None
        NS = alm.NS
        LMAX = min(alm.LMAX, blm.LMAX)
        worksize = self.worksize

        int_dev = cl_array.empty(queue, (NS,), dtype='f4')

        ev = self.program.alm_cross(queue,
                                    (NS,),
                                    (worksize,),
                                    np.uint32(LMAX),
                                    alm.data,
                                    blm.data,
                                    int_dev.data)
        return ev, int_dev
