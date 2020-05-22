import calendar
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


# ======================= YEAR ================================================
def replace_year(dt, year):
    """Replace the year in ``dt`` by ``year``. If dt has the last day in the month, keep also the last day of the
    month for leap years

    :param dt:
    :type dt:
    :param year:
    :type year:
    :return:
    :rtype:
    """
    dt = pd.Timestamp(dt)
    if is_leap_day(dt):
        if calendar.isleap(year):
            dt0 = dt.replace(year=year)
        else:
            dt0 = dt.replace(year=year, day=28)
    else:
        if calendar.isleap(year) and dt.day == 28 and dt.month == 2:
            dt0 = dt.replace(year=year, day=29)
        else:
            dt0 = dt.replace(year=year)
    return dt0


def is_leap_day(dt):
    """Check whether ``dt`` is the 29.02

    :param dt: datetime
    :type dt: datetime, pd.Timestamp, np.datetime64
    :return: True/False
    :rtype: bool
    """
    dt = pd.Timestamp(dt)
    return dt.day == 29 and dt.month == 2


def last_day_of_month(dt):
    try:
        return [(pd.Timestamp(t) + pd.tseries.offsets.MonthEnd(n=0)).day for t in dt]
    except (TypeError, ValueError):
        return (pd.Timestamp(dt) + pd.tseries.offsets.MonthEnd(n=0)).day


def is_last_day_of_month(dt):
    """Check whether day in ``dt`` is the last day of the month
    :param dt: datetime
    :type dt: datetime, pd.Timestamp, np.datetime64
    :return: True/False
    :rtype: bool
    """
    return pd.Timestamp(dt).day == last_day_of_month(dt)


def increment_months(dt, months=1, microseconds=0):
    """Increment ``dt`` by ``months``. Default is to increment one month.
    Return a ``pd.Timestamp``.

    :param dt: timestamp
    :type dt: datetime, pd.Timestamp, np.datetime64
    :param months: number of months to increment. Negative values are allowed. Default months = 1
    :type months: int
    :param microseconds: microseconds to add to the right interval: 0 for closed, -1 for right opened interval
    :type microseconds: int
    :return: ts incremented by ``months``
    :rtype: pd.Timestamp
    """
    # Don't use pd.Timedelta:
    # pd.Timestamp('2000-12-30 07:30') + pd.Timedelta(1, unit='M') == Timestamp('2001-01-29 17:59:06')
    dt = pd.Timestamp(dt)
    ts1 = pd.Timestamp(dt.to_pydatetime() + relativedelta(months=months, microseconds=microseconds))
    if is_last_day_of_month(dt):
        return ts1.replace(day=1) + pd.tseries.offsets.MonthEnd(n=1)
    else:
        return ts1


