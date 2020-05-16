import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from regression_model.processing.errors import InvalidModelInputError
from regression_model.processing.solar_calculation_functions import *

class WindDiscretizer(BaseEstimator, TransformerMixin):
    '''Discretization of Wind'''
    def __init__(self, variables=None):
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        buckets = np.arange(11.25, 372, 22.5)
        labels = np.arange(17)
        for feature in self.variables:
            X[feature].loc[(X[feature]>=0)&(X[feature]<11.25)] = X[feature].loc[(X[feature]>=0)&(X[feature]<11.25)].apply(lambda x:x+360)
            X[feature]=labels[np.digitize(X[feature], buckets)]
        return X

class DiscretizerNumericalIntoBinary(BaseEstimator, TransformerMixin):
    '''Discretization of cloud coverage and precipitation intensity into
        binary. The function takes a dictionary of variables as boundaries.
    '''

    def __init__(self, boundaries=None, variables=None):
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables
        self.boundaries=boundaries

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        for feature in self.variables:
            X[feature] = np.where(X[feature]>self.boundaries[feature],1,0)
        return X

class TemporalHour(BaseEstimator, TransformerMixin):
        def __init__(self, variable=None, ref_feature=None):
            self.variable = variable
            self.ref_feature = ref_feature
            #can make one temporal transformer for both issues
            #dict with lambda?

        def fit(self, X, y=None):
            return self

        def transform(self, X):
            X = X.copy()
            X[self.variable] = pd.DatetimeIndex(pd.to_datetime(X[self.ref_feature])).hour
            return X

class TemporalDayofYear(BaseEstimator, TransformerMixin):
        def __init__(self, variable=None, ref_feature=None):
            self.variable = variable
            self.ref_feature = ref_feature

        def fit(self, X, y=None):
            return self

        def transform(self, X):
            X = X.copy()
            X[self.variable] = pd.DatetimeIndex(pd.to_datetime(X[self.ref_feature])).dayofyear
            return X

class SolarElevAngle(BaseEstimator, TransformerMixin):
        def __init__(self, var_name=None, day=None, hour=None):
            self.var_name = var_name
            self.day = day
            self.hour = hour

        def fit(self, X, y=None):
            return self

        def transform(self, X):
            X = X.copy()
            X[self.var_name] = X.apply(lambda x: calc_alpha_s_for_df(N=x[self.day],time=x[self.hour]),axis=1)

            return X

class SunAzimuth(BaseEstimator, TransformerMixin):
        def __init__(self, var_name=None, day=None, hour=None):
            self.var_name = var_name
            self.day = day
            self.hour = hour

        def fit(self, X, y=None):
            return self

        def transform(self, X):
            X = X.copy()
            X[self.var_name] = X.apply(lambda x: calc_sun_azimuth_for_df(N=x[self.day],time=x[self.hour]),axis=1)

            return X

class TheoreticalRadiation(BaseEstimator, TransformerMixin):
        def __init__(self, var_name=None, day=None, hour=None):
            self.var_name = var_name
            self.day = day
            self.hour = hour

        def fit(self, X, y=None):
            return self

        def transform(self, X):
            X = X.copy()
            X[self.var_name] = X.apply(lambda x: calc_glob_irrad(N=x[self.day],time=x[self.hour]),axis=1)

            return X

class DropUnnecessaryFeatures(BaseEstimator, TransformerMixin):
    def __init__(self, variables_to_drop=None):
        self.variables = variables_to_drop

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        X = X.drop(self.variables, axis=1)

        return X
