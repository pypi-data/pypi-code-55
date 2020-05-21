"""Implementation of the IAU 2010 Earth orientation model
"""
import functools
from math import sin, cos, floor, pi
import numpy as np

from .iers2003 import nut_argument
from .TableReader import read_table
from ...datetime.Date import JD_J2000
from ...datetime.TimeScale import UT1, TT
from ...utils.rotation import angles2matrix, rot_z
from ...constants import ARCSEC_TO_RAD
from ...datetime.Date import Date


__all__ = ["sidereal_era_2000", "precesion_nutation_2006", "earth_orientation"]


@functools.lru_cache(maxsize=None)
def _tab():
    """Extraction and caching of IAU2000 nutation coefficients
    """

    elements = ["tab5.2a.txt", "tab5.2b.txt", "tab5.2d.txt"]  # tables for x, y and s

    return read_table("2010", elements)


def _julian_century(date: Date):
    return date.change_scale(TT).julian_century_2000


def _earth_orientation(date: Date, eop):
    """Earth orientation parameters in degrees, X, Y and s': TIO locator"""

    ttt = _julian_century(date)
    # Formula Eq.5.13
    s_prime = -0.000047 * ttt
    return eop.x * ARCSEC_TO_RAD, eop.y * ARCSEC_TO_RAD, s_prime * ARCSEC_TO_RAD


def earth_orientation(date: Date, eop):
    """Earth orientation as a rotating matrix"""
    x_p, y_p, s_prime = _earth_orientation(date, eop)
    return angles2matrix([3, 2, 1], [-s_prime, x_p, y_p])


def _sidereal_era_2000(date: Date):
    """Sideral time in radians"""
    jd, fod = date.change_scale(UT1).julian_date()
    jd2000 = (jd - JD_J2000) + fod
    f = (jd - floor(jd)) + (fod - floor(fod))
    # formula 5.15
    return (2.0 * pi * (f + 0.779057273264 + 0.00273781191135448 * jd2000)) % (2.0 * pi)


def sidereal_era_2000(date: Date):
    """Sidereal time as a rotation matrix relating TIRS and CIRS"""
    # formula 5.5
    return rot_z(_sidereal_era_2000(date))


def _xysxy2_iau2006(date: Date):
    """
    Return:
        3-tuple of float: Values of X, Y, s + XY/2 in arcsecond
    """

    tjc = _julian_century(date)

    # The IAU 2006/2000A developements, formula 5.16
    # polynomial part
    X = -16616.99 + tjc * (2004191742.88 + tjc * (-427219.05 + tjc * (-198620.54 + tjc * (-46.05 + 5.98 * tjc))))

    Y = -6950.78 + tjc * (-25381.99 + tjc * (-22407250.99 + tjc * (1842.28 + tjc * (1113.06 + 0.99 * tjc))))

    # s + XY/2
    s_xy_2 = 94.0 + tjc * (3808.65 + tjc * (-122.68 + tjc * (-72574.11 + tjc * (27.98 + 15.62 * tjc))))

    # non-polynomial part
    x_tab, y_tab, s_tab = _tab()
    for j in range(5):
        t_pow_j = tjc ** j

        cx, cy, cs = 0.0, 0.0, 0.0
        for _, Axs, Axc, *p_coefficients in x_tab[j]:
            ax_p = nut_argument(tjc, p_coefficients)
            cx += Axs * sin(ax_p) * t_pow_j + Axc * cos(ax_p)

        for _, Ays, Ayc, *p_coefficients in y_tab[j]:
            ay_p = nut_argument(tjc, p_coefficients)
            cy += Ays * sin(ay_p) + Ayc * cos(ay_p) * t_pow_j

        for _, Ass, Asc, *p_coefficients in s_tab[j]:
            as_p = nut_argument(tjc, p_coefficients)
            cs += Ass * sin(as_p) * t_pow_j + Asc * cos(as_p)

        X += cx * t_pow_j
        Y += cy * t_pow_j
        s_xy_2 += cs * t_pow_j

    # Conversion to arcsecond
    return X * 1e-6, Y * 1e-6, s_xy_2 * 1e-6


def _xys_2006A(date: Date, eop):
    """Get The X, Y and s coordinates
    Return:
        3-tuple of floats: X, Y and s, in radians
    """

    X, Y, s_xy2 = _xysxy2_iau2006(date)
    X = (X + eop.dx / 1000.0) * ARCSEC_TO_RAD
    Y = (Y + eop.dy / 1000.0) * ARCSEC_TO_RAD
    s = s_xy2 * ARCSEC_TO_RAD - (X * Y / 2.0)
    return X, Y, s


def precesion_nutation_2006(date: Date, eop):
    """Precession/nutation joint rotation matrix for the IAU2010 model of the CIP motion,
    relating CIRS and GCRS"""

    x, y, s = _xys_2006A(date, eop)
    a = 0.5 + 1.0 / 8.0 * (x ** 2 + y ** 2)

    # formula 5.10, it requires less computation than 5.6
    x2 = x ** 2
    y2 = y ** 2
    xy = x * y
    mat = np.array(
        [
            [1.0 - a * x2, -a * xy, x],
            [-a * xy, 1.0 - a * y2, y],
            [-x, -y, 1.0 - a * (x2 + y2)],
        ]
    )
    return np.dot(mat, rot_z(s))

