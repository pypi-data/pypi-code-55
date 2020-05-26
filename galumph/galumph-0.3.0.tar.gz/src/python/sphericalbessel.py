# SPDX-FileCopyrightText: 2016 European Molecular Biology Laboratory (EMBL)
# SPDX-FileCopyrightText: 2017-2019 Christopher Kerr
#
# SPDX-License-Identifier: LGPL-3.0-or-later

__copyright__ = "European Molecular Biology Laboratory (EMBL)"
__license__ = "LGPLv3+"

import numpy as np
import pyopencl as cl
from pyopencl import array as cl_array

from .util import ClProgram, LMAXMixin, optional_out_array


class SphericalBessel(LMAXMixin, ClProgram):
    """Calculate an array of spherical Bessel functions

    Calculates the spherical Bessel function of the first kind j_L(r*s)
    for all L up to and including LMAX.
    The s array is assumed to be the same for all invocations and is passed
    to the __init__ function; r is the only parameter which varies between
    invocations."""

    def __init__(self, LMAX, s, worksize=64, natwork=16, context=None):
        """Set up the arrays, kernels etc for the spherical Bessel function

        s must be a one-dimensional array whose size is a multiple of
        the worksize parameter. LMAX should be a positive integer."""
        assert LMAX >= 0
        self.LMAX = LMAX
        s = np.asanyarray(s)
        NS, = s.shape
        assert NS > 0
        assert np.all(s >= 0)
        self.NS = NS
        assert worksize > 0
        assert NS % worksize == 0
        self.worksize = worksize
        assert natwork > 0
        self.natwork = natwork
        super(SphericalBessel, self).__init__(
            filename='spherical-bessel.cl',
            options=["-DWORKSIZE=%d" % worksize],
            context=context)
        context = self.context

        self.s_host = np.array(s, dtype=np.float32)
        with cl.CommandQueue(context) as queue:
            self.s_dev = cl_array.to_device(queue, self.s_host)

    @optional_out_array(shape=('LMAX1', 'NS'), dtype='f4')
    def __call__(self, r, queue=None, out=None):
        """Calculate the spherical Bessel function j_L(r*s) for L<=LMAX

        The calculation is done asynchronously, the returned OpenCL
        event object can be used to wait for the result."""
        assert r >= 0
        NS = self.NS
        worksize = self.worksize

        ev = self.program.jsph(queue,
                               (NS,),
                               (worksize,),
                               np.uint32(self.LMAX),
                               np.float32(r),
                               self.s_dev.data,
                               out.data)

        return ev, out

    @optional_out_array(shape=('natwork', 'LMAX1', 'NS'), dtype='f4')
    def batch(self, r, queue=None, out=None):
        """Batch spherical Bessel function for an array of r values."""
        r = np.array(r, dtype=np.float32)
        assert np.all(r >= 0)
        NS = self.NS
        worksize = self.worksize
        nAt = np.size(r)
        assert nAt > 0
        assert nAt <= self.natwork

        r_dev = cl_array.to_device(queue, r)
        ev = self.program.jsph_batch(queue,
                                     (NS, nAt),
                                     (worksize, 1),
                                     np.uint32(self.LMAX),
                                     r_dev.data,
                                     self.s_dev.data,
                                     out.data)

        return ev, out

    @optional_out_array(shape=('LMAX1', 'NS'), dtype='f4')
    def integral(self, r, queue=None, out=None):
        """Calculate the spherical Bessel integral \\Integral{0}{r} j_L(r'*s) dr' for L<=LMAX

        The calculation is done asynchronously, the returned OpenCL
        event object can be used to wait for the result.
        """
        assert r >= 0
        NS = self.NS
        LMAX = self.LMAX
        LMAX1 = self.LMAX1
        s_dev = self.s_dev
        worksize = self.worksize

        ev1 = self.program.jsph(queue,
                                (NS, 1),
                                (worksize, 1),
                                np.uint32(LMAX),
                                np.float32(r),
                                s_dev.data,
                                out.data)

        localJL = cl.LocalMemory(4*NS)
        ev = self.program.jsph_integral(queue,
                                        (worksize, LMAX1),
                                        (worksize, 1),
                                        np.uint32(NS),
                                        np.float32(r),
                                        s_dev.data,
                                        out.data,
                                        localJL,
                                        wait_for=(ev1,))

        return ev, out
