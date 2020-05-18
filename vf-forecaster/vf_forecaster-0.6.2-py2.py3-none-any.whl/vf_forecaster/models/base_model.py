from abc import abstractmethod

from sklearn.base import BaseEstimator, RegressorMixin


class TimeSeriesModel(BaseEstimator, RegressorMixin):
    """
    Base class of a Time Series Forecaster.
    """

    @abstractmethod
    def param_space(self):
        """Return the space of parameters Hyperopt will use to search for auto-optimization."""
        pass

    @abstractmethod
    def aic(self):
        """Return the AIC of an already fit model."""
        pass

    @abstractmethod
    def get_model(self):
        """Return the underlying model object. Note that this may not exist before fitting."""
        pass
