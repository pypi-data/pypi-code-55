import pandas
from pandas import DataFrame

from athena.patch.statsd_config import DEFAULT_STATSD_CLIENT as STATSD_CLIENT

_read_parquet = pandas.read_parquet
_to_parquet = DataFrame.to_parquet
_merge = pandas.merge
_groupby = DataFrame.groupby

pandas_string = "pandas.."


def read_parquet_patched(*args, **kwargs):
    """
    New read_parquet function
    """
    with STATSD_CLIENT.timer(f"{pandas_string}read_parquet"):
        return _read_parquet(*args, **kwargs)


def to_parquet_patched(*args, **kwargs):
    """
    New to_parquet function
    """
    with STATSD_CLIENT.timer(f"{pandas_string}to_parquet"):
        return _to_parquet(*args, **kwargs)


def merge_patched(*args, **kwargs):
    """
    New merge function
    """
    with STATSD_CLIENT.timer(f"{pandas_string}merge"):
        return _merge(*args, **kwargs)


def dataframe_groupby_patched(*args, **kwargs):
    """
    New read parquet function
    """
    with STATSD_CLIENT.timer(f"{pandas_string}df_groupby"):
        return _groupby(*args, **kwargs)


def patch():
    pandas.read_parquet = read_parquet_patched
    DataFrame.to_parquet = to_parquet_patched
    pandas.merge = merge_patched
    DataFrame.groupby = dataframe_groupby_patched