def monthly_intervals(indices, months=None, aggregation=1, start_at='beg',
                      closed_left=True, closed_right=True):
    """Return a list of tuples [from, to], where the intervals correspond to the begin and end of
    aggregated months (default aggregation=1 means monthly intervals). The aggregation may be also negative.

    :param indices: sorted list of timestamps
    :type indices: pd.DatetimeIndex, list
    :param months: output months for the intervals
    :type months: None or list
    :param aggregation: number of aggregated months. Default 1 (monthly)
    :type aggregation: int
    :param start_at: date and time to start. Only day and time are used, year and month are only placeholders
        and will be discarded. start_at='end' for the end of the first month in the time series.
        start_at='beg' for the first day of the month at 00:00:00. start_at=None is equivalent to start_at='beg'
    :type start_at: datetime.datetime, str
    :param closed_left: left close interval
    :type closed_left: bool
    :param closed_right: right close interval
    :type closed_right: bool
    :return: list of intervals [[begin0, end0], [begin1, end1], ..., [beginN, endN]]
    :rtype: list of [pd.Timestamp, pd.Timestamp]

    For the examples below the following `indices` will be used:

    .. code-block::

        >>> import numpy as np
        >>> import pandas as pd
        >>> from caeli.time_series import monthly_intervals
        >>> index = pd.date_range('1990-01-01 07:30', '2020-01-01 07:30', freq='1d')
        >>> index
        DatetimeIndex(['1990-01-01 07:30:00', '1990-01-02 07:30:00',
                       '1990-01-03 07:30:00', '1990-01-04 07:30:00',
                       '1990-01-05 07:30:00', '1990-01-06 07:30:00',
                       '1990-01-07 07:30:00', '1990-01-08 07:30:00',
                       '1990-01-09 07:30:00', '1990-01-10 07:30:00',
                       ...
                       '2019-12-23 07:30:00', '2019-12-24 07:30:00',
                       '2019-12-25 07:30:00', '2019-12-26 07:30:00',
                       '2019-12-27 07:30:00', '2019-12-28 07:30:00',
                       '2019-12-29 07:30:00', '2019-12-30 07:30:00',
                       '2019-12-31 07:30:00', '2020-01-01 07:30:00'],
                      dtype='datetime64[ns]', length=10958, freq='D')

    Examples:

    Using default values. Note that the time series starts at 07:30 but as per default the month starts at 00:00.
    Therefore, the first month is ignored.

    .. code-block::

        >>> itv = monthly_intervals(index, months=None, aggregation=1, start_at='beg',
                                   closed_left=True, closed_right=True)
        >>> print('{}, ..., {}'.format(itv[0], itv[-1]))
        [Timestamp('1990-02-01 00:00:00'), Timestamp('1990-03-01 00:00:00')], ...,
        [Timestamp('2019-12-01 00:00:00'), Timestamp('2020-01-01 00:00:00')]

    Setting start_at=1999-01-01 07:30'. YYYY-MM ('1999-01') is a place holder.

    .. code-block::

        >>> itv = monthly_intervals(index, months=None, aggregation=1, start_at='1999-01-01 07:30',
                                   closed_left=True, closed_right=True)
        >>> print('{}, ..., {}'.format(itv[0], itv[-1]))
        [Timestamp('1990-01-01 07:30:00'), Timestamp('1990-02-01 07:30:00')], ...,
        [Timestamp('2019-12-01 07:30:00'), Timestamp('2020-01-01 07:30:00')]

    closed_right=False.

    .. code-block::

        >>> itv = monthly_intervals(index, months=None, aggregation=1, start_at='1999-01-01 07:30',
                                   closed_left=True, closed_right=False)
        >>> print('{}, ..., {}'.format(itv[0], itv[-1]))
        [Timestamp('1990-01-01 07:30:00'), Timestamp('1990-02-01 07:29:59.999999')], ...,
        [Timestamp('2019-12-01 07:30:00'), Timestamp('2020-01-01 07:29:59.999999')]

    aggregation=2.

    .. code-block::

        >>> itv = monthly_intervals(index, months=None, aggregation=2, start_at='1999-01-01 07:30',
                                   closed_left=True, closed_right=False)
        >>> print('{}, ..., {}'.format(itv[0], itv[-1]))
        [Timestamp('1990-01-01 07:30:00'), Timestamp('1990-03-01 07:29:59.999999')], ...,
        [Timestamp('2019-11-01 07:30:00'), Timestamp('2020-01-01 07:29:59.999999')]

    months=[1, 4, 7, 10].

    .. code-block::

        >>> itv = monthly_intervals(index, months=[1, 4, 7, 10], aggregation=3,
                                   start_at='1999-01-01 07:30', closed_left=True, closed_right=False)
        >>> itv[:5]
        [[Timestamp('1990-01-01 07:30:00'), Timestamp('1990-04-01 07:29:59.999999')],
        [Timestamp('1990-04-01 07:30:00'), Timestamp('1990-07-01 07:29:59.999999')],
        [Timestamp('1990-07-01 07:30:00'), Timestamp('1990-10-01 07:29:59.999999')],
        [Timestamp('1990-10-01 07:30:00'), Timestamp('1991-01-01 07:29:59.999999')],
        [Timestamp('1991-01-01 07:30:00'), Timestamp('1991-04-01 07:29:59.999999')]]

    Negative aggregation (aggregation=-3). Note that the first aggregation
    [1989-12-31 07:30:00, 1990-02-01 07:29:59.999999] is ignored because the time series starts at 1990-01-01 07:30:00.

    .. code-block::

        >>> itv = monthly_intervals(index, months=[2, 5, 8, 11], aggregation=-3,
                                   start_at='1999-01-01 07:30', closed_left=True, closed_right=False)
        >>> itv[:5]
        [[Timestamp('1990-02-01 07:30:00'), Timestamp('1990-05-01 07:29:59.999999')],
        [Timestamp('1990-05-01 07:30:00'), Timestamp('1990-08-01 07:29:59.999999')],
        [Timestamp('1990-08-01 07:30:00'), Timestamp('1990-11-01 07:29:59.999999')],
        [Timestamp('1990-11-01 07:30:00'), Timestamp('1991-02-01 07:29:59.999999')],
        [Timestamp('1991-02-01 07:30:00'), Timestamp('1991-05-01 07:29:59.999999')]]

    """
    if not months:
        months = range(1, 13)
    index0 = indices[0]
    index1 = indices[-1]
    if start_at is None or start_at == 'beg':
        start_at = datetime(index0.year, index0.month, 1, 0, 0, 0, 0)
    elif start_at == 'end':
        start_at = increment_months(index0).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        index1 = increment_months(index1).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if aggregation < 0:
        index1 = increment_months(index1, aggregation)
    ts0 = replace_year(start_at, index0.year)
    tuples = list()
    while ts0 <= index1:
        if ts0.month in months:
            inc = increment_months(ts0, aggregation)
            tuples.append([ts0, inc] if aggregation > 0 else [inc, ts0])
        ts0 = increment_months(ts0, 1)
    if not closed_right:
        tuples = [[ts0, ts1 - pd.Timedelta(1, unit='us')] for ts0, ts1 in tuples]
    if not closed_left:
        tuples = [[ts0 + pd.Timedelta(1, unit='us'), ts1] for ts0, ts1 in tuples]
    while tuples[0][0] < index0:
        tuples = tuples[1:]
    while tuples[-1][1].replace(hour=0, minute=0, second=0, microsecond=0) > index1:
        tuples = tuples[:-1]
    return tuples


