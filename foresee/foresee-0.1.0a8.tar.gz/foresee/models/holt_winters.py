"""
Holt-Winters
"""

import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# local module
from foresee.models import models_util
from foresee.models import param_optimizer

def holt_winters_fit_forecast(ts, fcst_len, freq, params):
    
    try:
        hw_model = ExponentialSmoothing(
                                            endog = ts,
                                            trend = 'add',
                                            damped = True,
                                            seasonal = 'add',
                                            seasonal_periods = freq
                                          )
        
        if params is None:
            hw_model = hw_model.fit(optimized = True)
            
        else:
            s_level, s_slope, s_season, d_slope = (params['s_level'], params['s_slope'], params['s_season'], params['d_slope'])
            hw_model = hw_model.fit(
                                                      smoothing_level = s_level,
                                                      smoothing_slope = s_slope,
                                                      smoothing_seasonal = s_season,
                                                      damping_slope = d_slope,
                                                      optimized = True,
                                    )
            
        hw_fittedvalues = hw_model.fittedvalues    

        hw_forecast = hw_model.predict(
                                            start = len(ts),
                                            end =   len(ts) + fcst_len - 1
                                        )
        err = None
        
    except Exception as e:
        hw_fittedvalues = None
        hw_forecast = None
        err = str(e)
    
    
    return hw_fittedvalues, hw_forecast, err


def fit_holt_winters(data_dict, freq, fcst_len, model_params, run_type, tune, epsilon):
    
    model = 'holt_winters'
    
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
        
        hw_fitted_values, hw_forecast, err = holt_winters_fit_forecast(
                                                                           ts = complete_fact['y'],
                                                                           fcst_len = fcst_len,
                                                                           freq = freq,
                                                                           params = None
                                                                      )
        if err is None:
            fit_fcst_fact['holt_winters_forecast'] = hw_fitted_values.append(hw_forecast).values
            
        else:
            fit_fcst_fact['holt_winters_forecast'] = 0
            
        args['err'] = err
    
    
    # with model completition            
    if run_type in ['best_model', 'all_best']:
        
        train_fact = data_dict['train_fact']
        test_fact = data_dict['test_fact']
        
        if tune:
            # TODO: add logic when optimization fails
            
            model_param_space = model_params[model]
            opt_params, trials = param_optimizer.tune(train_fact, test_fact, fcst_len, model, model_param_space, freq, epsilon)
            
            args['trials'] = trials
            
        else:
            opt_params = None
            
        training_fitted_values, training_forecast, training_err = holt_winters_fit_forecast(
                                                                                                   ts = train_fact['y'],
                                                                                                   fcst_len = len(test_fact),
                                                                                                   freq = freq,
                                                                                                   params = opt_params,
                                                                                         )
        
        complete_fitted_values, complete_forecast, complete_err = holt_winters_fit_forecast(
                                                                                                   ts = complete_fact['y'],
                                                                                                   fcst_len = fcst_len,
                                                                                                   freq = freq,
                                                                                                   params = opt_params,
                                                                                         )
        
        if training_err is None and complete_err is None:
            hw_wfa = models_util.compute_wfa(
                                    y = test_fact['y'].values,
                                    yhat = training_forecast.values,
                                    epsilon = epsilon,
                                )
            hw_fit_fcst = training_fitted_values.append(training_forecast, ignore_index=True).append(complete_forecast, ignore_index=True)
            
            fit_fcst_fact['holt_winters_forecast'] = hw_fit_fcst.values
            fit_fcst_fact['holt_winters_wfa'] = hw_wfa
            
        else:
            hw_wfa = -1
            fit_fcst_fact['holt_winters_forecast'] = 0
            fit_fcst_fact['holt_winters_wfa'] = -1
            
        args['err'] = (training_err, complete_err)
        args['wfa'] = hw_wfa
        args['params'] = opt_params
        
        
    return fit_fcst_fact, args




