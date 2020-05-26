# SPDX-FileCopyrightText: 2018 Christopher Kerr
#
# SPDX-License-Identifier: LGPL-3.0-or-later

__copyright__ = "Christopher Kerr"
__license__ = "LGPLv3+"

import numpy as np
import pyopencl as cl
from pyopencl import array as cl_array

from .util import check_array, PackedLMMixin


class AlmArray(PackedLMMixin, cl_array.Array):
    """Array holding A(L,M,s) representation of scattering amplitudes."""

    def __init__(self, cq, LMAX, NS, dtype='c8', **kwargs):
        """Work out the shape from LMAX and call the superclass constructor."""
        assert LMAX >= 0
        assert NS > 0
        self.LMAX = LMAX
        self.NS = NS
        shape = (self.NLM, self.NS)
        super(AlmArray, self).__init__(cq, shape, dtype=dtype, **kwargs)

    def get(self, queue=None, ary=None, unpack=False, **kwargs):
        """Copy from the device into a numpy array.

        If unpack is True, unpack the array into a lower triangular array
        with dimensions [L,M,S].
        """
        if not unpack:
            return super(AlmArray, self).get(queue=queue, ary=ary, **kwargs)
        unpacked_shape = (self.LMAX1, self.LMAX1, self.NS)
        if ary is None:
            ary = np.zeros(unpacked_shape, dtype=self.dtype)
        else:
            check_array(ary, unpacked_shape)
        for L in range(self.LMAX1):
            packed_range = slice(self.indexLM(L, 0), self.indexLM(L+1, 0))
            ary[L, 0:L+1, :] = self[packed_range, :].get(queue=queue, **kwargs)
        return ary


def empty(cq, LMAX, NS, dtype='c8', **kwargs):
    """Create an AlmArray without initializing the memory."""
    return AlmArray(cq, LMAX, NS, dtype=dtype, **kwargs)


def zeros(cq, LMAX, NS, dtype='c8', **kwargs):
    """Create an AlmArray initialized to zero."""
    alm = AlmArray(cq, LMAX, NS, dtype=dtype, **kwargs)
    if isinstance(cq, cl.CommandQueue):
        alm.fill(0, queue=cq)
    else:
        with cl.CommandQueue(cq) as queue:
            alm.fill(0, queue)
    return alm
