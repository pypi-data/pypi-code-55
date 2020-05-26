"""Pure Python implementation of Gaunt coefficients.

Gaunt coefficients give the spatial integral of the product of three
spherical harmonic functions. In GALUMPH, they are used in the ALM
translation function.

The code here is based on Formula 4.2 of:
  J. Rasch and A. C. H. Yu, 'Efficient Storage Scheme for
  Pre-calculated Wigner 3j, 6j and Gaunt Coefficients', SIAM
  J. Sci. Comput. Volume 25, Issue 4, pp. 1416-1428 (2003)
  https://doi.org/10.1137/S1064827503422932
However, the formula in that article has some errors, which are corrected here.

For a translation along the Z axis, we only need values with:
    m_3 == 0, m_1 == -m_2
This allows simplifying the formula and referring to m_1 as plain `m`.
"""

# SPDX-FileCopyrightText: 2020 Christopher Kerr
#
# SPDX-License-Identifier: LGPL-3.0-or-later

__copyright__ = "Christopher Kerr"
__license__ = "LGPLv3+"

from fractions import Fraction
import functools
import math
import operator


def prod(iterable, *, start=1):
    """Product of a sequence of numbers.

    Reimplementation of math.prod, which is only available for Python >= 3.8.
    """
    return functools.reduce(operator.mul, iterable, start)


def _calculate_factorials(N):
    """Return a tuple containing the factorials of all numbers from 0 to N.

    Since Python integers are arbitrary-precision, the values are exact.
    """
    assert N >= 0
    # Special case for 0
    fac_i = 1
    fac_list = [fac_i]
    for i in range(1, N+1):
        fac_i *= i
        fac_list.append(fac_i)
    return tuple(fac_list)


def delta_squared(l_1, l_2, l_3, *, factorials=None):
    """Square of the Delta function defined in Formula 2.3 of Rasch2003."""
    if factorials is None:
        factorials = _calculate_factorials(l_1 + l_2 + l_3 + 1)
    return Fraction(
        prod((
            factorials[l_1 + l_2 - l_3],
            factorials[l_2 + l_3 - l_1],
            factorials[l_3 + l_1 - l_2],
        )),
        factorials[l_1 + l_2 + l_3 + 1],
    )


def _gaunt_ksum(l_1, l_2, l_3, m, *, factorials):
    """Part of the Gaunt coefficient function involving a sum over k."""
    k_min = max(l_1 - m - l_3, l_2 - m - l_3, 0)
    k_max = min(l_1 - m, l_2 - m, l_1 + l_2 - l_3)

    def kpart(k):
        return Fraction(
            (-1) ** k,
            prod((
                factorials[k],
                factorials[k + l_3 + m - l_1],
                factorials[k + l_3 + m - l_2],
                factorials[l_1 + l_2 - l_3 - k],
                factorials[l_1 - m - k],
                factorials[l_2 - m - k],
            )),
        )

    return sum(kpart(k) for k in range(k_min, k_max + 1))


def _gaunt_sqrt_arg(l_1, l_2, l_3, m, *, factorials):
    """Calculate the part of the formula that needs to be square-rooted."""
    return prod((
        (2 * l_1 + 1),
        (2 * l_2 + 1),
        (2 * l_3 + 1),
        factorials[l_1 + m],
        factorials[l_1 - m],
        factorials[l_2 + m],
        factorials[l_2 - m],
        factorials[l_3 + 0],
        factorials[l_3 - 0],
    ))


def _gaunt_big_L_part(l_1, l_2, l_3, *, factorials):
    """The part of the Gaunt coefficient formula involving the capital L."""
    assert (l_1 + l_2 + l_3) % 2 == 0
    L = (l_1 + l_2 + l_3) // 2
    return Fraction(
        factorials[L],
        prod((
            factorials[L - l_1],
            factorials[L - l_2],
            factorials[L - l_3],
        )),
    )


def _modified_gaunt_squared(l_1, l_2, l_3, m, *, factorials=None):
    """Square magnitude and sign of the modified Gaunt coefficient.

    Here we are calculating a modified Gaunt coefficient which differs from
    the standard coefficient by a factor of sqrt((2 * l_3 + 1) / 4 * pi). That
    modification is applied here.
    """
    if factorials is None:
        factorials = _calculate_factorials(l_1 + l_2 + l_3 + 1)
    non_sqrt_part = prod((
        delta_squared(l_1, l_2, l_3, factorials=factorials),
        _gaunt_ksum(l_1, l_2, l_3, m, factorials=factorials),
        _gaunt_big_L_part(l_1, l_2, l_3, factorials=factorials),
    ))
    sq_mag = prod((
        _gaunt_sqrt_arg(l_1, l_2, l_3, m, factorials=factorials),
        non_sqrt_part * non_sqrt_part,
        (2 * l_3 + 1),  # For standard Gaunt, omit this
    ))  # For standard Gaunt, divide by (4 * math.pi)
    sign = (-1) ** ((l_1 + l_2 - l_3) // 2)
    if non_sqrt_part < 0:
        sign *= -1
    return sq_mag, sign


def modified_gaunt(l_1, l_2, l_3, m, *, factorials=None):
    """Modified Gaunt coefficient used in the Z translation matrix."""
    sq_mag, sign = _modified_gaunt_squared(l_1, l_2, l_3, m, factorials=factorials)
    return sign * math.sqrt(sq_mag)


def shzmat(LMAX):
    """Calculate the array of Gaunt coefficients used for ALM Z translation."""
    factorials = _calculate_factorials(4 * LMAX + 1)
    dlmkp = list()
    for L in range(LMAX + 1):
        for M in range(L + 1):
            for K in range(M, L + 1):
                for P in range(L - K, L + K + 1, 2):
                    dlmkp.append(modified_gaunt(L, K, P, M, factorials=factorials))
    return dlmkp
