from datetime import datetime

import pandas as pd

from vf_forecaster.data.time_series import IntervalDataSelector


def test_date_based_data_selector():
    # Create test data with 2 columns: ds and y
    dates = pd.date_range(start='2019-1-1', end='2019-12-31')
    data_df = pd.Series(index=dates, data=[1.0] * len(dates), name='y')\
        .to_frame()\
        .rename_axis('ds')\
        .reset_index()

    selector = IntervalDataSelector(
        data_df,
        history_start=datetime(2019, 1, 1),
        forecast_start=datetime(2019, 6, 30),
        forecast_end=datetime(2019, 12, 31)
    )

    train_df = selector.get_training_data()

    # Check the start and end dates of the slice
    assert train_df.ds.min().to_pydatetime() == datetime(2019, 1, 1)
    assert train_df.ds.max().to_pydatetime() == datetime(2019, 6, 29)

    start, end = selector.get_forecast_interval()
    assert start == datetime(2019, 6, 30)
    assert end == datetime(2019, 12, 31)
