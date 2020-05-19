"""
sarimax from statsmodels
"""


import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import statsmodels.api

# local module
from foresee.models import models_util
from foresee.models import param_optimizer


def sarimax_fit_forecast(ts, fcst_len, freq, params):
    
    try:
        if params is None:
            sarimax_model = statsmodels.api.tsa.statespace.SARIMAX(
                                                                        endog = ts,
                                                                        enforce_stationarity = False,
                                                                        enforce_invertibility = False,
                                                                   ).fit(disp=0)
        else:
            order = (params['p'], params['d'], params['q'])
            seasonal_order = (params['cp'], params['cd'], params['cq'], freq)
            
            sarimax_model = statsmodels.api.tsa.statespace.SARIMAX(
                                                                        endog = ts,
                                                                        order = order,
                                                                        seasonal_order = seasonal_order,
                                                                        enforce_stationarity = True,
                                                                        enforce_invertibility = True,
                                                                   ).fit(disp=0)
            
        
        sarimax_fittedvalues = sarimax_model.fittedvalues
        sarimax_forecast = sarimax_model.predict(
                                                    start = len(ts),
                                                    end = len(ts) + fcst_len - 1,
                                                 )
        err = None
        
    except Exception as e:
        
        sarimax_model = None
        sarimax_fittedvalues = None
        sarimax_forecast = None
        err = str(e)
        
    return sarimax_fittedvalues, sarimax_forecast, err


def fit_sarimax(data_dict, freq, fcst_len, model_params, run_type, tune, epsilon):
    
    model = 'sarimax'
    
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
        
        sarimax_fitted_values, sarimax_forecast, err = sarimax_fit_forecast(
                                                                            ts = complete_fact['y'],
                                                                            fcst_len = fcst_len,
                                                                            freq = freq,
                                                                            params = None,
                                                                        )
        
        if err is None:
            fit_fcst_fact['sarimax_forecast'] = sarimax_fitted_values.append(sarimax_forecast).values
            
        else:
            fit_fcst_fact['sarimax_forecast'] = 0
            
        args['err'] = err
    
    # with model completition            
    if run_type in ['best_model', 'all_best']:
        
        train_fact = data_dict['train_fact']
        test_fact = data_dict['test_fact']
        
        if tune:
            # TODO: add logic when optimization fails
            model_param_space = model_params[model]
            params, trials = param_optimizer.tune(train_fact, test_fact, fcst_len, model, model_param_space, freq, epsilon)
            args['trials'] = trials
            
        else:
            params = None
            
        training_fitted_values, training_forecast, training_err = sarimax_fit_forecast(
                                                                                    ts = train_fact['y'],
                                                                                    fcst_len = len(test_fact),
                                                                                    freq = freq,
                                                                                    params = params,
                                                                                )
        
        complete_fitted_values, complete_forecast, complete_err = sarimax_fit_forecast(
                                                                                    ts = complete_fact['y'],
                                                                                    fcst_len = fcst_len,
                                                                                    freq = freq,
                                                                                    params = params,
                                                                                )
        
#        if 'enforce_stationarity' in complete_err or '' in complete_err:
#            
#            # run without enforcement
#        
#        #TODO: if failed with 'enforce_stationarity' or 'enforce_invertibility' at complete fcst, set these to false
        
        if training_err is None and complete_err is None:
            sarimax_wfa = models_util.compute_wfa(
                                    y = test_fact['y'].values,
                                    yhat = training_forecast.values,
                                    epsilon = epsilon,
                                )
            sarimax_fit_fcst = training_fitted_values.append(training_forecast, ignore_index=True).append(complete_forecast, ignore_index=True)
            
            fit_fcst_fact['sarimax_forecast'] = sarimax_fit_fcst.values
            fit_fcst_fact['sarimax_wfa'] = sarimax_wfa
            
        else:
            sarimax_wfa = -1
            fit_fcst_fact['sarimax_forecast'] = 0
            fit_fcst_fact['sarimax_wfa'] = -1
            
        args['err'] = (training_err, complete_err)
        args['wfa'] = sarimax_wfa
        args['params'] = params
            
            
    return fit_fcst_fact, args
