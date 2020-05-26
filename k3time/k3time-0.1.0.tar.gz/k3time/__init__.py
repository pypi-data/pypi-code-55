"""
Time convertion utils.

>>> parse('2017-01-24T07:51:59.000Z', 'iso')
datetime.datetime(2017, 1, 24, 7, 51, 59)
>>> format_ts(1485216000, 'iso')
'2017-01-24T00:00:00.000Z'
>>> format_ts(1485216000, '%Y-%m-%d')
'2017-01-24'

"""

from .tm import (
    formats,
    parse_to_ts,
    parse,
    format,
    format_ts,
    utc_datetime_to_ts,
    datetime_to_ts,
    ts_to_datetime,
    ts,
    ms,
    us,
    ns,
    ms_to_ts,
    us_to_ts,
    ns_to_ts,
    to_sec,
    is_timestamp,
)

__version__ = '0.1.0'
_name = 'k3time'
