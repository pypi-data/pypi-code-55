import os
from datetime import timedelta
from math import radians, sin, pi, floor
from pathlib import Path

from ..ccsds.enumerates import TimeSystem
from ..constants import JULIAN_CENTURY, DAYSEC, JD_J2000, MJD2000_MJD, JD_MJD
from ..errors import TimeSystemError
from .TaiUtc import TaiUtc


"""
From: http://www.stjarnhimlen.se/comp/time.html

 UTC 1972-  GPS 1980-    TAI 1958-               TT 2001-
----+---------+-------------+-------------------------+-----
    |         |             |                         |
    |<------ TAI-UTC ------>|<-----   TT-TAI    ----->|
    |         |             |      32.184s fixed      |
    |<GPS-UTC>|<- TAI-GPS ->|                         |
    |         |  19s fixed  |                         |
    |                                                 |
    <> delta-UT = UT1-UTC                             |
     | (max 0.9 sec)                                  |
-----+------------------------------------------------+-----
     |<-------------- delta-T = TT-UT1 -------------->|
    UT1 (UT)                                       TT/TDT/ET
    
And we have the following connection diagram:

    TDB  ---  TCG                _ _ _ _ _ _ _
                  \            /               \
                   TT  ---  TAI  ---  UTC  ---  UT1 
                  /            \                   \
              TCB               GPS                  GMST

"""

default_path = Path(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data")
)
taiUtc = TaiUtc(default_path / "tai-utc.dat")


def offset_tai_minus_utc(_):
    """
    UTC = TAI - (number of leap seconds)
    """
    return -timedelta(seconds=Timescale._LEAP_SECONDS)


def get_gmst_from_ut1(cjd_ut1_d, cjd_ut1_fod):
    """Compute GMST-UT1 (IAU 1982 GMST-UT1 model)"""
    # greenwich mean sidereal time of 0h UT1: gmst = A0 + A1*TU + A2*TU.^2 + A3*TU.^3;
    tu = floor(cjd_ut1_fod + (cjd_ut1_d - JD_J2000)) / JULIAN_CENTURY
    tof_sec_ut1 = ((cjd_ut1_d % 1.0) + (cjd_ut1_fod % 1.0)) * DAYSEC  # time of day, ut1, sec
    tof_sec_ut1 = tof_sec_ut1 % DAYSEC
    # GMST at 0h UT1
    gmst_0h_ut1 = ((-6.2e-6 * tu + 0.093104) * tu + 8640184.812866) * tu + (24110.54841 - 0.5 * DAYSEC)  # noon correction
    # GMST at current time
    omg = (7.2921158553 * 1e-5 + 4.3 * 1e-15 * tu) * 86400 / (2 * pi)
    gmst = gmst_0h_ut1 + omg * tof_sec_ut1
    gmst_ut1 = gmst % DAYSEC
    return gmst_ut1


def offset_ut1_minus_gmst(date):
    """Compute GMST-UT1 (IAU 1982 GMST-UT1 model)"""
    # greenwich mean sidereal time of 0h UT1: gmst = A0 + A1*TU + A2*TU.^2 + A3*TU.^3;
    cjd_ut1_d, cjd_ut1_fod = date.jd
    tof_sec_ut1 = ((cjd_ut1_d % 1.0) + (cjd_ut1_fod % 1.0)) * DAYSEC  # time of day, ut1, sec

    if date.time_system != TimeSystem.UT1:
        raise TimeSystemError("Date should be in UT1")
    cjd_ut1_d, cjd_ut1_fod = date.jd
    gmst_ut1 = get_gmst_from_ut1(cjd_ut1_d, cjd_ut1_fod)
    offset = (tof_sec_ut1 - 0.5 * DAYSEC) - (gmst_ut1 % DAYSEC)
    return offset


def offset_tdb_minus_tcb(date):
    """
        jd_mjd1950_tdb: Modified (1950.0) Julian date in TCB time scale
    TDB = TCB − LB×(JD_TCB − T0)×86400 + TDB0
    https://en.wikipedia.org/wiki/Barycentric_Dynamical_Time"""
    mjd_tcb, mjd_tcb_fod = date.mjd
    mjd_mjd1950_tcb = mjd_tcb - MJD2000_MJD + 18262.5
    t0_tcb = 9862.0003725
    tdb0 = -6.55 * 1e-5
    lb = 1.550519768 * 1e-8
    return -lb * ((mjd_mjd1950_tcb - t0_tcb) + mjd_tcb_fod) * DAYSEC + tdb0


