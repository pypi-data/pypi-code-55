# SPDX-FileCopyrightText: 2018 Christopher Kerr
#
# SPDX-License-Identifier: LGPL-3.0-or-later

__copyright__ = "Christopher Kerr"
__license__ = "LGPLv3+"

import numpy as np
import pyopencl as cl

from .almarray import AlmArray
from .util import ClProgram, PackedLMMixin, optional_out_array, with_some_queue


def _restrict_angle(theta):
    """Restrict an angle to the range (-pi, pi)."""
    if abs(theta) <= np.pi:
        return theta
    return (theta - np.pi) % (2 * np.pi) - np.pi


class PackedLM1M2Mixin(PackedLMMixin):
    """Mixin with utility methods for packed [L, M1, M2] arrays.

    0 <= L <= LMAX
    -L <= M1 <= L
    0 <= M2 <= L
    """

    @staticmethod
    def indexM1M2(L, M1, M2):
        """Index into a [M1, M2] slice of a packed [L, M1, M2] array."""
        assert L >= 0
        assert abs(M1) <= L
        assert M2 >= 0
        assert M2 <= L
        return (L+M1) * (L+1) + M2

    @staticmethod
    def indexLM1M2(L, M1=0, M2=0):
        """Index into a packed [L, M1, M2] array."""
        assert L >= 0
        assert abs(M1) <= L
        assert M2 >= 0
        assert M2 <= L
        return L * (L+1) * (4*L-1) // 6 + (L+M1) * (L+1) + M2

    @property
    def LMAX21(self):
        """Number of elements between -LMAX and +LMAX."""
        return self.LMAX * 2 + 1

    @property
    def NM1M2(self):
        """Size of an [M1, M2] slice for L=LMAX."""
        return self.LMAX21 * self.LMAX1

    @property
    def shapeM1M2(self):
        """Shape of an [M1, M2] slice for L=LMAX."""
        return (self.LMAX21, self.LMAX1)

    @property
    def NLM1M2(self):
        """Number of [L, M1, M2] elements for L <= LMAX."""
        return self.indexLM1M2(self.LMAX1, -self.LMAX1, 0)


class RotateAlm(PackedLM1M2Mixin, ClProgram):
    """Python interface to the alm rotation kernels."""

    def __init__(self, LMAX, NSWORK, context=None):
        """Compile the kernel."""
        self.context = context
        self.LMAX = LMAX
        # TODO work out a default value for NSWORK so the user does not have to set it
        self.NSWORK = NSWORK
        super(RotateAlm, self).__init__(
            filename='rotate-alm.cl',
            options=["-DLMAX1=%d" % self.LMAX1, "-DNSWORK=%d" % NSWORK],
            context=context)

    @with_some_queue
    def __call__(self, alm, alpha, beta, gamma, queue=None):
        """Rotate Alm by the Euler angles and return as Blm."""
        assert alm.context == self.context
        assert alm.LMAX >= self.LMAX
        assert (alm.NS % self.NSWORK) == 0
        assert queue is not None
        alpha = _restrict_angle(alpha)
        beta = _restrict_angle(beta)
        gamma = _restrict_angle(gamma)
        LMAX = self.LMAX
        LMAX1 = self.LMAX1
        NS = alm.NS
        NSWORK = self.NSWORK

        ev_mat, dlmm = self.y_rotation_matrix(beta, queue=queue)

        blm = AlmArray(queue, LMAX, NS)
        eiM1alpha = cl.LocalMemory(8 * LMAX1)
        dlmm_local = cl.LocalMemory(4 * self.NM1M2)
        ev = self.program.rotate_alm(queue,
                                     (LMAX1, LMAX1, NS),
                                     (1, LMAX1, NSWORK),
                                     alm.data,
                                     blm.data,
                                     dlmm.data,
                                     np.float32(alpha),
                                     np.float32(gamma),
                                     eiM1alpha,
                                     dlmm_local,
                                     wait_for=(ev_mat,))
        return ev, blm

    @optional_out_array(shape=('NLM1M2',), dtype='f4')
    def y_rotation_matrix(self, beta, queue=None, out=None, wait_for=()):
        """Calculate the y rotation matrix (Wigner small d)."""
        assert queue is not None
        LMAX1 = self.LMAX1
        LMAX21 = self.LMAX21
        beta = _restrict_angle(beta)

        sterm_local = cl.LocalMemory(4 * LMAX1)
        jterm_local = cl.LocalMemory(4 * LMAX1)
        ev = self.program.y_rotation_matrix(queue,
                                            (LMAX21, LMAX1, LMAX1,),
                                            (1, 1, LMAX1),
                                            out.data,
                                            np.float32(beta),
                                            sterm_local,
                                            jterm_local,
                                            wait_for=wait_for)
        return ev, out
