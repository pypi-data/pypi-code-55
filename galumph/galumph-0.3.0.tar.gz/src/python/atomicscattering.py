# SPDX-FileCopyrightText: 2016 European Molecular Biology Laboratory (EMBL)
# SPDX-FileCopyrightText: 2017-2020 Christopher Kerr
#
# SPDX-License-Identifier: LGPL-3.0-or-later

__copyright__ = "European Molecular Biology Laboratory (EMBL)"
__license__ = "LGPLv3+"

import numpy as np
import pyopencl as cl
from pyopencl import array as cl_array

from . import almarray
from .sphericalbessel import SphericalBessel
from .sphericalharmonic import SphericalHarmonic
from .util import check_array, ClProgram, PackedLMMixin, with_some_queue


def sicopolar(xyz):
    x = xyz[0]
    y = xyz[1]
    z = xyz[2]
    rho = np.linalg.norm(xyz[:2])
    if rho > 0:
        cosphi = x/rho
        sinphi = y/rho
    else:
        cosphi = 0
        sinphi = 0
    r = np.linalg.norm(xyz)
    if r > 0:
        costheta = z/r
        sintheta = rho/r
    else:
        costheta = 0
        sintheta = 0
    return r, costheta, sintheta, complex(cosphi, sinphi)


def sicopolar_array(xyz):
    x = xyz[:, 0]
    y = xyz[:, 1]
    z = xyz[:, 2]

    rho = np.linalg.norm(xyz[:, :2], axis=1)
    rho_gt0 = (rho > 0)
    eiphi = x + 1j * y
    eiphi[rho_gt0] /= rho[rho_gt0]

    r = np.linalg.norm(xyz, axis=1)
    r_gt0 = (r > 0)
    costheta = np.zeros_like(r)
    sintheta = np.zeros_like(r)
    costheta[r_gt0] = z[r_gt0]/r[r_gt0]
    sintheta[r_gt0] = rho[r_gt0]/r[r_gt0]
    return r, costheta, sintheta, eiphi


class AtomicScattering(PackedLMMixin, ClProgram):
    """Kernel for calculating the ALM scattering from an atomic structure."""

    def __init__(self, LMAX, s,
                 worksize=64,
                 natwork=16,
                 context=None):
        assert LMAX >= 0
        self.LMAX = LMAX
        s = np.asanyarray(s)
        NS, = s.shape
        assert NS > 0
        assert np.all(s >= 0)
        self.NS = NS
        self.s = s
        assert worksize > 0
        assert NS % worksize == 0
        self.worksize = worksize
        assert natwork > 0
        self.natwork = natwork
        super(AtomicScattering, self).__init__(
            filename='alm-add-atom.cl',
            options=["-DNATWORK=%d" % natwork, "-DWORKSIZE=%d" % worksize],
            context=context)
        context = self.context

        self.sphbes = SphericalBessel(LMAX, s, worksize, natwork, context=context)
        self.sphharm = SphericalHarmonic(LMAX, natwork, context=context)

    def zeros(self):
        """Return an AlmArray with the correct shape initialized to zero."""
        with cl.CommandQueue(self.context) as queue:
            return almarray.zeros(queue, self.LMAX, self.NS)

    @with_some_queue
    def add_atom(self, alm, xyz, ff, queue=None):
        """Add the scattering from a single atom to the ALM.

        Args:
            alm: AlmArray
            xyz: Cartesian coordinates of the atom
            ff: Atomic form factor: single value or an array of length NS

        """
        assert alm.context == self.context
        check_array(alm, (self.NLM, self.NS), dtype='c8')
        assert queue is not None
        LMAX1 = self.LMAX1
        NS = self.NS
        worksize = self.worksize

        ff = np.asanyarray(ff)
        if np.isscalar(ff) or (np.shape(ff) == ()):
            ff = np.ones_like(self.s) * ff
        else:
            assert ff.shape == self.s.shape

        r, costheta, sintheta, eiphi = sicopolar(xyz)

        evY, ylm_dev = self.sphharm(costheta, sintheta, queue=queue)
        evJ, jl_dev = self.sphbes(r, queue=queue)

        ff32 = np.array(ff, dtype=np.float32)
        ff_dev = cl_array.to_device(queue, ff32)

        ev = self.program.alm_add_atom(queue,
                                       (LMAX1, NS),
                                       (1, worksize),
                                       np.complex64(eiphi),
                                       ylm_dev.data,
                                       jl_dev.data,
                                       ff_dev.data,
                                       alm.data,
                                       wait_for=(evY, evJ))
        return ev, alm

    @with_some_queue
    def add_many_atoms(self, alm, xyz, ff, queue=None):
        """Add the scattering from an array of atoms to the ALM.

        Args:
            alm: AlmArray
            xyz: Cartesian coordinates of the atoms
            ff: Atomic form factors: shape either (natoms) or (natoms, NS)

        """
        assert alm.context == self.context
        check_array(alm, (self.NLM, self.NS), dtype='c8')
        assert queue is not None
        LMAX1 = self.LMAX1
        NS = self.NS
        natwork = self.natwork
        worksize = self.worksize

        natoms, ndim = np.shape(xyz)
        assert natoms > 0
        assert ndim == 3

        ff = np.asanyarray(ff)
        if np.ndim(ff) == 1:
            ff = np.ones_like(self.s) * ff[:, np.newaxis]
        check_array(ff, (natoms, NS))

        ylm_local = cl.LocalMemory(8*natwork*LMAX1)

        for iAt0 in range(0, natoms, natwork):
            iAtN = min(natoms, iAt0+natwork)

            r, costheta, sintheta, eiphi = sicopolar_array(xyz[iAt0:iAtN, :])

            evY, ylm_dev = self.sphharm.batch(costheta, sintheta, queue=queue)
            evJ, jl_dev = self.sphbes.batch(r, queue=queue)

            ff32 = np.array(ff[iAt0:iAtN, :], dtype=np.float32)
            ff_dev = cl_array.to_device(queue, ff32)
            eiphi32 = np.array(eiphi, dtype=np.complex64)
            eiphi_dev = cl_array.to_device(queue, eiphi32)

            ev = self.program.alm_add_many_atoms(queue,
                                                 (LMAX1, NS),
                                                 (1, worksize),
                                                 np.uint32(iAtN - iAt0),
                                                 eiphi_dev.data,
                                                 ylm_dev.data,
                                                 jl_dev.data,
                                                 ff_dev.data,
                                                 alm.data,
                                                 ylm_local,
                                                 wait_for=(evY, evJ))
            ev.wait()
        return ev, alm

    @with_some_queue
    def __call__(self, xyz, ff, queue=None):
        """Calculate the atomic scattering from the given atoms.

        Allocates an AtomAlm array, zeros it, then adds the scattering from
        the atoms given the (x,y.z) positions and the atomic form factors.
        """
        alm = self.zeros()
        ev, alm = self.add_many_atoms(alm, xyz, ff, queue=queue)
        return ev, alm