def offset_tcg_minus_tt(date):
    """Definition of the Barycentric Dynamic Time scale relatively to Terrestrial Time
    """
    jd_tt, jd_tt_fod = date.jd
    Lg = 6.969290134 * 1e-10
    return Lg * ((jd_tt - 2443144.5003725) * DAYSEC + jd_tt_fod * DAYSEC)


def offset_tdb_minus_tt(date):
    """Definition of the Barycentric Dynamic Time scale relatively to Terrestrial Time
    """
    jd = date.jd
    jj = date.julian_century
    mjd2000_d, mjd2000_fod = date.mjd2000
    m = radians(357.5277233 + 35999.05034 * jj)
    delta_lambda = radians(246.11 + 0.90251792 * (mjd2000_d + mjd2000_fod))
    return 0.001657 * sin(m) + 0.000022 * sin(delta_lambda)


class Timescale:
    _LEAP_SECONDS = 37.0  # as of 2018
    _DUT1 = 0.0  # delta-UT = UT1-UTC

    def __init__(self, name: TimeSystem, parent):
        self.name = name
        self.parent = parent
        self.offset_to_parent = 0
        self.taiUtc = taiUtc
        pass

    def get_offset_parent_minus_this(self, date):
        parent, offset = self._get_offset(date, self.parent, self, False)
        return parent, offset

    def get_offset_this_minus_parent(self, date):
        parent, offset = self._get_offset(date, self, self.parent, True)
        return parent, offset

    def _get_offset(self, date, ts1, ts2, is_from):
        """Return the parent timescale, and the offset to this parent timescale
            ts_current = ts_parent + offset
        """
        if not ts1 or not ts2:
            return self.parent, 0.0

        # check if the inverse function is defined
        fcn = "offset_{}_minus_{}".format(ts1.get_name(), ts2.get_name()).lower()
        if hasattr(self, fcn):
            offset_sec = getattr(self, fcn)(date)
            return self.parent, offset_sec

        fcn = "offset_{}_minus_{}".format(ts2.get_name(), ts1.get_name()).lower()
        offset_sec = -getattr(self, fcn)(date)
        return self.parent, offset_sec

    def get_name(self):
        return self.name.value

    @staticmethod
    def set_leap_second(leap_seconds):
        """Set the cumulative number of leap seconds, TAI-UTC"""
        Timescale._LEAP_SECONDS = leap_seconds

    @staticmethod
    def set_delta_ut1(dut1):
        """Set the delta-Ut1 = UT1-UTC,  |dUT1| < 0.9 seconds"""
        if abs(dut1) > 0.9:
            raise TimeSystemError("|DeltaUT1| must be < 0.9")
        Timescale._DUT1 = dut1

    def offset_from(self, date, scale):
        """Compute offset between this time scale and the input time scale, in the input time scale,
        at given date, in seconds.
            scale = this - offset
        """

        # date.change_scale(scale)

        if self == scale:
            return 0.0
        elif self.parent == scale:
            _, offset = self.get_offset_this_minus_parent(date)
            return offset
        elif scale.parent == self:
            _, offset = scale.get_offset_parent_minus_this(date)
            return offset

        # there is at least one intermediate timescale...
        self_parent, offset_this_minus_parent = self.get_offset_this_minus_parent(date)
        scale_parent, offset_parent_minus_scale = scale.get_offset_parent_minus_this(date)
        if self_parent is None:
            self_parent = self
            offset_this_minus_parent = 0.0
        if scale_parent is None:
            scale_parent = scale
            offset_parent_minus_scale = 0.0

        offset_this_minus_scale = offset_this_minus_parent + offset_parent_minus_scale
        return offset_this_minus_scale + self_parent.offset_from(date, scale_parent)

    def offset_to(self, date, scale):
        """Compute offset between this time scale and the input time scale, in the input time scale,
        at given date, in seconds.
            scale = this + offset
        """
        return -self.offset_from(date, scale)


class TimescaleTai(Timescale):
    def __init__(self):
        Timescale.__init__(self, TimeSystem.TAI, None)


TAI = TimescaleTai()


class TimescaleUTC(Timescale):
    def __init__(self):
        Timescale.__init__(self, TimeSystem.UTC, TAI)

    def offset_utc_minus_tai(self, date):
        """ UTC = TAI - (number of leap seconds)
        return UTC-TAI
        """
        #return -Timescale._LEAP_SECONDS
        d, fod = date.mjd
        return -self.taiUtc[d]


