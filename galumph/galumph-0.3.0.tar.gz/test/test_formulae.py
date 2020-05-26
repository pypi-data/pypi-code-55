"""Test various mathematical formulae used in GALUMPH.

This uses symbolic algebra to verify various simplified formulae.
"""

# SPDX-FileCopyrightText: 2018-2020 Christopher Kerr
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import pytest

sympy = pytest.importorskip('sympy')


def iLMKP(L, M, K, P, check=True):
    """Index into a packed DLMKP matrix."""
    if check:
        assert L >= M
        assert L >= K
        assert M >= 0
        assert K >= M
        assert (L+K) >= P
        assert (L-K) <= P
        assert (L+K+P) % 2 == 0
    iP = (P - (L-K)) // 2
    iK0 = (K*(K+1) - M*(M+1)) // 2
    iM00 = (3*L*(L+3) + 7 - M*M) * M // 6
    iL000 = L*(L+1)*(L+1)*(L+2) // 12
    return iL000 + iM00 + iK0 + iP


def assert_sympy_equal(a, b):
    """Assert that two sympy expressions are equal."""
    assert sympy.simplify(a - b) == 0


def test_packed_sizes_offsets():
    """Check formulae for sizes of and offsets into packed dlmkp matrices."""
    def psize(K):
        """Number of P points for a given K (where K <= L)."""
        return K + 1

    def pindex(L, K, P):
        """Number of points between (L,M,K,Pmin) and (L,M,K,P)."""
        return (P - (L-K)) / 2

    def ksize(L, M):
        """Number of (K, P) points for given (L, M)."""
        K = sympy.symbols("k", integer=True)
        return sympy.summation(psize(K), (K, M, L))

    def iKP_local_ip(M, K, iP):
        """Number of points between (L,M,Kmin,Pmin) and (K,P)."""
        Kx = sympy.symbols("k'", integer=True)
        return sympy.summation(psize(Kx), (Kx, M, K-1)) + iP

    def iKP_local(L, M, K, P):
        """Number of points between (L,M,Kmin,Pmin) and (K,P)."""
        return iKP_local_ip(M, K, pindex(L, K, P))

    def msize(L):
        """Number of points for a given L."""
        M = sympy.symbols("M", integer=True)
        return sympy.summation(ksize(L, M), (M, 0, L))

    def lsize(LMAX):
        """Total number of points for L <= LMAX."""
        L = sympy.symbols("L", integer=True)
        return sympy.summation(msize(L), (L, 0, LMAX))

    def iL000(L):
        """Index of (L,0,0,Pmin)."""
        Lx = sympy.symbols("L'", integer=True)
        return sympy.summation(msize(Lx), (Lx, 0, L-1))

    def iLMoff(L, M):
        """Difference between (L,0,0,Pmin) and (L,M,Kmin,Pmin)."""
        Mx = sympy.symbols("M'", integer=True)
        return sympy.summation(ksize(L, Mx), (Mx, 0, M-1))

    def iLM00(L, M):
        """Index of (L,M,0,Pmin)."""
        return iL000(L) + iLMoff(L, M)

    # Put these checks in internal sub-functions so that the variables
    # are not visible in the scope of the helper sub-functions above
    def check_sizes():
        """Check that sizes are one greater than the index of the last value."""
        L, M, K = sympy.symbols("L M, K", integer=True)
        assert_sympy_equal(
            psize(K) - 1,
            pindex(L, K, L+K),
        )
        assert_sympy_equal(
            ksize(L, M) - 1,
            iKP_local(L, M, L, 2*L),
        )
        assert_sympy_equal(
            lsize(L) - 1,
            iLM00(L, L) + iKP_local(L, L, L, 2*L),
        )

    def check_formulae():
        L, M, K, P, ip, LMAX = sympy.symbols("L M, K, P, i_P, LMAX", integer=True)
        assert_sympy_equal(
            ((L+1) * (L+2) - M * (M+1)) / 2,
            ksize(L, M),
        )
        assert_sympy_equal(
            (K * (K+1) - M * (M+1)) / 2 + ip,
            iKP_local_ip(M, K, ip),
        )
        assert_sympy_equal(
            (LMAX+1) * (LMAX+2)**2 * (LMAX+3) / 12,
            lsize(LMAX),
        )
        assert_sympy_equal(
            L * (L+1) * (L+1) * (L+2) / 12,
            iL000(L),
        )
        assert_sympy_equal(
            (3 * L * (L+3) + 7 - M * M) * M / 6,
            iLMoff(L, M),
        )

    check_sizes()
    check_formulae()
