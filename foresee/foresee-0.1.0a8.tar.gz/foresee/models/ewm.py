"""
exponentially weighted moving average
"""

import numpy as np
import pandas as pd

# local module
from foresee.models import models_util
from foresee.models import param_optimizer


def ewm_fit_forecast(ts, fcst_len, span):
    
    try:
        
        ewm_model = pd.Series(ts).ewm(span=span)
        ewm_fittedvalues = ewm_model.mean()
        
        ewm_forecast = np.empty(fcst_len)
        ewm_forecast.fill(ewm_fittedvalues.iloc[-1])
        ewm_forecast = pd.Series(ewm_forecast)
        err = None

    except Exception as e:
        
        ewm_fittedvalues = None
        ewm_forecast = None
        err = str(e)
        
    return ewm_fittedvalues, ewm_forecast, err


def fit_ewm(data_dict, freq, fcst_len, model_params, run_type, tune, epsilon):
    
    model = 'ewm_model'
    
    complete_fact = data_dict['complete_fact']
    
    # dataframe to hold fitted values
    fitted_fact = pd.DataFrame()
    fitted_fact['y'] = complete_fact['y']
    fitted_fact['data_split'] = complete_fact['data_split']
    
    # dataframe to hold forecast values
    forecast_fact = pd.DataFrame()
    forecast_fact['y'] = np.full(fcst_len, 0)
    forecast_fact['data_split'] = np.full(fcst_len, 'Forecast')
    
    fit_fcst_fact = pd.concat([fitted_fact, forecast_fact], ignore_index=True)
    
    args = dict()
    
    # no model competition
    if run_type in ['all_models']:
        
        span = 5
        ewm_fitted_values, ewm_forecast, err = ewm_fit_forecast(
                                                                    ts = complete_fact['y'],
                                                                    fcst_len = fcst_len,
                                                                    span = span,
                                                                )
        
        if err is None:
            fit_fcst_fact['ewm_model_forecast'] = ewm_fitted_values.append(ewm_forecast).values
            
        else:
            fit_fcst_fact['ewm_model_forecast'] = 0
            
        args['err'] = err
        args['span'] = span
            
            
    # with model completition            
    if run_type in ['best_model', 'all_best']:
        
        train_fact = data_dict['train_fact']
        test_fact = data_dict['test_fact']
        
        if tune:
            # TODO: add logic when optimization fails
            model_param_space = model_params[model]['span']
            span, trials = param_optimizer.tune(train_fact, test_fact, fcst_len, model, model_param_space, freq, epsilon)
            args['trials'] = trials
            
        else:
            span = 5
            
        training_fitted_values, training_forecast, training_err = ewm_fit_forecast(
                                                                                    ts = train_fact['y'],
                                                                                    fcst_len = len(test_fact) ,
                                                                                    span = span
                                                                                )
        
        complete_fitted_values, complete_forecast, complete_err = ewm_fit_forecast(
                                                                                    ts = complete_fact['y'],
                                                                                    fcst_len = fcst_len,
                                                                                    span = span
                                                                                )
        
        if training_err is None and complete_err is None:
            ewm_wfa = models_util.compute_wfa(
                                    y = test_fact['y'].values,
                                    yhat = training_forecast.values,
                                    epsilon = epsilon,
                                )
            ewm_fit_fcst = training_fitted_values.append(training_forecast, ignore_index=True).append(complete_forecast, ignore_index=True)
            
            fit_fcst_fact['ewm_model_forecast'] = ewm_fit_fcst.values
            fit_fcst_fact['ewm_model_wfa'] = ewm_wfa
            
        else:
            ewm_wfa = -1
            fit_fcst_fact['ewm_model_forecast'] = 0
            fit_fcst_fact['ewm_model_wfa'] = ewm_wfa
            
        args['err'] = (training_err, complete_err)
        args['wfa'] = ewm_wfa
        args['span'] = span
            
            
    return fit_fcst_fact, args
