from datetime import datetime
from enum import Enum
from math import floor

from dateutil.parser import isoparse as parse_iso_date
from dateutil.tz import UTC as tzUTC

from ..ccsds.enumerates import TimeSystem
from ..constants import DAYSEC, JD_J2000, MJD2000_MJD, JD_MJD, JULIAN_CENTURY
from ..errors import DateError, TimeSystemError
from .TimeScale import TAI, Timescale, get_scale

ISO8601_FORMAT_Z = "%Y-%m-%dT%H:%M:%S.%fZ"

"""Origin of MJD"""
MJD_T0 = datetime(1858, 11, 17)

"""Offset between JD and J2000"""
J2000_T0 = datetime(2000, 1, 1)


"""Reference time scale (used internally for all computations). It must be a continuous scale: TT, TAI, UT1"""
REF_SCALE = TAI


def dnint(x):
    if x < 0.0:
        x -= 0.5
    else:
        x += 0.5
    return int(x)


def datetime_to_mjd(date_time : datetime):
    """Convert datetime to modified julian date"""
    year = date_time.year
    month = date_time.month
    day = date_time.day
    hour = date_time.hour
    minute = date_time.minute
    second = date_time.second + date_time.microsecond * 1e-6
    A = int(year / 100.0)
    B = 2.0 - A + int(A / 4.0)
    if month <= 2:
        year -= 1
        month += 12

    jd1 = int(365.25 * (year + 4716.0)) + int(30.6001 * (month + 1.0)) + day - 1524.0
    jd2 = (hour * 3600.0 + minute * 60.0 + second) / DAYSEC - 0.5
    if jd1 + jd2 >= 2299160.5:
        jd1 += B

    mjd1 = jd1 - JD_MJD
    mjd2 = jd2 + (mjd1 - floor(mjd1))
    mjd1 = floor(mjd1) + floor(mjd2)
    mjd2 -= floor(mjd2)

    return mjd1, mjd2


