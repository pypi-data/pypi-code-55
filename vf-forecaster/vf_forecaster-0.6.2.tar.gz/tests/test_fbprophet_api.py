import os

import numpy as np
import pandas as pd
import pytest
from fbprophet import Prophet
from sklearn.metrics import mean_squared_error as mse

from utils import suppress_stdout_stderr


@pytest.fixture
def ts():
    df = pd.read_csv(
        os.path.join(os.path.dirname(__file__), 'test_data', 'air_passenger.csv'),
        parse_dates=True
    )
    yield df


def test_prophet_with_default_args(ts):
    """Construct a prophet model with default args."""
    model = Prophet()

    # train on all but last 4 observations
    train_ts = ts.iloc[:-5]
    with suppress_stdout_stderr():
        model.fit(train_ts)

    # predict on the last 4 observations
    future_df = model.make_future_dataframe(periods=4, freq='MS')
    predictions = model.predict(future_df).\
        assign(y=ts.y).\
        set_index('ds').\
        truncate(before=train_ts.ds.max()).\
        sort_index(axis=1)

    # Prophet relies on Pystan - the random seed used by Pystan is not exposed, so we cannot reproduce the same result
    # So we'll calculate MSE and expect it to be within a certain boundary
    actual_mse = mse(predictions.y.values, predictions.yhat.values)
    assert 2940 < actual_mse < 2960

    # Only expect yearly seasonality
    assert model.seasonalities['yearly']['fourier_order'] == 10
    assert 'monthly' not in model.seasonalities
    assert 'weekly' not in model.seasonalities

    # expect additive seasonality
    assert not np.all(predictions.additive_terms == 0)
    assert np.all(predictions.multiplicative_terms == 0)


def test_prophet_with_multiplicative_seasonality(ts):
    model = Prophet(seasonality_mode='multiplicative')

    # train on all but last 4 observations
    train_ts = ts.iloc[:-5]

    with suppress_stdout_stderr():
        model.fit(train_ts)

    # predict on the last 4 observations
    future_df = model.make_future_dataframe(periods=4, freq='MS')
    predictions = model.predict(future_df). \
        assign(y=ts.y). \
        set_index('ds'). \
        truncate(before=train_ts.ds.max()). \
        sort_index(axis=1)

    # Prophet relies on Pystan - the random seed used by Pystan is not exposed, so we cannot reproduce the same result
    # So we'll calculate MSE and expect it to be within a certain boundary
    actual_mse = mse(predictions.y.values, predictions.yhat.values)
    assert 410 < actual_mse < 430

    # expect multiplicative seasonality
    assert np.all(predictions.additive_terms == 0)
    assert not np.all(predictions.multiplicative_terms == 0)


def test_prophet_with_logistic_growth_and_cap_and_floor(ts):
    cap, floor = 350, 100
    model = Prophet(growth='logistic')

    # train on all but last 4 observations using no capacity restriction
    train_ts = ts.iloc[:-5].copy().assign(cap=1E10, floor=0)

    with suppress_stdout_stderr():
        model.fit(train_ts)

    # predict on the last 4 observations
    future_df = model.make_future_dataframe(periods=4, freq='MS').assign(cap=1E10, floor=0)

    uncapped_predictions = model.predict(future_df). \
        assign(y=ts.y). \
        set_index('ds'). \
        truncate(before=train_ts.ds.max()). \
        sort_index(axis=1)

    # train on all but last 4 observation, this time with capacity restriction
    model = Prophet(growth='logistic')
    train_ts = ts.iloc[:-5].copy().assign(cap=cap, floor=floor)
    model.fit(train_ts)
    future_df = model.make_future_dataframe(periods=4, freq='MS').assign(cap=cap, floor=floor)

    capped_predictions = model.predict(future_df). \
        assign(y=ts.y). \
        set_index('ds'). \
        truncate(before=train_ts.ds.max()). \
        sort_index(axis=1)

    assert np.all(uncapped_predictions.yhat > capped_predictions.yhat)
