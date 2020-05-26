"""Tests for the spherical bessel functions."""

# SPDX-FileCopyrightText: 2016 European Molecular Biology Laboratory (EMBL)
# SPDX-FileCopyrightText: 2018-2020 Christopher Kerr
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from hypothesis import assume, given, settings
import hypothesis.strategies as st
import hypothesis.extra.numpy as npst
import numpy as np
import numpy.testing as npt
from scipy.integrate import cumtrapz, quad
import scipy.special

from galumph.sphericalbessel import SphericalBessel


def spherical_bessel(n, z):
    """Calculate the order-n spherical bessel J function of z.

    Uses scipy.special.spherical_jn if available (since scipy 0.18.0),
    otherwise scipy.special.sph_jn (removed in scipy 1.0).
    """
    if hasattr(scipy.special, 'spherical_jn'):
        return scipy.special.spherical_jn(n, z, derivative=False)
    else:
        j, dj = scipy.special.sph_jn(n, z)
        return j[n]


def spherical_bessel_range(nmax, z):
    """Calculate the spherical bessel J function of z for orders up to nmax.

    Uses scipy.special.spherical_jn if available (since scipy 0.18.0),
    otherwise scipy.special.sph_jn (removed in scipy 1.0).
    """
    if hasattr(scipy.special, 'spherical_jn'):
        nrange = np.arange(nmax+1, dtype=int)
        return scipy.special.spherical_jn(nrange, z, derivative=False)
    else:
        j, dj = scipy.special.sph_jn(nmax, z)
        return j


def scipyBessel(LMAX, s, r):
    """Do the same calculation as SphericalBessel.__call__, using scipy."""
    NS, = s.shape
    result = np.empty((LMAX+1, NS))
    for i in range(NS):
        result[:, i] = spherical_bessel_range(LMAX, r*s[i])
    return result


def scipyBesselIntegral(LMAX, s, r):
    """Do the same calculation as SphericalBessel.integral, using scipy."""
    NS, = s.shape
    jl = scipyBessel(LMAX, s, r)
    result = np.zeros_like(jl)
    result[:, 1:] = cumtrapz(jl, x=s[np.newaxis, :]**3, axis=1) * (r**3 / s[1:]**3) / 3
    result[0, 0] = r**3 / 3
    return result


def scipyBesselQuad(L, s, r):
    """Integrate Jl(r*s)*r**2 from 0 to r."""
    def integrand(rr):
        return spherical_bessel(L, s*rr) * rr**2
    result = quad(integrand, 0, r, full_output=True)
    return result[0]


@settings(max_examples=25)
@given(
    LMAX=st.integers(min_value=0, max_value=20),
    worksize=st.integers(min_value=1, max_value=64),
    nchunks=st.integers(min_value=1, max_value=20),
    smax=st.floats(min_value=0.1, max_value=10),
    r=st.floats(min_value=0, max_value=100),
)
def test_single(cl_context, cl_queue,
                LMAX, worksize, nchunks, smax, r):
    """Test calculating the spherical Bessel for a single r value."""
    NS = worksize * nchunks
    assume(NS < 200)
    s = np.linspace(0, smax, num=NS, endpoint=True, dtype='f4')
    clBessel = SphericalBessel(LMAX, s, worksize, context=cl_context)
    ev, jl_dev = clBessel(r, queue=cl_queue)
    jl_sp = scipyBessel(LMAX, s, r)
    ev.wait()
    jl_cl = jl_dev.get(cl_queue)
    tolerance_factor = max((1, smax * r))
    npt.assert_allclose(jl_cl, jl_sp,
                        rtol=(tolerance_factor * 1e-5),
                        atol=(tolerance_factor * 1e-8))