def monthly_series(sr, rule='sum', months=None, aggregation=1, start_at=None,
                   closed_left=True, closed_right=False, label='right',
                   is_sorted=False, time_format='d'):
    """Return the series resampled to the months listed in ``months``,
    taking ``accum`` adjacent months. The default resampling rule is ``sum``.

    :param sr: pandas.Series with DateTimeIndex as index. The series at any frequency will be aggregated to month(s)
    :type sr: pandas.Series, pandas.DataFrame
    :param rule: resample rule. Default *rule='sum'*
    :type rule: str
    :param months: see :func:`monthly_intervals`
    :param aggregation: see :func:`monthly_intervals`
    :param start_at: see :func:`monthly_intervals`
    :param closed_left: see :func:`monthly_intervals`
    :param closed_right: see :func:`monthly_intervals`
    :param label: 'right' for setting the index at the end and 'left' for setting the index at the begin of the
        interval in the time series. Default label='right'
    :type label: str
    :param is_sorted: True if the input time series is alredy sorted, otherwise False. Default is_sorted = False
    :type is_sorted: bool
    :param time_format: 'd' (day/date): round hour, minute, sencond, and milliseconds to 0; 'h' (hour): round minute,
        second, and milliseconds to 0, 'm' (minute)': round second and milliseconds to 0, 's' (second): round
        milliseconds to 0; None: do not round anything
    :type time_format: str, None
    :return: (**pandas.DataFrame, pandas.Series**): monthly time series

    For the examples below the following time series will be used:

    .. code-block::

        >>> import numpy as np
        >>> import pandas as pd
        >>> from caeli.time_series import monthly_series
        >>> np.random.seed(1)
        >>> index = pd.date_range('1990-01-01 07:30', '2020-01-01 07:30', freq='1d')
        >>> p = np.random.normal(2, 0.1, size=len(index))
        >>> p[p < 0.0] = 0.0
        >>> sr_daily = pd.Series(p, index=index)
        >>> sr_daily
        1990-01-01 07:30:00    2.162435
        1990-01-02 07:30:00    1.938824
                                 ...
        2019-12-31 07:30:00    1.937972
        2020-01-01 07:30:00    2.081355
        Freq: D, Length: 10958, dtype: float64

    Right labeled, showing date only:

    .. code-block::

        >>> sr_monthly = monthly_series(sr_daily, aggregation=2, start_at='1999-01-01 07:30')
        >>> sr_monthly
        1990-03-01    117.961372
        1990-04-01    118.789945
                         ...
        2019-12-01    122.096353
        2020-01-01    123.361334
        Length: 359, dtype: float64

    Right labeled, showing the full date/time:

    .. code-block::

        >>> sr_monthly = monthly_series(sr_daily, aggregation=2, start_at='1999-01-01 07:30',
                                        time_format=None)
        >>> sr_monthly
        1990-03-01 07:29:59.999999    117.961372
        1990-04-01 07:29:59.999999    118.789945
                                         ...
        2019-12-01 07:29:59.999999    122.096353
        2020-01-01 07:29:59.999999    123.361334
        Length: 359, dtype: float64

    Left labeled, showing date only:

    .. code-block::

        >>> sr_monthly = monthly_series(sr_daily, aggregation=2, start_at='1999-01-01 07:30',
                                        label='left')
        >>> sr_monthly
        1990-01-01    117.961372
        1990-02-01    118.789945
                         ...
        2019-10-01    122.096353
        2019-11-01    123.361334
        Length: 359, dtype: float64

    Left labeled, showing the full date/time:

    .. code-block::

        >>> sr_monthly = monthly_series(sr_daily, aggregation=2, start_at='1999-01-01 07:30',
                                        label='left', time_format=None)
        >>> sr_monthly
        1990-01-01 07:30:00    117.961372
        1990-02-01 07:30:00    118.789945
                                  ...
        2019-10-01 07:30:00    122.096353
        2019-11-01 07:30:00    123.361334
        Length: 359, dtype: float64

    """
    if not is_sorted:
        sr = sr.sort_index()
    idx = 1 if label == 'right' else 0
    intervals_list = monthly_intervals(sr.index, months=months, aggregation=aggregation, start_at=start_at,
                                       closed_left=closed_left, closed_right=closed_right)
    tdf = []
    for beg_end in intervals_list:
        value = getattr(slice_by_timestamp(sr, beg_end[0], beg_end[1]), rule)()
        tdf.append([beg_end[idx], value])
    tdf = list(zip(*tdf))
    try:
        sr1 = pd.concat(tdf[1][:], axis=1).transpose().set_index(pd.DatetimeIndex(tdf[0]))
    except TypeError:
        sr1 = pd.Series(tdf[1], index=tdf[0])
        sr1.name = sr.name
    if time_format == 'd':
        sr1.index = sr1.index.map(lambda t: t.replace(hour=0, minute=0, second=0, microsecond=0))
    elif time_format == 'h':
        sr1.index = sr1.index.map(lambda t: t.replace(minute=0, second=0, microsecond=0))
    elif time_format == 'm':
        sr1.index = sr1.index.map(lambda t: t.replace(second=0, microsecond=0))
    elif time_format == 's':
        sr1.index = sr1.index.map(lambda t: t.replace(microsecond=0))
    return sr1


