import pandas as pd
from datetime import datetime
import numpy as np


def get_returns(cur_price: float, base_price: float):
    return (cur_price - base_price) / base_price


def get_annualized_returns(start_date: datetime, end_date: datetime, returns: float):
    years = get_delta_year(start_date, end_date)
    if years == 0:
        return np.nan
    return (1 + returns) ** (1 / years) - 1


def get_delta_year(start_date: datetime, end_date: datetime):
    """
    1년 365일 기준
    4년(1460) 초과시마다 하루 씩 제외
    """
    time_delta = end_date - start_date

    leaps = int(time_delta.days / 1460)
    years = (time_delta.days - leaps) / 365
    return years


def convert_values_to_cumulative_returns(value_series: pd.Series) -> pd.Series:
    cumulative_returns = value_series.pct_change().add(1).cumprod() - 1
    return cumulative_returns
