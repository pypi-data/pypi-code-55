import pandas as pd
import numpy as np
import datetime

from matplotlib import pyplot as plt
from functools import reduce
from sklearn import preprocessing
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.base  import BaseEstimator,TransformerMixin
### Calculate ratio of fraudulent transaction by each categorical variable

class MultiColumnLabelEncoder(BaseEstimator, TransformerMixin):
    def __init__(self,columns = None):
        self.columns = columns # array of column names to encode

    def fit(self,X,y=None):
        return self # not relevant here

    def transform(self,X):
        '''
        Transforms columns of X specified in self.columns using
        LabelEncoder(). If no columns specified, transforms all
        columns in X.
        '''
        output = X.copy()
        if self.columns is not None:
            for col in self.columns:
                output[col] = preprocessing.LabelEncoder().fit_transform(output[col])
        else:
            for colname,col in output.iteritems():
                output[colname] = preprocessing.LabelEncoder().fit_transform(col)
        return output

    def fit_transform(self,X,y=None):
        return self.fit(X,y).transform(X)
class CalculateRatioFraud(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key=key
    def fit(self, X, y=None):
        return self
    def transform(self,X):
        tmp = X.groupby([self.key, 'class']).user_id.nunique()\
        .unstack(level = 1)\
        .reset_index()\
        .rename(columns = {0:'Not Fraud', 1: 'Fraud'}).fillna(0.0)
        tmp['ratio_fraud_' + self.key] = tmp['Fraud']/(tmp['Fraud'] + tmp['Not Fraud'])
        tmp['num_trans_' + self.key] = tmp['Fraud'] + tmp['Not Fraud']
        return X[['user_id', self.key]]\
                .merge(tmp[[self.key, 'ratio_fraud_' + self.key, 'num_trans_' + self.key]], on = self.key)

class CalculateTimeLatency(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    def fit(self,X,y=None):
        return self
    def transform(self,X):
        X['time_latency']=(X.purchase_time-X.signup_time).dt.total_seconds()/60/60
        return X

class MergeMultipleDataframes(BaseEstimator, TransformerMixin):
    def __init__(self,dfs,key,method):
        self.dfs=dfs
        self.key=key
        self.method=method
    def fit(self,X,y=None):
        return self
    def transform(self,X):
        Xunion=reduce(lambda  left, right: pd.merge(left, right, on = self.key, how=self.method), self.dfs)
        return Xunion
        
class ApplyLabelEncoding(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    def fit(self,X,y=None):
        return self
    def transform(self,X):
        return MultiColumnLabelEncoder(columns = X.columns).fit_transform(X)

    
class CreateFeatures(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    def fit(self,X,y=None):
        return self
    def transform(self,X):
        X.signup_time=pd.to_datetime(X.signup_time, format = '%m/%d/%Y %H:%M')
        X.purchase_time=pd.to_datetime(X.purchase_time, format = '%m/%d/%Y %H:%M')
        X = X.fillna('NA')
        fraud_by_dev = CalculateRatioFraud(key='device_id').transform(X)
        fraud_by_country = CalculateRatioFraud(key='country').transform(X)
        fraud_by_age = CalculateRatioFraud(key='age').transform(X)
        fraud_by_gender = CalculateRatioFraud(key='sex').transform(X)
        fraud_by_source = CalculateRatioFraud(key='source').transform(X)
        fraud_by_browser = CalculateRatioFraud(key='browser').transform(X)
        latency_df = CalculateTimeLatency().transform(X)
        feature_df = MergeMultipleDataframes(dfs=[
                                        fraud_by_dev, fraud_by_country, 
                                        fraud_by_gender, 
                                        fraud_by_age, 
                                        fraud_by_browser, 
                                        fraud_by_source, 
                                        X[['user_id', 'purchase_value', 'class']],
                                        latency_df[['user_id', 'time_latency']]
                                       ], 
                                       key = ['user_id'], method = 'outer').transform(X)
        df_cat = ApplyLabelEncoding().transform(feature_df[['country', 'sex', 'browser', 'source']])
        return pd.concat([feature_df.drop(['country', 'sex', 'browser', 'source'], axis = 1), df_cat], axis = 1).set_index(['user_id', 'device_id'])