def months_split_annually(sr, rule='sum', months=None, aggregation=1, start_at=None,
                          closed_left=True, closed_right=False, label='left',
                          is_sorted=False, time_format='d', prefix='M'):
    """Return a pandas.DataFrame with aggregated months as columns and year as index.

    :param sr: pandas.Series with DateTimeIndex as index
    :type sr: pandas.Series or pandas.DataFrame
    :param rule: see :func:`monthly_series`
    :param months: see :func:`monthly_intervals`
    :param aggregation: see :func:`monthly_intervals`
    :param start_at: see :func:`monthly_intervals`
    :param closed_left: see :func:`monthly_intervals`
    :param closed_right: see :func:`monthly_intervals`
    :param label: see :func:`monthly_intervals`
    :param is_sorted: see :func:`monthly_intervals`
    :param time_format:  see :func:`monthly_intervals`
    :param prefix: Prefix for columns names. Default prefix='M'
    :type prefix: str
    :return: (**pandas.DataFrame**) with aggregated months as columns and year as index

    For the examples below the following time series will be used:

    .. code-block::

        >>> import numpy as np
        >>> import pandas as pd
        >>> from caeli.time_series import months_split_annually
        >>> np.random.seed(1)
        >>> index = pd.date_range('1990-01-01 07:30', '2020-01-01 07:30', freq='1d')
        >>> p = np.random.normal(2, 0.1, size=len(index))
        >>> p[p < 0.0] = 0.0
        >>> sr_daily = pd.Series(p, index=index)
        >>> sr_daily
        1990-01-01 07:30:00    2.162435
        1990-01-02 07:30:00    1.938824
                                 ...
        2019-12-31 07:30:00    1.937972
        2020-01-01 07:30:00    2.081355
        Freq: D, Length: 10958, dtype: float64

    .. code-block::

        >>> spy = months_split_annually(sr_daily, aggregation=2, start_at='1999-01-01 07:30')
        >>> print(spy)
                  M01-02      M02-03  ...      M11-12      M12-01
        year                          ...
        1990  117.961372  118.789945  ...  121.819112  123.028979
        1991  117.760247  118.953375  ...  121.958717  123.601324
        ...          ...         ...  ...         ...         ...
        2018  117.549323  117.780231  ...  121.336530  122.549497
        2019  116.797959  117.721573  ...  123.361334         NaN

        [30 rows x 12 columns]
                  M01-02      M02-03  ...      M11-12      M12-01
        year                          ...
        1990  117.961372  118.789945  ...  121.819112  123.028979
        1991  117.760247  118.953375  ...  121.958717  123.601324
        ...          ...         ...  ...         ...         ...
        2018  117.549323  117.780231  ...  121.336530  122.549497
        2019  116.797959  117.721573  ...  123.361334         NaN

        [30 rows x 12 columns]
    """
    if not months:
        months = range(1, 13)
    df = monthly_series(sr, rule=rule, months=months, aggregation=aggregation, start_at=start_at,
                        closed_left=closed_left, closed_right=closed_right, label=label,
                        is_sorted=is_sorted, time_format=time_format)
    try:
        df = df.to_frame()
    except AttributeError:
        pass
    name = df.columns[0]
    df['month'] = df.index.month
    df['year'] = df.index.year
    df1 = df.pivot(index='year', columns='month', values=name)
    months1 = list(range(1, 13))
    if aggregation > 1:
        columns = ['{}{}-{}'.format(prefix, str(m).zfill(2),
                                    str(months1[(m + aggregation - 2) % 12]).zfill(2)) for m in months]
    elif aggregation < 1:
        columns = ['{}{}-{}'.format(prefix, str(months1[(m + aggregation) % 12]).zfill(2),
                                    str(m).zfill(2)) for m in months]
    else:
        columns = ['{}{}'.format(prefix, str(m).zfill(2)) for m in months]
    df1.columns = columns
    return df1


def slice_by_timestamp(df, beg_timestamp=pd.Timestamp.min, end_timestamp=pd.Timestamp.max):
    """Slice the data frame from index starting at beg_timestamp to end_timestamp, including the latter.

    :param df: data frame
    :type df: pandas.DataFrame or pandas.Series
    :param beg_timestamp: begin of slice
    :type beg_timestamp: datetime.datetime, pandas.timestamp, or numpy.datetime64
    :param end_timestamp: end of slice (inclusive)
    :type end_timestamp: datetime.datetime, pandas.timestamp, or numpy.datetime64
    :return: (**pandas.DataFrame or pandas.Series**) sliced data frame
    """
    beg = df.index.searchsorted(beg_timestamp, side='left')
    end = df.index.searchsorted(end_timestamp, side='right')
    return df.iloc[beg:end]
