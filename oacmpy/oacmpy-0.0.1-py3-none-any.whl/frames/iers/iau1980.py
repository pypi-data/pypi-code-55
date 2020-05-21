"""Implementation of the IAU 1980 models"""
import functools
import re
from math import cos, sin

import numpy as np

from . import default_path
from ...constants import ARCSEC_TO_RAD, TWO_PI
from ...datetime.TimeScale import TT
from ...utils.rotation import angles2matrix


@functools.lru_cache(maxsize=None)
def _tab():
    """Extraction and caching of IAU1980 nutation coefficients"""

    filepath = default_path / "1996" / "tab5.1.txt"
    pattern = "^\s*(\-?\d+\s*)\s*(\-?\d+\s*)\s*(\-?\d+\s*)\s*(\-?\d+\s*)\s*(\-?\d+\s*)(\-?\d*\.?\d*\s*)(\-?\d*\.?\d*\s*)(\-?\d*\.?\d*\s*)(\-?\d*\.?\d*\s*)(\-?\d*\.?\d*\s*)$"
    # pattern = "^\s*([-]?\d+\s*)\s*(\d+\s*)\s*(\d+\s*)\s*(\d+\s*)\s*(\d+\s*)(\-?\d*\.?\d*\s*){5}"

    result = []
    with filepath.open() as fhd:
        lines = fhd.read().splitlines()
        i = 0
        for line in lines:
            m = re.search(pattern, line)
            if m:
                multipliers = [int(m.group(i)) for i in range(1, 6)]
                period = float(m.group(6))
                longitude_obliquity = [
                    float(m.group(7)),
                    float(m.group(8)),
                    float(m.group(9)),
                    float(m.group(10)),
                ]
                result.append((multipliers, period, longitude_obliquity))
                i += 1
    return result


def _earth_orientation(date, eop):
    """Earth Orientation Parameters in degrees"""
    return eop.x / 3600.0, eop.y / 3600.0


def earth_orientation(date, eop):
    """Earth Orientation as a rotation matrix"""
    x_p, y_p = np.deg2rad(_earth_orientation(date, eop))
    return angles2matrix([1, 2], [y_p, x_p])


def _precession_iau1976(date):
    """Precession in degrees. IAU1976 : Lieske precession"""

    t = date.change_scale(TT).julian_century

    theta = ((2004.3109 - (0.42665 + 0.041833 * t) * t) * t) * ARCSEC_TO_RAD
    z = ((2306.2181 + (1.09468 + 0.018203 * t) * t) * t) * ARCSEC_TO_RAD
    zeta = ((2306.2181 + (0.30188 + 0.017998 * t) * t) * t) * ARCSEC_TO_RAD
    return zeta, theta, z


def precession_iau1976(date):
    """Precession as a rotation matrix"""
    zeta, theta, z = _precession_iau1976(date)
    return angles2matrix([3, 2, 3], [zeta, -theta, z])


def _obliquity_iau1980(t):
    """Mean obliquity of the ecliptic"""
    # Mean obliquity of the ecliptic (IAU 1980 model), in radians
    eps = (84381.448 + (-46.8150 + (-5.9e-4 + 1.813e-3 * t) * t) * t) * ARCSEC_TO_RAD
    return eps


def _nutation_iau1980(t, eop, with_eop_correction):
    """Model 1980 of nutation

    :param t: julian centuries
    :param eop: EOP database
    :param with_eop_correction: set to ``True`` to include model correction
        from 'finals' files.
    :return: delta_psi, delta_eps in radians
    """

    # Fundamental argument in FK5
    # Mean longitude of Moon minus mean longitude of Moon's perigee.
    el = (485866.733 + (715922.633 + (31.310 + 0.064 * t) * t) * t) * ARCSEC_TO_RAD + (
        (1325.0 * t) % 1.0
    ) * TWO_PI
    el = el % TWO_PI

    # Mean longitude of Sun minus mean longitude of Sun's perigee.
    elp = (
        1287099.804 + (1292581.224 + (-0.577 - 0.012 * t) * t) * t
    ) * ARCSEC_TO_RAD + ((99.0 * t) % 1.0) * TWO_PI
    elp = elp % TWO_PI

    # Mean longitude of Moon minus mean longitude of Moon's node.
    f = (335778.877 + (295263.137 + (-13.257 + 0.011 * t) * t) * t) * ARCSEC_TO_RAD + (
        (1342.0 * t) % 1.0
    ) * TWO_PI
    f = f % TWO_PI

    # Mean elongation of Moon from Sun.
    d = (1072261.307 + (1105601.328 + (-6.891 + 0.019 * t) * t) * t) * ARCSEC_TO_RAD + (
        (1236.0 * t) % 1.0
    ) * TWO_PI
    d = d % TWO_PI

    # Longitude of the mean ascending node of the lunar orbit on the
    # ecliptic, measured from the mean equinox of date.
    omg = (450160.280 + (-482890.539 + (7.455 + 0.008 * t) * t) * t) * ARCSEC_TO_RAD + (
        (-5.0 * t) % 1.0
    ) * TWO_PI
    omg = omg % TWO_PI

    # ∆ψ = Σ (Ai+A'it) sin(ARGUMENT), ∆ε = Σ (Bi+B'it) cos(ARGUMENT)
    delta_psi = 0.0
    delta_eps = 0.0
    for multipliers, _, AiBi in _tab():
        arg = (
            multipliers[0] * el     # l
            + multipliers[1] * elp  # l'
            + multipliers[2] * f    # F
            + multipliers[3] * d    # D
            + multipliers[4] * omg  # Om
        )
        delta_psi += (AiBi[0] + AiBi[1] * t) * sin(arg)  # longitude
        delta_eps += (AiBi[2] + AiBi[3] * t) * cos(arg)  # obliquity

    delta_psi *= ARCSEC_TO_RAD * 1e-4
    delta_eps *= ARCSEC_TO_RAD * 1e-4

    # add the corrections (in marcsec) to the nutation in obliquity and longitude.
    if with_eop_correction:
        delta_psi += eop.dpsi * ARCSEC_TO_RAD / 1000.0
        delta_eps += eop.deps * ARCSEC_TO_RAD / 1000.0

    return delta_psi, delta_eps


def nutation(date, eop, eop_correction):
    """Nutation as a rotation matrix. This nutation is used for the TOD/MOD transformation.
    Correction can be obtained from IERS EOP Data: IERS EOP C04 IAU198 or finals

    """
    t = date.change_scale(TT).julian_century
    eps_bar = _obliquity_iau1980(t)
    delta_psi, delta_eps = _nutation_iau1980(t, eop, eop_correction)
    eps = eps_bar + delta_eps
    return angles2matrix([1, 3, 1], [-eps, -delta_psi, eps_bar])

