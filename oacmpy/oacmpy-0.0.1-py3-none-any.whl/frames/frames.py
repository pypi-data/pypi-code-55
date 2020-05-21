# -*- coding: utf-8 -*-

"""This module defines the Frames transformation, and their links.




   Inertial Frames             EME2000 ------ bias ----- GCRF
                                   |                      |
                               (Precession)               |
                                   |                      |
                                 ,---.        (Precession + Nutation + model corrections)
                                 |MOD|                    |
                                 `---'                    |
                                   |                      |
                                Nutation                  |
                 ,---.   + model corrections              |
                 |GTOD|            |                      |
                                   |                      |
   True Equator Frames: GTOD --- TOD                     CIRF
                                 |                        |
                               |G50|                      |
                        (Sidereal time)                (Sidereal time)
                                |                         |
Terrestrial  Frames:             |                        |
            TEME -- (Equinox) -- PEF                     TIRF
                                   \                     /
                                    \                   /
                               (IAU 1980 EOP)      (IAU 2010 EOP)
                                       \              /
                                         \          /
                                             ITRF



"""

import numpy as np

from ..constants import ARCSEC_TO_RAD, TWO_PI
from ..datetime.TimeScale import UTC, TT, GMST
from ..errors import UnknownFrameError
from ..utils.rotation import rot_z
from .AbstractFrame import AbstractFrame
from .iers import iau1980, iau2000, iau2010, iers
from .iers.eop import EopDb

CIO_BASED_FRAMES = ["ITRF", "TIRF", "CIRF", "GCRF"]
EQUINOX_BASED_FRAMES = ["TOD", "MOD"]
OTHER_FRAMES = ["EME2000", "TEME", "PEF", "G50"]
__all__ = CIO_BASED_FRAMES + EQUINOX_BASED_FRAMES + OTHER_FRAMES + ["get_frame"]


class _EME2000(AbstractFrame):
    """EME2000 inertial frame (also known as J2000)"""

    frame_name = "EME2000"

    def __init__(self):
        AbstractFrame.__init__(self, self.frame_name, None)


EME2000 = _EME2000()


class _GCRF(AbstractFrame):
    """Geocentric Celestial Reference Frame"""

    frame_name = "GCRF"

    def __init__(self):
        AbstractFrame.__init__(self, self.frame_name, EME2000)

    def GCRF_to_EME2000(self, _):
        m = iers._bias2006()
        return m, np.zeros(3)


GCRF = _GCRF()


class _CIRF(AbstractFrame):
    """Celestial Intermediate Reference Frame"""

    frame_name = "CIRF"

    def __init__(self):
        AbstractFrame.__init__(self, self.frame_name, GCRF)

    def CIRF_to_GCRF(self, date):
        self.eop = EopDb.get(date.mjd)
        m = iau2010.precesion_nutation_2006(date, self.eop)
        return m, np.zeros(3)


CIRF = _CIRF()


class _TIRF(AbstractFrame):
    """Terrestrial Intermediate Reference Frame"""

    frame_name = "TIRF"

    def __init__(self):
        AbstractFrame.__init__(self, self.frame_name, CIRF)

    def TIRF_to_CIRF(self, date):
        self.eop = EopDb.get(date.mjd)
        m = iau2010.sidereal_era_2000(date)
        return m, np.zeros(3)


TIRF = _TIRF()


class _MOD(AbstractFrame):
    """Mean (Equator) Of Date"""

    frame_name = "MOD"

    def __init__(self):
        AbstractFrame.__init__(self, self.frame_name, EME2000)

    def MOD_to_EME2000(self, date):
        m = iau1980.precession_iau1976(date)
        return m, np.zeros(3)


MOD = _MOD()