UTC = TimescaleUTC()


class TimescaleUt1(Timescale):
    def __init__(self):
        Timescale.__init__(self, TimeSystem.UT1, UTC)

    def offset_ut1_minus_utc(self, date):
        return Timescale._DUT1


class TimescaleTT(Timescale):
    def __init__(self):
        Timescale.__init__(self, TimeSystem.TT, TAI)

    def offset_tt_minus_tai(self, _):
        return 32.184


class TimescaleGps(Timescale):
    def __init__(self):
        Timescale.__init__(self, TimeSystem.GPS, TAI)

    def offset_gps_minus_tai(self, _):
        return -19.0


TT = TimescaleTT()


class TimescaleTdb(Timescale):
    def __init__(self):
        Timescale.__init__(self, TimeSystem.TDB, TT)

    def offset_tdb_minus_tt(self, date):
        return offset_tdb_minus_tt(date)


TDB = TimescaleTdb()


class TimescaleTcb(Timescale):
    def __init__(self):
        Timescale.__init__(self, TimeSystem.TCB, TDB)

    def offset_tcb_minus_tdb(self, date):
        # compute mjd_tdb
        #if not hasattr(date, "mjd_tcb"):
        #    if not hasattr(date, "mjd_tt"):
        #        date.mjd_tt = (
        #            date.mjd_tai + TimescaleTT().offset_tt_minus_tai(date) / DAYSEC
        #        )
        #    date.mjd_tcb = date.mjd_tt + offset_tcb_minus_tt(date) / DAYSEC
        return -offset_tdb_minus_tcb(date)


TCB = TimescaleTcb()


class TimescaleTcg(Timescale):
    def __init__(self):
        Timescale.__init__(self, TimeSystem.TCG, TT)

    def offset_tcg_minus_tt(self, date):
        return offset_tcg_minus_tt(date)


class TimescaleGmst(Timescale):
    def __init__(self):
        Timescale.__init__(self, TimeSystem.GMST, TAI)

    def offset_gmst_minus_tai(self, date):
        """Offset GMST - TAI"""
        # try to find a solution to the non-linear relation between gmst and tai
        gmst0_sec = (date.mjd_gmst[0] % 1.0 + date.mjd_gmst[1]) * DAYSEC
        cjd_ut1_d, cjd_ut1_fod = date.jd
        cjd_ut1_fod = 0.
        for i in range(0, 20):
            gmst_sec = get_gmst_from_ut1(cjd_ut1_d, cjd_ut1_fod)
            df = gmst_sec - gmst0_sec
            cjd_ut1_fod = cjd_ut1_fod - df / DAYSEC
            if abs(df) < 1e-8:
                pass
        sec_ut1 = ((cjd_ut1_d % 1.0) + cjd_ut1_fod % 1.0) * DAYSEC
        _ut1_minus_tai = TimescaleUTC().offset_utc_minus_tai(date) + \
                         TimescaleUt1().offset_ut1_minus_utc(date)
        sec_tai = sec_ut1 - _ut1_minus_tai
        return gmst0_sec - sec_tai - ((date.mjd_gmst[0] + JD_MJD) - cjd_ut1_d) * DAYSEC

    def offset_tai_minus_gmst(self, date):
        _ut1_minus_tai = TimescaleUTC().offset_utc_minus_tai(date) + \
                         TimescaleUt1().offset_ut1_minus_utc(date)
        date = date.change_scale(UT1)
        _ut1_minus_gmst = offset_ut1_minus_gmst(date)
        return _ut1_minus_gmst - _ut1_minus_tai


UT1 = TimescaleUt1()
GPS = TimescaleGps()
TCG = TimescaleTcg()
GMST = TimescaleGmst()


def get_scale(time_scale):
    """Retrieve a Scale from a TimeSystemEnum
    """
    switcher = {
        TimeSystem.UTC: UTC,
        TimeSystem.GPS: GPS,
        TimeSystem.UT1: UT1,
        TimeSystem.TAI: TAI,
        TimeSystem.TT: TT,
        TimeSystem.TDB: TDB,
        TimeSystem.TCG: TCG,
        TimeSystem.TCB: TCB,
        TimeSystem.GMST: GMST,
    }
    res = switcher.get(time_scale, None)
    if res is None:
        raise TimeSystemError("Cannot find a match for {}".format(time_scale))
    return res
