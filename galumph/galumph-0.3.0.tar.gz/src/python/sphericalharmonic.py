# SPDX-FileCopyrightText: 2016 European Molecular Biology Laboratory (EMBL)
# SPDX-FileCopyrightText: 2017-2020 Christopher Kerr
#
# SPDX-License-Identifier: LGPL-3.0-or-later

__copyright__ = "European Molecular Biology Laboratory (EMBL)"
__license__ = "LGPLv3+"

import numpy as np
import pyopencl as cl
import pyopencl.array as cl_array

from .util import ClProgram, optional_out_array, PackedLMMixin


class SphericalHarmonic(PackedLMMixin, ClProgram):
    """Functor class giving spherical harmonics at a given theta, phi

    LMAX and the OpenCL work group size are set in the __init__ function
    The output will contain all values of L and all non-negative M up to
    and including LMAX, in a packed format

    theta and phi are passed to __call__ in the form of cos and sin values
    This is not only how they are used internally but also easier to calculate
    precisely from (x,y,z) coordinates"""

    def __init__(self, LMAX, natwork=16, context=None):
        """Set up all the necessary arrays, kernels etc"""
        if LMAX < 0:
            raise ValueError('LMAX < 0 is meaningless')
        elif LMAX < 3:
            # Using LMAX < 3 causes pocl to crash while compiling the
            # ylm_Mpart_local CL kernel - see issue #54
            raise NotImplementedError('LMAX < 3 is not supported')
        self.LMAX = LMAX
        assert natwork > 0
        self.natwork = natwork
        super(SphericalHarmonic, self).__init__(
            filename='spherical-harmonic.cl',
            options=["-DLMAX1=%d" % (self.LMAX1,)],
            context=context)

    @optional_out_array(shape=('NLM',), dtype='f4')
    def __call__(self, costheta, sintheta, queue=None, out=None):
        """Calculate all non-negative spherical harmonics up to LMAX.

        The calculation is done asynchronously, the returned OpenCL
        event object can be used to wait for the result.
        """
        assert -1 <= costheta
        assert costheta <= 1
        assert 0 <= sintheta  # 0 <= theta <= pi
        assert sintheta <= 1

        LMAX1 = self.LMAX1

        localmemF = cl.LocalMemory(4*LMAX1)
        localmemI = cl.LocalMemory(4*LMAX1)

        ev = self.program.ylm_real(
            queue, (LMAX1,), (LMAX1,),
            np.float32(costheta),
            np.float32(sintheta),
            out.data,
            localmemF,
            localmemI,
        )
        return ev, out

    @optional_out_array(shape=('natwork', 'NLM'), dtype='f4')
    def batch(self, costheta, sintheta, queue=None, out=None):
        """Calculate spherical harmonics for a batch of atoms.

        The calculation is done asynchronously, the returned OpenCL
        event object can be used to wait for the result.
        """
        costheta = np.array(costheta, dtype=np.float32)
        sintheta = np.array(sintheta, dtype=np.float32)
        assert np.shape(costheta) == np.shape(sintheta)
        assert np.all(-1 <= costheta)
        assert np.all(costheta <= 1)
        assert np.all(0 <= sintheta)  # 0 <= theta <= pi
        assert np.all(sintheta <= 1)

        LMAX1 = self.LMAX1
        nAt = np.size(costheta)
        assert nAt > 0
        assert nAt <= self.natwork

        costh_dev = cl_array.to_device(queue, costheta)
        sinth_dev = cl_array.to_device(queue, sintheta)
        localmemF = cl.LocalMemory(4*LMAX1)
        localmemI = cl.LocalMemory(4*LMAX1)

        ev = self.program.ylm_real_batch(
            queue, (LMAX1, nAt), (LMAX1, 1),
            costh_dev.data,
            sinth_dev.data,
            out.data,
            localmemF,
            localmemI,
        )

        return ev, out
