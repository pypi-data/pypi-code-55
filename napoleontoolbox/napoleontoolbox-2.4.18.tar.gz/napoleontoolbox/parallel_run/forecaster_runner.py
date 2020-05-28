#!/usr/bin/env python
# coding: utf-8

from abc import ABC, abstractmethod

from napoleontoolbox.file_saver import dropbox_file_saver

from napoleontoolbox.forecasting import forecasting_model
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

from napoleontoolbox.signal import signal_utility
from napoleontoolbox.rebalancing import time_series_forecasting
from napoleontoolbox.utility import metrics
import datetime

import json

import pandas as pd
import numpy as np


class AbstractRunner(ABC):
    def __init__(self, starting_date = None, running_date = None, drop_token=None, dropbox_backup = True, underlying=None, frequence = None, algo=None, aggregated_pkl_file_suffix='freqly_to_mix.pkl', aggregated_pkl_mapping_file_suffix = 'freqly_to_mix_mapping.pkl', list_pkl_file_suffix = 'my_list.pkl', local_root_directory='../data/', user = 'napoleon'):
        super().__init__()
        self.aggregated_pkl_file_suffix=aggregated_pkl_file_suffix
        self.aggregated_pkl_mapping_file_suffix=aggregated_pkl_mapping_file_suffix
        self.underlying = underlying
        self.list_pkl_file_suffix = list_pkl_file_suffix
        self.frequence=frequence
        self.algo=algo

        self.list_pkl_file_name = self.underlying + '_' + self.frequence + '_' + self.algo + self.list_pkl_file_suffix
        self.aggregated_pkl_file_name = self.underlying + '_' + self.frequence + '_' + self.algo + self.aggregated_pkl_file_suffix
        self.aggregated_pkl_mapping_file_name = self.underlying + '_' + self.frequence + '_' + self.algo + self.aggregated_pkl_mapping_file_suffix
        self.local_root_directory=local_root_directory
        self.user=user
        self.dropbox_backup = dropbox_backup
        self.dbx = dropbox_file_saver.NaPoleonDropboxConnector(drop_token=drop_token,dropbox_backup=dropbox_backup)
        self.running_date = running_date
        self.starting_date = starting_date
        self.starting_iterations_to_pass = 20



    @abstractmethod
    def runTrial(self,saver,  seed,  n, s, s_eval, n_fft, n_wavelet, add_wavelet_detail, calibration_step,  optimize_threshold, signal_type, idios_string):
        pass

class ForecasterRunner(AbstractRunner):
    def runTrial(self, saver, seed, n, s, s_eval, calibration_step, optimize_threshold, signal_type, idios_string):
        if n == 0:
            n = None
        if s_eval == 0:
            s_eval = None
        idios = json.loads(idios_string)
        common_params ={
            'n':n,
            's':s,
            's_eval':s_eval,
            'calibration_step':calibration_step,
            'optimize_threshold':optimize_threshold,
            'signal_type' : signal_type
        }
        common_params.update(idios)
        saving_key = json.dumps(common_params, sort_keys=True)
        saving_key = signal_utility.convert_to_sql_column_format(saving_key)
        check_run_existence = saver.checkRunExistence(saving_key)
        if check_run_existence:
            return

        raw_data = pd.read_pickle(self.local_root_directory + self.aggregated_pkl_file_name)
        mapping_data = pd.read_pickle(self.local_root_directory + self.aggregated_pkl_mapping_file_name)

        print('size before filtering')
        print(raw_data.shape)

        raw_data=raw_data[raw_data.index >= (self.starting_date+datetime.timedelta(days=self.starting_iterations_to_pass))]
        raw_data=raw_data[raw_data.index <= self.running_date]
        print('size after filtering')
        print(raw_data.shape)

#        X, y = raw_data.loc[:, raw_data.columns != 'target'], raw_data['target']
        y = raw_data['close'].pct_change()
        X = raw_data[[col for col in raw_data.columns if 'signal' in col]]

        print('predictors shape')
        print(X.shape)
        print('output shape')
        print(y.shape)
        chosen_method = signal_type
        model = forecasting_model.ForecasterWrapper(method=chosen_method)

        # Compute rolling weights
        forecasted_series, features_importances = time_series_forecasting.rolling_forecasting(
            model,
            X,
            y,
            n=n,
            s=s,
            s_eval = s_eval,
            calibration_step = calibration_step,
            optimize_threshold = optimize_threshold,
            method = chosen_method,
            display = True)

        print('forecasting done')
        features_importances = features_importances.sum(axis = 0)
        print('features importance')
        print(features_importances.sum())

        forecasted_series[np.isnan(forecasted_series)] = 0
        forecasted_series[np.isinf(forecasted_series)] = 0
        matrix = confusion_matrix(y > 0, forecasted_series > 0)
        rmse = mean_squared_error(y, forecasted_series)
        accuracy = accuracy_score(y > 0, forecasted_series > 0)


        print('rmse '  + str(rmse))
        print('accuracy')
        print(accuracy)
        print('confusion matrix')
        print(matrix)

        # print(forecasted_series.shape)
        # if not filter_best_predictors:
        #     features_importances.to_pickle(local_root_directory + 'importances.pkl')
        #
        # perf_df = signal_utility.reconstitute_prediction_perf(y_pred=forecasted_series>0,y_true = y, transaction_cost=False,
        #                                                     print_turnover=False)
        #
        # perf_df = perf_df[perf_df.index >= '2002-02-01']
        # perf_df.to_pickle(local_root_directory +'perf_df.pkl')
        # #perf_df = pd.read_pickle(local_root_directory +'perf_df.pkl')
        # perf_df[['reconstituted_perf','reconstituted_close']].plot()


        perf_df = signal_utility.reconstitute_prediction_perf(y_pred=forecasted_series>0, y_true = y, transaction_cost=False, print_turnover=False)
        sharpe_strat = metrics.sharpe(perf_df['perf_return'].dropna(), period= 252, from_ret=True)
        sharpe_under = metrics.sharpe(perf_df['close_return'].dropna(), period= 252, from_ret=True)
        print('underlying sharpe')
        print(sharpe_under)
        print('strat sharpe')
        print(sharpe_strat)
        saver.saveAll(saving_key, perf_df)


