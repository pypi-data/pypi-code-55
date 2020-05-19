"""
fast fourier transform
"""

import numpy as np
import pandas as pd

# local module
from foresee.models import models_util
from foresee.models import param_optimizer


def reconstruct_signal(
                         n_periods,
                         forecast_len,
                         fft_model,
                         ft_sample_frequencies,
                         fft_terms_for_reconstruction,
                         linear_trend
                      ):
    """

    :param n_periods:
    :param fft_model:
    :param ft_sample_frequencies:
    :param fft_terms_for_reconstruction:
    :param linear_trend:
    :return:
    """
    
    pi = np.pi
    t = np.arange(0, n_periods+forecast_len)
    restored_sig = np.zeros(t.size)
    for i in fft_terms_for_reconstruction:
        ampli = np.absolute(fft_model[i]) / n_periods
        phase = np.angle(
                             fft_model[i],
                             deg = False
                           )
        restored_sig += ampli * np.cos(2 * pi * ft_sample_frequencies[i] * t + phase)
    return restored_sig + linear_trend[0] * t


def fft_fit_forecast(ts, fcst_len, n_harmonics):
    
    ts_len = len(ts)
    
    try:
        t = np.arange(0, ts_len)
        linear_trend = np.polyfit(t, ts, 1)
        training_endog_detrend = ts - linear_trend[0] * t
        fft_model = np.fft.fft(training_endog_detrend)
        indexes = list(range(ts_len))
        
        # sort by amplitude
        indexes.sort(
                        key = lambda i: np.absolute(fft_model[i]) / ts_len,
                        reverse = True
                    )
        fft_terms_for_reconstruction = indexes[:1 + n_harmonics * 2]
        ft_sample_frequencies = np.fft.fftfreq(
                                                    n = ts_len,
                                                    d = 1
                                                 )
        
        fft_fit_forecast = reconstruct_signal(
                                                 n_periods = ts_len,
                                                 forecast_len = fcst_len,
                                                 fft_model = fft_model,
                                                 ft_sample_frequencies = ft_sample_frequencies,
                                                 fft_terms_for_reconstruction = fft_terms_for_reconstruction,
                                                 linear_trend = linear_trend
                                              )
        
        fft_fit_forecast = pd.Series(fft_fit_forecast)
        
        
        fft_fittedvalues = fft_fit_forecast[:-(fcst_len)]
        
        fft_forecast = fft_fit_forecast[-(fcst_len):]
        
        err = None
        
        
    except Exception as e:
        fft_fittedvalues = None
        fft_forecast = None
        err = str(e)
        
    return fft_fittedvalues, fft_forecast, err


def fit_fft(data_dict, freq, fcst_len, model_params, run_type, tune, epsilon):
    
    model = 'fft'
    
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
        
        n_harmonics = 5
        fft_fitted_values, fft_forecast, err = fft_fit_forecast(
                                                                    ts = complete_fact['y'],
                                                                    fcst_len = fcst_len,
                                                                    n_harmonics = n_harmonics,
                                                            )
        
        if err is None:
            fit_fcst_fact['fft_forecast'] = fft_fitted_values.append(fft_forecast).values
            
        else:
            fit_fcst_fact['fft_forecast'] = 0
            
        args['err'] = err
        args['n_harmonics'] = n_harmonics
            
    # with model completition            
    if run_type in ['best_model', 'all_best']:
        
        train_fact = data_dict['train_fact']
        test_fact = data_dict['test_fact']
        
        if tune:
            # TODO: add logic when optimization fails
            model_param_space = model_params[model]['n_harmonics']
            n_harmonics, trials = param_optimizer.tune(train_fact, test_fact, fcst_len, model, model_param_space, freq, epsilon)
            args['trials'] = trials
            
        else:
            n_harmonics = 5
            
        training_fitted_values, training_forecast, training_err = fft_fit_forecast(
                                                                                    ts = train_fact['y'],
                                                                                    fcst_len = len(test_fact) ,
                                                                                    n_harmonics = n_harmonics
                                                                                )
        
        complete_fitted_values, complete_forecast, complete_err = fft_fit_forecast(
                                                                                    ts = complete_fact['y'],
                                                                                    fcst_len = fcst_len,
                                                                                    n_harmonics = n_harmonics
                                                                                )
        
        if training_err is None and complete_err is None:
            fft_wfa = models_util.compute_wfa(
                                    y = test_fact['y'].values,
                                    yhat = training_forecast.values,
                                    epsilon = epsilon,
                                )
            fft_fit_fcst = training_fitted_values.append(training_forecast, ignore_index=True).append(complete_forecast, ignore_index=True)
            
            fit_fcst_fact['fft_forecast'] = fft_fit_fcst.values
            fit_fcst_fact['fft_wfa'] = fft_wfa
            
        else:
            fft_wfa = -1
            fit_fcst_fact['fft_forecast'] = 0
            fit_fcst_fact['fft_wfa'] = -1
            
        args['err'] = (training_err, complete_err)
        args['wfa'] = fft_wfa
        args['n_harmonics'] = n_harmonics
        
        
    return fit_fcst_fact, args