class _TOD(AbstractFrame):
    """True (Equator) Of Date"""

    frame_name = "TOD"

    def __init__(self, nutation_model='1980', eop_correction=False):
        self._nutation_model = nutation_model
        self._eop_correction = eop_correction
        AbstractFrame.__init__(self, self.frame_name, MOD)

    def TOD_to_MOD(self, date):
        self.eop = EopDb.get(date.change_scale(UTC).mjd)
        if self._nutation_model == '1980':
            m = iau1980.nutation(date, self.eop, self._eop_correction)
        elif self._nutation_model == '2000AR06':
            m = iau2000.nutation(date, self.eop, self._eop_correction)
        else:
            raise UnknownFrameError("Unknown nutation model")
        return m, np.zeros(3)


TOD = _TOD(nutation_model='1980', eop_correction=False)
TOD1980 = _TOD(nutation_model='1980', eop_correction=True)
TOD2000 = _TOD(nutation_model='2000AR06', eop_correction=False)


class _GTOD(AbstractFrame):
    """Greenwich True Of Date"""

    frame_name = "GTOD"

    def __init__(self):
        AbstractFrame.__init__(self, self.frame_name, TOD)


class _PEF(AbstractFrame):
    """Pseudo Earth Fixed"""

    frame_name = "PEF"

    def __init__(self):
        AbstractFrame.__init__(self, self.frame_name, TIRF)

    def PEF_to_TIRF(self, date):
        t = date.julian_century
        sp = -47.e-6 * t * ARCSEC_TO_RAD  # Eq5.13
        m = rot_z(np.deg2rad(sp))
        offset = np.zeros(3)
        return m, offset


PEF = _PEF()


class _TEME(AbstractFrame):
    """True Equator Mean Equinox of date
    This frame is of interest only for TLE."""

    frame_name = "TEME"

    def __init__(self):
        AbstractFrame.__init__(self, self.frame_name, PEF)

    def TEME_to_PEF(self, date):
        # reference: Vallado 2007, p236
        gmst = date.change_scale(GMST)
        d, fod = gmst.mjd
        gmst80 = ((d % 1.0) + fod) * TWO_PI
        m = rot_z(-gmst80)
        return m, np.zeros(3)


TEME = _TEME()


class _ITRF(AbstractFrame):
    """International Terrestrial Reference Frame"""

    frame_name = "ITRF"

    def __init__(self):
        AbstractFrame.__init__(self, self.frame_name, PEF)

    def ITRF_to_PEF(self, date):
        self.eop = EopDb.get(date.mjd)
        m = iau1980.earth_orientation(date, self.eop)
        return m, np.zeros(3)

    def ITRF_to_TIRF(self, date):
        self.eop = EopDb.get(date.mjd)
        m = iau2010.earth_orientation(date, self.eop)
        return m, np.zeros(3)


ITRF = _ITRF()  # 2000
ITRF93 = _ITRF()  # approx
ITRF97 = _ITRF()  # approx


class _G50(AbstractFrame):
    """Gamma50 Reference Frame
    """

    frame_name = "G50"

    def __init__(self):
        AbstractFrame.__init__(self, self.frame_name, EME2000)

    def G50_to_EME2000(self, _):

        m = [
            [0.9999256794956877, -0.0111814832204662, -0.0048590038153592],
            [0.0111814832391717, 0.9999374848933135, -0.0000271625947142],
            [0.0048590037723143, -0.0000271702937440, 0.9999881946023742],
        ]

        return m, np.zeros(3)


G50 = _G50()
GTOD = _GTOD()


def get_frame(frame):
    switcher = {
        "EME2000": EME2000,
        "GCRF": GCRF,
        "TIRF": TIRF,
        "ITRF93": ITRF93,
        "ITRF97": ITRF97,
        "ITRF2000": ITRF,
        "ITRF": ITRF,
        "CIRF": CIRF,
        "VEIS": G50,
        "GTOD": GTOD,
        "TOD": TOD,
        "TOD1980": TOD1980,
        "TOD2000": TOD2000,
        "MOD": MOD,
    }
    res = switcher.get(frame, None)
    if res is None:
        raise UnknownFrameError(frame)
    return res
