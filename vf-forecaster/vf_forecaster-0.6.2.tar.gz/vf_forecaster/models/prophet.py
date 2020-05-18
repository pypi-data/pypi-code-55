import numpy as np
import scipy.stats as stats
from fbprophet import Prophet
from hyperopt import hp
from statsmodels.tools.eval_measures import aic

from utils import suppress_stdout_stderr
from vf_forecaster.models.base_model import TimeSeriesModel


class ProphetModel(TimeSeriesModel):

    def __init__(self, growth=None, seasonality_mode=None, changepoint_prior_scale=None, seasonality_prior_scale=None):
        self.growth = growth
        self.seasonality_mode = seasonality_mode
        self.changepoint_prior_scale = changepoint_prior_scale
        self.seasonality_prior_scale = seasonality_prior_scale

        self._model = None
        self.aic_value = None

    def param_space(self):
        space = {'growth': hp.choice('growth', ['linear', 'logistic']),
                 'seasonality_mode': hp.choice('seasonality_mode', ['multiplicative', 'additive']),
                 'changepoint_prior_scale': hp.uniform('changepoint_prior_scale', 0.001, 1),
                 'seasonality_prior_scale': hp.uniform('seasonality_prior_scale', 0.01, 1000)
                 }
        return space

    def get_model(self):
        return self._model

    def fit(self, X, *args, **kwargs):
        """
        Parameters
        ----------
        X: pd.DataFrame containing the history. Must have columns ds (date
            type) and y, the time series. If self.growth is 'logistic', then
            df must also have a column cap that specifies the capacity at
            each ds.
        *args: Additional arguments if y is needed
        **kwargs: Two integers (cap and floor), If 'growth'=='logistic'
        """
        y = args
        self._model = Prophet(
            growth=self.growth,
            seasonality_mode=self.seasonality_mode,
            changepoint_prior_scale=self.changepoint_prior_scale,
            seasonality_prior_scale=self.seasonality_prior_scale
        )

        for key, value in kwargs.items():
            X[key] = value * X['y'].max() if key == 'cap' else value * X['y'].min()

        with suppress_stdout_stderr():
            self._model = self._model.fit(X)
            # computes and keeps the performance of the model for later
            self.aic_value = self.aic_helper(X)
        return self

    def predict(self, X, **kwargs):
        for key, value in kwargs.items():
            X[key] = value * X['y'].max() if key == 'cap' else value * X['y'].min()
        return self._model.predict(X)

    def aic(self):
        return self.aic_value

    def aic_helper(self, X):
        # n_params = 0
        # for param in self._model.params:
        #     n_params += len(param) #the output is always 20
        n_params = 20
        n_observations = len(X)
        pred_x = self._model.predict(X)['yhat']

        sd = self._model.params['sigma_obs'] * self._model.y_scale
        ll = np.sum(stats.norm.logpdf(X['y'], loc=pred_x, scale=sd))
        aic_value = aic(ll, n_observations, n_params)
        return aic_value

    @staticmethod
    def _get_tags():
        return {}