class Date:
    def __init__(self, string=None, time_system=None, day=None, sec=None,
                 _d_s_tai=None):
        """

        :param string: date string
        :param time_system: time system. Can be included in date string when UTC, otherwise it is mandatory.
        :param day: number of days from MJD
        :param sec: number of secs in day
        """
        self._datetime = None

        _mjd = 0.0
        d_to_mjd = 0.0
        s_to_mjd = 0.0
        if day:
            self.text = None
            d_to_mjd = day
            s_to_mjd = sec
            self._d = day
            self._s = sec
            self._fod = sec / DAYSEC
            self._mjd = (day, sec / DAYSEC)
            if time_system is None:
                raise TimeSystemError("Time system is missing!")
            self._time_system = time_system
            self._scale = get_scale(time_system)
            self._set_dt_properties(self._scale, self._d, self._s)  # set mjd_{REF_SCALE}

        if string:
            self.text = string

            if time_system is None:
                time_system = TimeSystem.UTC
            self._time_system = time_system
            self._scale = get_scale(time_system)

            date_time = parse_iso_date(string)
            if date_time.tzinfo is tzUTC:
                if time_system == TimeSystem.UTC:
                    self._datetime = date_time
                else:
                    raise DateError(
                        "Mixing different time systems! {} != {}".format(
                            date_time.tzinfo, time_system
                        )
                    )

            d_to_mjd, fod = datetime_to_mjd(date_time)
            s_to_mjd = fod * DAYSEC
            self._mjd = (d_to_mjd, fod)
            self._set_dt_properties(self._scale, d_to_mjd, s_to_mjd)  # set mjd_{scale}

        # _d, _s, _for are in the indicated time scale
        self._d = d_to_mjd
        self._s = s_to_mjd
        self._fod = self._s / DAYSEC

        # compute mjd_tai
        if _d_s_tai:
            self._d_tai = _d_s_tai[0]
            self._s_tai = _d_s_tai[1]
            self._mjd_tai = (_d_s_tai[0], _d_s_tai[1] / DAYSEC)
        else:
            _offset = -self._scale.offset_from(self, REF_SCALE)
            self._d_tai = d_to_mjd + int((s_to_mjd + _offset) // DAYSEC)
            self._s_tai = (s_to_mjd + _offset) % DAYSEC
            self._mjd_tai = (self._d_tai, self._s_tai / DAYSEC)

    @property
    def time_system(self):
        return self._time_system

    def change_scale(self, new_scale):
        """Compute values for new_scale, and set default properties to the new scale.
        A new instance is returned"""
        if isinstance(new_scale, Enum):
            new_scale = get_scale(new_scale)

        if new_scale == self._scale:
            return self

        offset = REF_SCALE.offset_to(self, new_scale)
        d = self._d_tai + int((self._s_tai + offset) // DAYSEC)
        s = (self._s_tai + offset) % DAYSEC
        return Date(time_system=TimeSystem(new_scale.get_name()), day=d, sec=s,
                    _d_s_tai=[self._d_tai, self._s_tai])

    def with_timescale(self, time_system):
        """Change the time scale information. No conversion is done."""
        self._time_system = time_system
        return self

    def add_offset(self, offset):
        d = self._d + int((self._s + offset) // DAYSEC)
        s = (self._s + offset) % DAYSEC
        _d_s_tai = None
        if hasattr(self, '_d_tai'):
            d_tai = self._d_tai + int((self._s + offset) // DAYSEC)
            s_tai = (self._s_tai + offset) % DAYSEC
            _d_s_tai = [d_tai, s_tai]
        return Date(time_system=TimeSystem.TAI, day=d, sec=s,
                    _d_s_tai=_d_s_tai)

    def _set_dt_properties(self, scale: Timescale, d_scaled, s_scaled):
        """Set the value of MJD for a given timescale.
        The value is accessible as a property: (e.g. mjd_tt, mjd_ut1...)"""
        ts = scale.get_name().lower()
        setattr(self, "mjd_{}".format(ts), (d_scaled, s_scaled / DAYSEC))
        setattr(self, "_d_{}".format(ts), d_scaled)
        setattr(self, "_s_{}".format(ts), s_scaled)

    @property
    def julian_century(self):
        """Compute the julian_century since J2000, in the current time scale"""
        d, fod = self.julian_date()
        return ((d - JD_J2000) + fod) / JULIAN_CENTURY

    @property
    def julian_century_2000(self):
        """Compute the julian_century since J2000, in the current time scale"""
        d, fod = self.julian_date()
        return ((d - JD_J2000) + fod) / JULIAN_CENTURY

    def modified_julian_date(self):
        """Return the Modified Julian date as day and fraction of day, in the current time scale
        RESOLUTION B1: It is recommended that JD be specified as SI seconds in Terrestrial Time (TT)"""
        return self._d, self._fod

    def julian_date(self):
        """Return the Modified Julian date as day and fraction of day, in the current time scale
        RESOLUTION B1: It is recommended that JD be specified as SI seconds in Terrestrial Time (TT)"""
        d = self._d + JD_MJD
        fod = self._fod
        fod += d - floor(d)
        d = floor(d) + floor(fod)
        fod -= floor(fod)
        return d, fod

    @property
    def jd(self):
        """Compute the Julian Date, which is the number of days from the
        January 1, 4712 B.C., 12:00. (TT)  [IERS RESOLUTION B1]"""
        return self.julian_date()

    @property
    def mjd(self):
        """Return the Modified Julian Date in the current time scale"""
        return self.modified_julian_date()

    @property
    def mjd1950(self):
        """Return the Modified 1950 Julian Day in the current time scale"""
        d, fod = self.modified_julian_date()
        return d - MJD2000_MJD + 18262.5, fod

    @property
    def mjd2000(self):
        d, fod = self.julian_date()
        return d - JD_J2000, fod

    @property
    def d(self):
        """Return the integer number of days in current time scale"""
        return self._d


    def iso_str(self):
        """Convert date to string with ISO format '2020-01-01T00:00:00+00:00'"""
        return self.datetime.isoformat(sep="T")

    def format_date(self, fmt):
        """Convert date to string with ISO format"""
        return self.datetime.strftime(fmt)

    def duration_from(self, date):
        """Return the duration from date, in seconds"""
        if self._time_system == date._time_system:
            tsname = self._time_system.name.lower()
            attr1d = getattr(self, "_d_{}".format(tsname))
            attr1s = getattr(self, "_s_{}".format(tsname))
            attr2d = getattr(date, "_d_{}".format(tsname))
            attr2s = getattr(date, "_s_{}".format(tsname))
            return (attr1d - attr2d) * DAYSEC + (attr1s - attr2s)
        return (self._d_tai - date._d_tai) * DAYSEC + (self._s_tai - date._s_tai)

    @property
    def datetime(self):
        if self._datetime is None:
            year, month, day, h, m, s, ms = self._to_calendar()
            self._datetime = datetime(year=year, month=month, day=day, hour=h, minute=m, second=s, microsecond=ms)
        return self._datetime

    def date(self):
        return self.datetime.date()

    def time(self):
        return self.datetime.time()

    def _to_calendar(self):
        """Convert date to Gregorian calendar: year, month, day, hour, minutes, seconds, microseconds
        Updated from SOFA."""
        d, fod = self.jd
        fod -= 0.5
        f1 = d % 1.0
        f2 = fod % 1.0
        f = (f1 + f2) % 1.0
        if f < 0.0:
            f += 1.0

        d = dnint(d - f1) + dnint(fod - f2) + dnint(f1 + f2 - f)
        jd = dnint(d) + 1

        l = jd + 68569
        n = (4 * int(l)) / 146097
        l -= int((146097 * int(n) + 3) / 4)
        i = (4000 * (l + 1)) / 1461001
        l -= int((1461 * int(i)) / 4 - 31)
        k = (80 * int(l)) / 2447
        day = l - int((2447 * int(k)) / 80)
        l = k / 11
        month = int(k) + 2 - 12 * int(l)
        year = int(100 * (int(n) - 49) + int(i) + int(l))
        hour = f * 24.0
        minutes = (hour % 1.0) * 60.0
        seconds = (minutes % 1.0) * 60.0
        microsec = (seconds % 1.0) * 1e6
        return year, month, day, int(hour), int(minutes), int(seconds), int(round(microsec))

    def strftime(self, fmt):
        return self.datetime.strftime(fmt)

    def str(self):
        return self.__str__()

    def __str__(self):
        return self.strftime(ISO8601_FORMAT_Z)
