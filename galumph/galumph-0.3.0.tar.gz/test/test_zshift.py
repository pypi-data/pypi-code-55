# SPDX-FileCopyrightText: 2018-2020 Christopher Kerr
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from hypothesis import assume, given, settings
import hypothesis.strategies as st
import numpy as np
import numpy.testing as npt
import pyopencl as cl
import pyopencl.array as cl_array
import pytest

from galumph.atomicscattering import AtomicScattering
from galumph.gaunt import shzmat
from galumph.zshift import AlmShiftZ

# Import test strategies from test_atomic_scattering
from test_atomic_scattering import alm_parameters, atom_xyzf


LMAX_TEST = 20


@pytest.fixture(scope='module')
def cl_shzmat(cl_context):
    """Fixture with the dlmkp matrix already copied to the device."""
    dlmkp_host = np.asarray(shzmat(LMAX_TEST), dtype='f4')
    with cl.CommandQueue(cl_context) as queue:
        dlmkp_dev = cl_array.to_device(queue, dlmkp_host)
    return dlmkp_dev


@settings(max_examples=10)
@given(
    almparams=alm_parameters(
        # Need a reasonable LMAX to get accurate results
        LMAX=st.integers(min_value=10, max_value=LMAX_TEST),
        worksize=st.integers(min_value=4, max_value=16),
        smax=st.floats(min_value=0.1, max_value=1),
    ),
    xyz_ff=atom_xyzf(),
    u=st.floats(min_value=0, max_value=5),  # TODO support negative u
)
def test_zshift(cl_context, cl_shzmat, cl_queue, almparams, xyz_ff, u):
    """Compare shifting the Alm versus shifting the atomic positions."""
    s = almparams['s']
    LMAX = almparams['LMAX']
    NSWORK = almparams['worksize']
    # LMAX1 * NSWORK needs to be less than the maximum work group size
    assume((LMAX+1) * NSWORK <= 256)
    assume(u*s[-1] < LMAX/2)
    scattering_kernel = AtomicScattering(context=cl_context, **almparams)
    shift_kernel = AlmShiftZ(context=cl_context,
                             LMAX=LMAX,
                             NSWORK=NSWORK,
                             s=s,
                             dlmkp=cl_shzmat)
    xyz, ff = xyz_ff

    alm_orig = scattering_kernel(xyz, ff)

    ev, alm_almshz = shift_kernel(alm_orig, u, queue=cl_queue)

    xyzshz = xyz + np.array([[0, 0, u]])
    alm_xyzshz = scattering_kernel(xyzshz, ff)

    ev.wait()

    np_alm_almshz = alm_almshz.get(unpack=True)
    # M==0 terms should be real
    npt.assert_array_almost_equal(np_alm_almshz[:, 0, :].imag, 0, decimal=4)

    np_alm_xyzshz = alm_xyzshz.get(unpack=True)
    # Up to LMAX/2 should give good quality
    npt.assert_allclose(np_alm_almshz[:LMAX//2, :LMAX//2, :],
                        np_alm_xyzshz[:LMAX//2, :LMAX//2, :],
                        rtol=1e-2, atol=1e-3 * np.sum(ff))
    npt.assert_allclose(np_alm_almshz, np_alm_xyzshz,
                        rtol=1e-0, atol=1e-1 * np.sum(ff))


@settings(max_examples=10)
@given(
    almparams=alm_parameters(
        # Need a reasonable LMAX to get accurate results
        LMAX=st.integers(min_value=10, max_value=LMAX_TEST),
        worksize=st.integers(min_value=1, max_value=16),
    ),
    xyz_ff=atom_xyzf(),
)
def test_zshift_0(cl_context, cl_shzmat, almparams, xyz_ff):
    """Check that shifting by zero gives exactly the same ALM."""
    s = almparams['s']
    LMAX = almparams['LMAX']
    NSWORK = almparams['worksize']
    # LMAX1 * NSWORK needs to be less than the maximum work group size
    assume((LMAX+1) * NSWORK <= 256)
    scattering_kernel = AtomicScattering(context=cl_context, **almparams)
    shift_kernel = AlmShiftZ(context=cl_context,
                             LMAX=LMAX,
                             NSWORK=NSWORK,
                             s=s,
                             dlmkp=cl_shzmat)
    xyz, ff = xyz_ff
    alm_orig = scattering_kernel(xyz, ff)
    alm_almshz = shift_kernel(alm_orig, 0)

    np_alm_orig = alm_orig.get(unpack=True)
    np_alm_almshz = alm_almshz.get(unpack=True)
    npt.assert_allclose(np_alm_almshz, np_alm_orig)
