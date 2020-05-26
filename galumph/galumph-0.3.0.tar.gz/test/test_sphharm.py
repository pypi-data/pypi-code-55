# SPDX-FileCopyrightText: 2016 European Molecular Biology Laboratory (EMBL)
# SPDX-FileCopyrightText: 2017-2020 Christopher Kerr
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from hypothesis import assume, example, given, settings
import hypothesis.strategies as st
import hypothesis.extra.numpy as npst
import numpy as np
import numpy.testing as npt
from scipy.special import sph_harm

from galumph.sphericalharmonic import SphericalHarmonic


def scipy_SphHarm(LMAX, theta):
    NLM = (LMAX+1)*(LMAX+2)//2
    ylm = np.empty((NLM,), dtype=np.complex128)
    for L in range(LMAX+1):
        il0 = L*(L+1)//2
        ilend = il0+L+1
        ylm[il0:ilend] = sph_harm(np.arange(L+1), L, 0, theta)
    return ylm.real


@settings(max_examples=25)
@given(
    LMAX=st.integers(min_value=3, max_value=20),
    theta=st.floats(min_value=0, max_value=np.pi),
)
@example(LMAX=3, theta=(np.pi/2))  # Issue #24
def test_single(cl_context, cl_queue, LMAX, theta):
    """Test calculating the spherical harmonics for one (theta, phi) pair."""
    clSphHarm = SphericalHarmonic(LMAX, context=cl_context)
    costheta = np.cos(theta)
    sintheta = np.sin(theta)
    # Rounding error sometimes gives theta slightly greater than pi
    assume(sintheta >= 0)

    ev, ylm_dev = clSphHarm(costheta, sintheta, queue=cl_queue)
    ylm_sp = scipy_SphHarm(LMAX, theta)
    ev.wait()
    ylm_cl = ylm_dev.get(cl_queue)

    npt.assert_allclose(ylm_cl[:], ylm_sp, rtol=1e-4, atol=1e-6)


@settings(max_examples=10)
@given(
    LMAX=st.integers(min_value=3, max_value=20),
    theta=npst.arrays(
        shape=st.tuples(
            st.integers(min_value=1, max_value=16),
        ),
        elements=st.floats(min_value=0, max_value=np.float32(np.pi), width=32),
        dtype=st.sampled_from(('f4', 'f8')),
    ),
)
def test_multiple(cl_context, cl_queue, LMAX, theta):
    """Test calculating the spherical harmonics for arrays of theta."""
    clSphHarm = SphericalHarmonic(LMAX, context=cl_context)
    nAt = theta.shape[0]
    costheta = np.cos(theta)
    sintheta = np.sin(theta)
    # Rounding error sometimes gives theta slightly greater than pi
    assume(np.all(sintheta >= 0))

    ev, ylm_dev = clSphHarm.batch(costheta, sintheta, queue=cl_queue)

    NLM = (LMAX+1)*(LMAX+2)//2
    ylm_sp = np.empty((nAt, NLM), dtype=np.complex128)
    for iAt in range(nAt):
        ylm_sp[iAt, :] = scipy_SphHarm(LMAX, theta[iAt])
    ev.wait()
    ylm_cl = ylm_dev.get(cl_queue)

    npt.assert_allclose(ylm_cl[:nAt, :], ylm_sp, rtol=1e-4, atol=1e-6)
