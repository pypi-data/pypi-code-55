# SPDX-FileCopyrightText: 2018 Christopher Kerr
#
# SPDX-License-Identifier: LGPL-3.0-or-later

__copyright__ = "Christopher Kerr"
__license__ = "LGPLv3+"

import numpy as np
import pyopencl as cl
import pyopencl.array as cl_array

from .almarray import AlmArray
from .sphericalbessel import SphericalBessel
from .util import ClProgram, LMAXMixin, check_array, with_some_queue
from .gaunt import shzmat


class PackedLMKPMixin(LMAXMixin):
    """Utility functions for packed [L,M,K,P] arrays."""

    @property
    def NLMKP(self):
        """Total number of points in the packed array."""
        return (self.LMAX+1) * (self.LMAX+2)**2 * (self.LMAX+3) // 12


class AlmShiftZ(PackedLMKPMixin, ClProgram):
    """OpenCL kernel for translating ALM arrays along the Z axis."""

    def __init__(self, LMAX, NSWORK, s, dlmkp=None, context=None):
        """Compile the kernel."""
        self.context = context
        self.LMAX = LMAX
        self.NS = len(s)
        self.s = s
        # TODO work out a default value for NSWORK so the user does not have to set it
        self.NSWORK = NSWORK
        assert LMAX >= 0
        assert self.NS > 0
        assert self.NSWORK > 0
        assert self.NS % self.NSWORK == 0

        if dlmkp is None:
            dlmkp = shzmat(LMAX)
        check_array(dlmkp, (self.NLMKP,), exact=False)

        super(AlmShiftZ, self).__init__(
            filename='translate-alm.cl',
            options=["-DLMAX1=%d" % self.LMAX1, "-DNSWORK=%d" % NSWORK],
            context=context)

        # Copy the dlmkp array to the device if it is not already a device array
        if isinstance(dlmkp, cl_array.Array):
            assert dlmkp.context == self.context
            assert dlmkp.dtype == np.dtype('f4')
            self.dlmkp = dlmkp
        else:
            dlmkp = np.asarray(dlmkp, dtype='f4')
            with cl.CommandQueue(self.context) as queue:
                self.dlmkp = cl_array.to_device(queue, dlmkp)

        self.sphbes = SphericalBessel(
            2*LMAX, s,
            # TODO the SphericalBessel kernel can use a larger work size
            worksize=NSWORK,
            natwork=1,
            context=self.context,
        )

    @with_some_queue
    def __call__(self, alm, u, queue=None):
        """Shift Alm by u along the z axis and return as Blm."""
        assert alm.context == self.context
        assert alm.LMAX == self.LMAX
        assert alm.NS == self.NS
        assert queue is not None
        if (u < 0):
            # TODO implement negative shifts
            raise NotImplementedError('Negative z-shifts not yet supported.')
        LMAX = self.LMAX
        LMAX1 = self.LMAX1
        NS = self.NS
        NSWORK = self.NSWORK

        ev_j, jp = self.sphbes(u, queue=queue)

        blm = AlmArray(queue, LMAX, NS)
        alm_local = cl.LocalMemory(LMAX1*NSWORK * 8)
        blm_local = cl.LocalMemory(LMAX1*NSWORK * 8)
        dlmkp_local = cl.LocalMemory(LMAX1*LMAX1 * 4)
        jp_local = cl.LocalMemory((2*LMAX + 1)*NSWORK * 4)

        ev = self.program.translate_alm(queue,
                                        (LMAX1, LMAX1, NS),
                                        (LMAX1, 1, NSWORK),
                                        alm.data,
                                        blm.data,
                                        self.dlmkp.data,
                                        jp.data,
                                        alm_local,
                                        blm_local,
                                        dlmkp_local,
                                        jp_local,
                                        wait_for=(ev_j,))
        return ev, blm
