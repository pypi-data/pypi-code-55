import warnings

import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.exceptions import ConvergenceWarning, NotFittedError

from amicrt.utils import monteCarloEntropy

warnings.filterwarnings("ignore", category=ConvergenceWarning)

class TestStatistic(object):
    def __init__(self, j=None, name=None):
        self.j = j
        if name is not None:
            self.name = name
        else:
            self.name = 'TestStatistic'

    def fit(self, x, y):
        raise NotImplementedError('.fit() method not implemented')

    def score(self, x, y):
        raise NotImplementedError('.score() method not implemented')

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        print(self.__repr__())


class ModelBasedStatistic(TestStatistic):
    """
    modelClass must implement scikit-learn model interface
    or at the very least include these methods:
        - fit
        - predict
        - predict_proba
        - predict_log_proba
    """

    def __init__(self,
                 modelClass=RandomForestClassifier,
                 modelArgs=dict(n_estimators=10),
                 fn=monteCarloEntropy,
                 j=None,
                 name=None):
        super(ModelBasedStatistic, self).__init__(
            f"{'ModelBasedStatistic' if name is None else name}")
        self.modelClass = modelClass
        self.modelArgs = modelArgs
        self.isFit = False
        self.fn = fn
        self.j = j

    def fit(self, x, y):
        np.random.seed(int.from_bytes(os.urandom(4), byteorder='little'))
        self.model = self.modelClass(**self.modelArgs)
        self.model.fit(x, y)
        self.isFit = True
        return self

    def score(self, x, y):
        if not self.isFit:
            raise NotFittedError('Model-based statistic must be fit first.')
        return self.fn(self.model, x, y)


class CorrelationStatistic(TestStatistic):
    def __init__(self, j, name=None):
        super(CorrelationStatistic,
              self).__init__(f'CorrelationStatistic({j})')
        self.j = j

    def fit(self, x, y):
        return self

    def score(self, x, y):
        return np.corrcoef(x[:, self.j], y)[0, 1]
