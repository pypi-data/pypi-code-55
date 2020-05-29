import lightgbm as lgb

import numpy as np

from scipy.stats import uniform, randint

from sklearn.datasets import load_breast_cancer, load_diabetes, load_wine
from sklearn.metrics import auc, accuracy_score, confusion_matrix, mean_squared_error
from sklearn.model_selection import cross_val_score, GridSearchCV, KFold, RandomizedSearchCV, train_test_split
from sklearn.linear_model import Lasso
import xgboost as xgb
from sklearn import datasets, linear_model

from napoleontoolbox.forecasting import linear_model_wrapper
from napoleontoolbox.forecasting import lasso_model_wrapper
from napoleontoolbox.forecasting import lgbm_model_wrapper
from napoleontoolbox.forecasting import xgb_model_wrapper
from napoleontoolbox.forecasting import standard_mean_model_wrapper
from napoleontoolbox.forecasting import deterministic_sharpe_optim_model_wrapper
from napoleontoolbox.forecasting import  to_weighted_mean_model_wrapper

from abc import ABC, abstractmethod


def instantiate_model(method):
    if method == 'standard':
        return linear_model_wrapper.LinearModel()
    if method == 'lasso':
        return lasso_model_wrapper.LASSOModel()
#        alpha = 0.1
#        self.model = Lasso(alpha=alpha, fit_intercept=False, max_iter=5000)
    if method == 'lgbm':
        return lgbm_model_wrapper.LGBMModel()
    if method == 'xgb':
        return xgb_model_wrapper.XGBModel()
    if method == 'standard_mean':
        return standard_mean_model_wrapper.MeanModel()
    if method == 'to_weighted_mean':
        return to_weighted_mean_model_wrapper.WeightedMeanModel()
    if method == 'deterministic_sharpe_optim':
        return deterministic_sharpe_optim_model_wrapper.DeterministicSharpeOptimModel()



def report_best_scores(results, n_top=3):
    for i in range(1, n_top + 1):
        candidates = np.flatnonzero(results['rank_test_score'] == i)
        for candidate in candidates:
            print("Model with rank: {0}".format(i))
            print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
                  results['mean_test_score'][candidate],
                  results['std_test_score'][candidate]))
            print("Parameters: {0}".format(results['params'][candidate]))
            print("")

class AbstractForecasterWrapper(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def calibrate(self, X, y):#, method = 'standard'):
        pass

    @abstractmethod
    def fit(self, X_train, y_train, X_val, y_val):#, method = 'standard'):
        pass

    @abstractmethod
    def predict(self, X_test):#, method = 'standard'):
        pass

    @abstractmethod
    def get_features_importance(self, features_names):#, method = 'standard'):
        pass
