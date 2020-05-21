import functools
from math import cos, sin

from .iers2003 import nut_argument
from .TableReader import read_table
from ...constants import ARCSEC_TO_RAD
from ...datetime.TimeScale import TT
from ...datetime.Date import Date
from ...utils.rotation import angles2matrix


@functools.lru_cache(maxsize=None)
def _tab():
    """Extraction and caching of IAU2000 nutation coefficients
    """

    elements = ["tab5.3a.txt", "tab5.3b.txt"]  # tables for deps, dpsi

    return read_table("2006", elements)


def bias_2000():
    """Frame bias components of IAU 2000 precession-nutation models"""
    DPBIAS = -0.041775 * ARCSEC_TO_RAD
    DEBIAS = -0.0068192 * ARCSEC_TO_RAD
    DRA0 = -0.0146 * ARCSEC_TO_RAD
    return DPBIAS, DEBIAS, DRA0


def _precession_correction_2000(date: Date):
    """Precession-rate part of the IAU 2000 precession-nutation models"""
    t = date.julian_century_2000
    PRECOR = -0.29965 * ARCSEC_TO_RAD
    OBLCOR = -0.02524 * ARCSEC_TO_RAD
    # Precession rate contributions with respect to IAU 1976/80
    return PRECOR * t, OBLCOR * t


def _precession_2000(date: Date):
    """Frame bias and precession, IAU 2000. (Lieske et al. 1977)"""
    t = date.julian_century_2000

    EPS0 = 84381.448 * ARCSEC_TO_RAD
    psia77 = (5038.7784 + (-1.07259 + (-0.001147) * t) * t) * t * ARCSEC_TO_RAD
    oma77  =       EPS0 + ((0.05127 + (-0.007726) * t) * t) * t * ARCSEC_TO_RAD
    chia   = (  10.5526 + (-2.38064 + (-0.001125) * t) * t) * t * ARCSEC_TO_RAD

    # frame bias
    dpsibi, depsbi, dra0 = bias_2000()

    # precession correction
    dpsipr, depspr = _precession_correction_2000(date)
    psia = psia77 + dpsipr
    oma = oma77 + depspr

    pass


# noinspection PyPep8Naming
def _xys_2000A(date):
    """Get The X, Y and s coordinates
    Return:
        3-tuple of floats: X, Y and s, in radians
    """
    pass


def _obliquity_iau2006(t):
    """Mean obliquity of the ecliptic(IAU2006 model)"""
    # Mean obliquity of the ecliptic (IAU 2006 model), in radians
    eps = (84381.406 + (-46.836769 + (-1.831e-4 + (2.0034e-3 + (-5.76e-7 - 4.34e-8 * t) * t) * t) * t) * t) * ARCSEC_TO_RAD
    return eps


# noinspection PyPep8Naming
def _nutation_iau2000R06(t, eop, with_eop_correction):
    """Nutation model in IAU 2000_R06"""
    dpsi_tab, deps_tab = _tab()

    delta_eps = 0
    delta_psi = 0
    for j in range(0, 2):
        t_j = t ** j
        # longitude
        for _, Axs, Axc, *p_coefficients in dpsi_tab[j]:
            arg = nut_argument(t, p_coefficients)
            c_arg = cos(arg)
            s_arg = sin(arg)
            delta_psi += (Axs * s_arg + Axc * c_arg) * t_j

        # obliquity
        for _, Bxs, Bxc, *p_coefficients in deps_tab[j]:
            arg = nut_argument(t, p_coefficients)
            c_arg = cos(arg)
            s_arg = sin(arg)
            delta_eps += (Bxc * c_arg + Bxs * s_arg) * t_j

    delta_psi *= ARCSEC_TO_RAD * 1e-6
    delta_eps *= ARCSEC_TO_RAD * 1e-6

    # add the corrections (in marcsec) to the nutation in obliquity and longitude.
    if with_eop_correction:
        delta_psi += eop.dpsi * ARCSEC_TO_RAD / 1000.0*0
        delta_eps += eop.deps * ARCSEC_TO_RAD / 1000.0*0

    # into radians
    return delta_psi, delta_eps


def nutation(date: Date, eop, eop_correction=True):
    """Nutation as a rotation matrix. This nutation is used for the TOD/MOD transformation.

    """
    t = date.change_scale(TT).julian_century
    eps_bar = _obliquity_iau2006(t)
    delta_psi, delta_eps = _nutation_iau2000R06(t, eop, eop_correction)
    eps = eps_bar + delta_eps
    return angles2matrix([1, 3, 1], [-eps, -delta_psi, eps_bar])