@settings(max_examples=10)
@given(
    LMAX=st.integers(min_value=0, max_value=20),
    worksize=st.integers(min_value=1, max_value=64),
    natwork=st.integers(min_value=2, max_value=16),
    nchunks=st.integers(min_value=1, max_value=20),
    smax=st.floats(min_value=0.1, max_value=10),
    r=npst.arrays(
        dtype=st.sampled_from(('f4', 'f8')),
        shape=st.integers(min_value=1, max_value=16),
        elements=st.floats(min_value=0, max_value=100, width=32),
    ),
)
def test_multiple(cl_context,
                  LMAX, worksize, natwork, nchunks, smax, r):
    """Test calculating the spherical Bessel for multiple r values together."""
    NS = worksize * nchunks
    nAt, = r.shape
    assume(NS * nAt < 1000)
    assume(nAt <= natwork)
    s = np.linspace(0, smax, num=NS, endpoint=True, dtype='f4')
    clBessel = SphericalBessel(LMAX, s, worksize, natwork, context=cl_context)
    jl_dev = clBessel.batch(r)
    jl_cl = jl_dev.get()
    for iAt in range(nAt):
        jl_sp = scipyBessel(LMAX, s, r[iAt])
        tolerance_factor = max((1, smax * r[iAt]))
        npt.assert_allclose(jl_cl[iAt, :, :], jl_sp,
                            rtol=(tolerance_factor * 1e-5),
                            atol=(tolerance_factor * 1e-8))


@settings(max_examples=25)
@given(
    LMAX=st.integers(min_value=0, max_value=20),
    worksize=st.integers(min_value=1, max_value=64),
    nchunks=st.integers(min_value=1, max_value=20),
    smax=st.floats(min_value=0.1, max_value=10),
    r=st.floats(min_value=0, max_value=10),
)
def test_integral_simple(cl_context, cl_queue,
                         LMAX, worksize, nchunks, smax, r):
    """Test the integral kernel against a simple scipy implementation.

    scipyBesselIntegral does the same thing as the integral kernel
    (this checks that the algorithm is correctly implemented)
    """
    NS = worksize * nchunks
    assume(NS < 200)
    s = np.linspace(0, smax, num=NS, endpoint=True, dtype='f4')
    clBessel = SphericalBessel(LMAX, s, worksize, context=cl_context)
    ev, jl_dev = clBessel.integral(r, queue=cl_queue)
    jl_sp = scipyBesselIntegral(LMAX, s, r)
    ev.wait()
    jl_cl = jl_dev.get(cl_queue)
    tolerance_factor = max((1, smax * r))
    npt.assert_allclose(jl_cl, jl_sp,
                        rtol=(tolerance_factor * 1e-4),
                        atol=(tolerance_factor * 1e-6))


@settings(max_examples=10)
@given(
    LMAX=st.integers(min_value=0, max_value=20),
    worksize=st.integers(min_value=16, max_value=64),
    smax=st.floats(min_value=0.1, max_value=10),
    r=st.floats(min_value=0, max_value=10),
    # Don't test all s values as it would take too long, instead take a sample
    # also, don't test the first value, an integral over one step will never be very good
    i_s_test=st.lists(st.integers(min_value=128, max_value=1024),
                      min_size=20, max_size=20, unique=True),
)
def test_integral_quad(cl_context,
                       LMAX, worksize, smax, r, i_s_test):
    """Test the integral kernel against a scipy implementation.

    scipyBesselQuad uses non-uniform sampling to get an accurate
    value for the integral (to check that the algorithm gives
    the correct answer)
    """
    NS = (max(i_s_test) // worksize + 1) * worksize
    assert max(i_s_test) < NS
    assume(NS >= 256)
    s = np.linspace(0, smax, num=NS, endpoint=True, dtype='f4')
    clBessel = SphericalBessel(LMAX, s, worksize, context=cl_context)
    jl_dev = clBessel.integral(r)
    jl_cl = jl_dev.get()

    tolerance_factor = max((1, smax * r))
    for i_s in i_s_test:
        jl_sp = np.array([scipyBesselQuad(L, s[i_s], r)
                          for L in range(LMAX + 1)])
        npt.assert_allclose(jl_cl[:, i_s], jl_sp,
                            rtol=(tolerance_factor * 1e-3),
                            atol=(tolerance_factor * 1e-4))
