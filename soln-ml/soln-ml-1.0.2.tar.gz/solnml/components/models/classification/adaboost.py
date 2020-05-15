import numpy as np
from ConfigSpace.configuration_space import ConfigurationSpace
from ConfigSpace.hyperparameters import UniformFloatHyperparameter, \
    UniformIntegerHyperparameter, CategoricalHyperparameter

from solnml.components.models.base_model import BaseClassificationModel
from solnml.components.utils.constants import DENSE, SPARSE, UNSIGNED_DATA, PREDICTIONS


class AdaboostClassifier(BaseClassificationModel):

    def __init__(self, n_estimators, learning_rate, algorithm, max_depth,
                 random_state=None):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.algorithm = algorithm
        self.random_state = random_state
        self.max_depth = max_depth
        self.estimator = None
        self.time_limit = None

    def fit(self, X, Y, sample_weight=None):
        import sklearn.tree

        self.n_estimators = int(self.n_estimators)
        self.learning_rate = float(self.learning_rate)
        self.max_depth = int(self.max_depth)
        base_estimator = sklearn.tree.DecisionTreeClassifier(max_depth=self.max_depth)

        estimator = sklearn.ensemble.AdaBoostClassifier(
            base_estimator=base_estimator,
            n_estimators=self.n_estimators,
            learning_rate=self.learning_rate,
            algorithm=self.algorithm,
            random_state=self.random_state
        )

        estimator.fit(X, Y, sample_weight=sample_weight)

        self.estimator = estimator
        return self

    def predict(self, X):
        if self.estimator is None:
            raise NotImplementedError
        return self.estimator.predict(X)

    def predict_proba(self, X):
        if self.estimator is None:
            raise NotImplementedError()
        return self.estimator.predict_proba(X)

    @staticmethod
    def get_properties(dataset_properties=None):
        return {'shortname': 'AB',
                'name': 'AdaBoost Classifier',
                'handles_regression': False,
                'handles_classification': True,
                'handles_multiclass': True,
                'handles_multilabel': False,
                'is_deterministic': True,
                'input': (DENSE, SPARSE, UNSIGNED_DATA),
                'output': (PREDICTIONS,)}

    @staticmethod
    def get_hyperparameter_search_space(dataset_properties=None, optimizer='smac'):
        if optimizer == 'smac':
            cs = ConfigurationSpace()
            n_estimators = UniformIntegerHyperparameter(
                name="n_estimators", lower=50, upper=500, default_value=50, log=False)
            learning_rate = UniformFloatHyperparameter(
                name="learning_rate", lower=0.01, upper=2, default_value=0.1, log=True)
            algorithm = CategoricalHyperparameter(
                name="algorithm", choices=["SAMME.R", "SAMME"], default_value="SAMME.R")
            max_depth = UniformIntegerHyperparameter(
                name="max_depth", lower=1, upper=10, default_value=1, log=False)
            cs.add_hyperparameters([n_estimators, learning_rate, algorithm, max_depth])
            return cs
        elif optimizer == 'tpe':
            from hyperopt import hp
            space = {'n_estimators': hp.randint('ab_n_estimators', 451) + 50,
                     'learning_rate': hp.loguniform('ab_learning_rate', np.log(0.01), np.log(2)),
                     'algorithm': hp.choice('ab_algorithm', ["SAMME.R", "SAMME"]),
                     'max_depth': hp.randint('ab_max_depth', 10) + 1}

            init_trial = {'n_estimators': 50, 'learning_rate': 0.1, 'algorithm': "SAMME.R", 'max_depth': 1}
            return space
