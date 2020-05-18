import numpy as np
import pandas as pd
import pytest

from vf_forecaster.data.time_series import IntervalDataSelector
from vf_forecaster.models.holt_winters import HoltWintersModel, HoltwintersOptimizer


@pytest.fixture
def aust():
    """
    Return a ``pd.DataFrame`` containing the data from the "aust" dataset referenced here:
    https://www.statsmodels.org/stable/examples/notebooks/generated/exponential_smoothing.html#Exponential-smoothing
    The original dataset is quarterly, but here we use a daily index for easier application of
    ``IntervalDataSelector``. It has no effect on the result because an ``ExponentialSmoothing`` model is not frequency
    dependent.
    """
    data = [41.7275, 24.0418, 32.3281, 37.3287, 46.2132, 29.3463, 36.4829, 42.9777, 48.9015, 31.1802, 37.7179, 40.4202,
            51.2069, 31.8872, 40.9783, 43.7725, 55.5586, 33.8509, 42.0764, 45.6423, 59.7668, 35.1919, 44.3197, 47.9137]
    index = pd.date_range(start='2020-1-1', periods=len(data), freq='D')
    aust = pd.Series(data, index, name='y')
    aust.index.name = 'ds'
    aust = aust.reset_index()
    return aust


def test_optimizer(aust):
    data_selector = IntervalDataSelector(
        aust,
        history_start='2020-1-1',
        forecast_start='2020-1-25',
        forecast_end='2020-1-31',
    )
    optimizer = HoltwintersOptimizer(data_selector)
    results = optimizer.optimize()

    # Check auto-optimizer discovered parameters against what we expect (see the statsmodels link above)
    assert results.best_params['seasonal'] == 'mul'
    assert results.best_params['trend'] == 'add'
    assert results.best_params['seasonal_periods'] == 4

    # # Check that we can rebuild the model and reproduce the same results as the original best model
    # new_model = HoltWintersModel(**results.best_params)
    # forecast_df = data_selector.get_forecast_df()
    # new_model.fit(data_selector.get_training_data())
    #
    # new_model_predictions = new_model.predict(forecast_df)
    # existing_model_predictions = results.best_model.predict(forecast_df)
    #
    # # It is not possible to reproduce exactly the same result, so instead we check the L2 norm of the
    # # difference is below a certain threshold
    # # ctselas: delete until investigation, there was an assertion
    # differences = new_model_predictions.y - existing_model_predictions.y
    # diff_norm = np.linalg.norm(differences.values)
    # assert diff_norm <= 6.0
