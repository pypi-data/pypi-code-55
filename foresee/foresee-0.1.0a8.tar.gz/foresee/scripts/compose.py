# -*- coding: utf-8 -*-
"""
manage input and output of forecasting models
"""

import pandas as pd
import numpy as np
import datetime
import dask
dask.config.set(scheduler='processes')

from foresee.scripts import fitter

def generate_fit_forecast(dict_key, dict_values, model_list, freq, forecast_len, model_params, run_type, tune, epsilon):
    
    fit_result = dict()
    fit_result['ts_id'] = dict_key
    
    for m in model_list:

        f = fitter.fitter(m)

        (
         fit_result[m+'_fit_fcst_df'],
         fit_result[m+'_args']
         ) = f.fit(dict_values, freq, forecast_len, model_params, run_type, tune, epsilon)
    
    return fit_result


# non-parallel fit function
def compose_fit(pre_processed_dict, model_params, param_config, gbkey, run_type, processing_method, tune):
    
    freq = param_config['FREQ']
    forecast_len = param_config['FORECAST_LEN']
    model_list = param_config['MODEL_LIST']
    epsilon = param_config['EPSILON']
    
    # non-parallel fit
    
    if processing_method == 'parallel':
        task_list = list()
        
        for dict_key, dict_values in pre_processed_dict.items():
            fit_task = dask.delayed(generate_fit_forecast)(
                                                               dict_key,
                                                               dict_values,
                                                               model_list,
                                                               freq,
                                                               forecast_len,
                                                               model_params,
                                                               run_type,
                                                               tune,
                                                               epsilon
                                                          )
            task_list.append(fit_task)

        fit_result_list = dask.compute(task_list)[0]
        
    else:
        fit_result_list = list()

        for dict_key, dict_values  in pre_processed_dict.items():
            fit_result = generate_fit_forecast(
                                                    dict_key,
                                                    dict_values,
                                                    model_list,
                                                    freq,
                                                    forecast_len,
                                                    model_params,
                                                    run_type,
                                                    tune,
                                                    epsilon
                                            )
            fit_result_list.append(fit_result)
        
    result = combine_to_dataframe(fit_result_list, model_list, run_type)
        
    return result, fit_result_list


def combine_to_dataframe(fit_result_list, model_list, run_type):
    
    if run_type == 'best_model':

        fit_result_list = _find_best_model(fit_result_list, model_list)
        
        df_list = list()

        for result_dict in fit_result_list:

            bm = result_dict['best_model']
            df = result_dict[bm+'_fit_fcst_df']
            
            df['best_model'] = bm
            df['ts_id'] = result_dict['ts_id']
            df_list.append(df)

        result = pd.concat(df_list, axis=0, ignore_index=True)
        
    elif run_type == 'all_best':
        
        fit_result_list = _find_best_model(fit_result_list, model_list)
        
        df_list = list()

        for result_dict in fit_result_list:
            bm = result_dict['best_model']
            df = result_dict[bm+'_fit_fcst_df']
            
            for m in model_list:
                mdf = result_dict[m+'_fit_fcst_df']
                df[m+'_forecast'] = mdf[m+'_forecast'].values
                df[m+'_wfa'] = mdf[m+'_wfa'].values

            df['ts_id'] = result_dict['ts_id']
            df['best_model'] = bm
            df_list.append(df)

        result = pd.concat(df_list, axis=0, ignore_index=True)
                
        
    else:
        df_list = list()
        
        for result_dict in fit_result_list:
            df = pd.DataFrame()
            
            for m in model_list:
                mdf = result_dict[m+'_fit_fcst_df']
                df[m+'_forecast'] = mdf[m+'_forecast'].values
                
            df['data_split'] = mdf['data_split'].values
            df['ts_id'] = result_dict['ts_id']
            df_list.append(df)
        
        result = pd.concat(df_list, axis=0, ignore_index=True) 
    
    return result


def _find_best_model(fit_result_list, model_list):
    
    for result_dict in fit_result_list:
        model_wfa_dict = dict()
        
        for m in model_list:
            model_wfa_dict[m] = result_dict[m+'_args']['wfa']
            
        result_dict['best_model'] = [k for k,v in model_wfa_dict.items() if v == max(model_wfa_dict.values())][0]
    
    return fit_result_list


# not in use
def _transform_dataframe_to_dict(raw_fact, gbkey):
    
    data_param_list = list()
    
    if gbkey is None:
        
        data_param_list.append({'ts_id':1, 'df':raw_fact})
    
    else:
        for k,v in raw_fact.groupby(gbkey):
            data_param_list.append({'ts_id':k, 'df':v})
    
    return data_param_list


