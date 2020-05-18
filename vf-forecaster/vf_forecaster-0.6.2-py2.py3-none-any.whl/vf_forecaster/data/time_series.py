from abc import abstractmethod
from collections import namedtuple

import pandas as pd

OptimizationResult = namedtuple('OptimizationResult', ['best_model', 'best_params'])


class ForecastDataSelector(object):
    """
    Base class for provisioning input data for Forecasts.
    """

    @abstractmethod
    def get_training_data(self):
        """Return the dataset used to train a time series model."""
        raise NotImplementedError

    @abstractmethod
    def get_forecast_interval(self):
        """Return two ``datetime``s for the forecasting interval."""
        raise NotImplementedError


class IntervalDataSelector(ForecastDataSelector):
    """A ``ForecastDataSelector`` suitable for DFM forecasts.

    Given some training data, returns the slice between [``history_start``, ``forecast_start`` - 1D]
    as training data, and the slice between [``forecast_start``, ````forecast_end``] as forecast interval.
    """

    def __init__(self, data_df, history_start, forecast_start, forecast_end):
        assert 'ds' in data_df.columns
        assert 'y' in data_df.columns

        self._data_df = data_df

        assert history_start < forecast_start < forecast_end

        self._history_start = history_start
        self._forecast_start = forecast_start
        self._forecast_end = forecast_end

    @property
    def data_df(self):
        return self._data_df

    @property
    def history_start(self):
        return self._history_start

    @property
    def forecast_start(self):
        return self._forecast_start

    @property
    def forecast_end(self):
        return self._forecast_end

    def get_training_data(self):
        mask = (self.data_df.ds >= self.history_start) & (self.data_df.ds < self.forecast_start)
        train_df = self._data_df[mask].copy()
        return train_df

    def get_forecast_interval(self):
        return self.forecast_start, self.forecast_end

    def get_forecast_df(self):
        forecast_dates = pd.date_range(start=self.forecast_start, end=self.forecast_end, freq='D')
        forecast_df = pd.Series(data=forecast_dates.tolist(), name='ds').to_frame()
        return forecast_df
