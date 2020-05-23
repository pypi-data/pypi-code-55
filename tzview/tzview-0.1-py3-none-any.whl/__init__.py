"""
Leave dt arithmetic to others

Incorporate to this command using
substitution (preferable) or xargs.

now means current time
local means current timezone
"""

from typing import List
import datetime

import pytz
import tzlocal

# Stuff for mypy
# _pytz_tzinfo = Union[pytz.UTC.__class__,
#                     pytz.tzinfo.StaticTzInfo, pytz.tzinfo.DstTzInfo]
# _pytz_tzinfo = Union[pytz.tzinfo.StaticTzInfo, pytz.tzinfo.DstTzInfo]


def parse_dt(dt_str: str) -> datetime.datetime:
    """
    Convert datetime in string form to datetime object.

    dt_str: Input datetime as a string in %Y-%m-%d %H:%M:%S format.
    'now' indicates local time.

    Returns datetime.datetime
    """
    dt_str = dt_str.strip().lower()
    if dt_str == 'now':
        dt = datetime.datetime.now()
    else:
        dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    return dt


def parse_tz(tz_str: str):
    """
    Converts time zone name to corresponding to pytz timezone.

    tz_str: Name of timezone
    'local' indicates local timezone

    Returns pytz timezone
    """
    tz_str = tz_str.strip().lower()
    if tz_str == 'local':
        return tzlocal.get_localzone()
    return pytz.timezone(tz_str)


def tzview(dt: datetime.datetime,
           from_tz,
           to_tzs: list) -> List[datetime.datetime]:
    """
    dt: datetime to be converted.
    from_tz: the time zone in which dt is.
    to_tzs: list of tzs to which dt should be converted.

    Accepts source time and timezone along with a list of timezones to
    which it should be converted to.

    Returns list of tz aware converted datetimes.
    """
    to_dts = []
    from_dt = from_tz.localize(dt)
    for to_tz in to_tzs:
        to_dt = from_dt.astimezone(to_tz)
        to_dts.append(to_dt)
    return to_dts
