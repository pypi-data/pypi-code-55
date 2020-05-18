import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

from vf_forecaster.data.time_series import OptimizationResult
from vf_forecaster.models.base_model import TimeSeriesModel


class HoltWintersModel(TimeSeriesModel):

    @classmethod
    def param_space(cls):
        return {
            'trend': [None, 'add', 'mul'],
            'seasonal': [None, 'add', 'mul'],
            'seasonal_periods': list(range(2, 13)),
            'use_boxcox': [True, False],
        }

    def __init__(self,
                 trend=None,
                 seasonal=None,
                 seasonal_periods=0,
                 use_boxcox=False,
                 smoothing_level=None,
                 smoothing_slope=None,
                 smoothing_seasonal=None,
                 initial_level=None,
                 initial_slope=None,
                 remove_bias=False,
                 damping_slope=None
        ):

        self.trend = trend
        self.seasonal = seasonal
        self.seasonal_periods = seasonal_periods
        self.use_boxcox = use_boxcox
        self.smoothing_level = smoothing_level
        self.smoothing_slope = smoothing_slope
        self.smoothing_seasonal = smoothing_seasonal
        self.initial_level = initial_level
        self.initial_slope = initial_slope
        self.remove_bias = remove_bias
        self.damping_slope = damping_slope

        self._model = None
        self._results = None

    def aic(self):
        if not self._results:
            raise RuntimeError("'aic' called before 'fit'.")

        return self._results.aic

    def get_model(self):
        return self._model

    def fit(self, X, y=None):
        if isinstance(X, pd.DataFrame):
            X = X.set_index('ds').squeeze()

        self._model = ExponentialSmoothing(
            X,
            trend=self.trend,
            seasonal=self.seasonal,
            seasonal_periods=self.seasonal_periods
        )

        # If smoothing_slope is specified, do not use auto-optimization
        # This handles the case where during the auto-optimization, we want to
        # discover the exponential smoothing coefficients, but when we re-create
        # the model from existing parameters, we want to supply them ourselves.
        optimized = self.smoothing_level is None

        self._results = self._model.fit(
            optimized=optimized,
            smoothing_level=self.smoothing_level,
            smoothing_slope=self.smoothing_slope,
            smoothing_seasonal=self.smoothing_seasonal,
            damping_slope=self.damping_slope,
            remove_bias=self.remove_bias,
            use_boxcox=self.use_boxcox)

        return self

    def predict(self, X):
        if not self._model:
            raise RuntimeError("'predict' called before 'fit'.")

        from pprint import pprint
        pprint(self.params)

        if isinstance(X, pd.DataFrame):
            X = X.set_index('ds').squeeze()

        start = X.index[0]
        end = X.index[-1]
        preds = self._model.predict(self._results.params, start=start, end=end)
        preds = pd.Series(data=preds, index=X.index, name='y')
        preds.index.name = 'ds'
        return preds.reset_index()

    @property
    def params(self):
        return self._model.params

    @staticmethod
    def _get_tags():
        return {}


class HoltwintersOptimizer(object):
    """Return the optimal parameters and the best model for a Holt-Winters ``ExponentialSmoothing`` model.

    This version executes a simple grid search over the possible parameter space. These parameters are:

        * trend
        * seasonal
        * seasonal_periods
        * use_boxcox

    Note that the best parameters include other parameters such as the 3 exponential smoothing coefficients
    and initial values to reproduce the model as closely as possible.
    """

    def __init__(self, data_selector):
        self._data_selector = data_selector

    @property
    def data_selector(self):
        return self._data_selector

    def optimize(self):
        best_model = None

        param_space = HoltWintersModel.param_space()
        train_df = self.data_selector.get_training_data()

        for trend in param_space['trend']:
            for seasonal in param_space['seasonal']:
                for seasonal_periods in param_space['seasonal_periods']:
                    if not seasonal:
                        seasonal_periods = 0

                    for use_boxcox in param_space['use_boxcox']:

                        model = HoltWintersModel(
                            trend=trend,
                            seasonal=seasonal,
                            seasonal_periods=seasonal_periods,
                            use_boxcox=use_boxcox
                        )
                        model = model.fit(train_df)
                        if (not best_model) or (model.aic() < best_model.aic()):
                            best_model = model

        best_params = best_model.params.copy()
        # Remove params we can't plug back into the model
        best_params.pop('initial_seasons')
        best_params.pop('lamda')

        best_params['trend'] = best_model.trend
        best_params['seasonal'] = best_model.seasonal
        best_params['seasonal_periods'] = best_model.seasonal_periods

        result = OptimizationResult(best_model=best_model, best_params=best_params)
        return result
