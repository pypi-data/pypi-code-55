# SPDX-FileCopyrightText: 2018-2020 Christopher Kerr
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from hypothesis import given
import hypothesis.strategies as st
import pytest

from galumph import gaunt

sympy = pytest.importorskip('sympy')
import sympy.physics.wigner  # noqa: E402

LMAX_TEST = 63


def assert_sympy_equal(a, b):
    """Assert that two sympy expressions are equal."""
    assert sympy.simplify(a - b) == 0


@st.composite
def LMKP(draw):
    L = draw(st.integers(min_value=0, max_value=LMAX_TEST))
    M = draw(st.integers(min_value=0, max_value=L))
    K = draw(st.integers(min_value=M, max_value=L))
    iP = draw(st.integers(min_value=0, max_value=K))
    P = L - K + 2 * iP
    return (L, M, K, P)


def sympy_matrix_element_W(L, M, K, P):
    """Calculate an element of the dlmkp matrix using sympy."""
    wigner0 = sympy.physics.wigner.wigner_3j(L, P, K, 0, 0, 0)
    wignerM = sympy.physics.wigner.wigner_3j(L, P, K, -M, 0, M)
    prefactor = (2*P+1) * sympy.sqrt((2*L+1) * (2*K+1))
    return prefactor * wigner0 * wignerM


def sympy_matrix_element_G(L, M, K, P):
    """Calculate an element of the dlmkp matrix using sympy."""
    standard_gaunt = sympy.physics.wigner.gaunt(L, K, P, M, -M, 0)
    prefactor = sympy.sqrt((2*P+1) * 4 * sympy.pi)
    return prefactor * standard_gaunt


@given(lmkp=LMKP())
def test_sympy_gaunt_vs_wigner(lmkp):
    L, M, K, P = lmkp
    assert_sympy_equal(
        sympy_matrix_element_W(L, M, K, P),
        sympy_matrix_element_G(L, M, K, P),
    )


@given(lmkp=LMKP())
def test_python_vs_sympy_gaunt2(lmkp):
    L, M, K, P = lmkp
    sympy_result = sympy_matrix_element_G(L, M, K, P)
    sympy_sign = sympy.sign(sympy_result)
    python_result, sign = gaunt._modified_gaunt_squared(L, K, P, M)
    if sympy_sign != 0:
        assert sign == sympy_sign
    assert_sympy_equal(
        python_result,
        sympy_result ** 2,
    )


@given(lmkp=LMKP())
def test_python_vs_sympy_gaunt(lmkp):
    L, M, K, P = lmkp
    sympy_result = sympy_matrix_element_G(L, M, K, P)
    sympy_float = float(sympy_result.n(10))
    python_result = gaunt.modified_gaunt(L, K, P, M)
    assert python_result == pytest.approx(sympy_float)
