"""
utility script for optimization techniques
"""


import warnings
warnings.filterwarnings('ignore')

from hyperopt import hp, fmin, tpe, Trials

# local methods
from foresee.models import ewm
from foresee.models import holt_winters
from foresee.models import fft
from foresee.models import sarimax

from foresee.models import models_util

def _model_wfa(p, ts_train, ts_test, model, freq, epsilon):
    
    fcst_len = len(ts_test)
    
    if model == 'ewm_model':
        
        fittedvalues, yhat, err  = ewm.ewm_fit_forecast(ts_train, fcst_len, p)
        
        if err is None:
            wfa = models_util.compute_wfa(ts_test.values, yhat.values, epsilon)
            
        else:
            wfa = 0
        
    
    elif model == 'holt_winters':
        
        fittedvalues, yhat, err  = holt_winters.holt_winters_fit_forecast(ts_train, fcst_len, freq, p)
        
        if err is None:
            wfa = models_util.compute_wfa(ts_test.values, yhat.values, epsilon)
            
        else:
            wfa = 0
        
    elif model == 'fft':
        
        fittedvalues, yhat, err  = fft.fft_fit_forecast(ts_train, fcst_len, p)
        
        if err is None:
            wfa = models_util.compute_wfa(ts_test.values, yhat.values, epsilon)
            
        else:
            wfa = 0
            
    elif model == 'sarimax':
        
        fittedvalues, yhat, err  = sarimax.sarimax_fit_forecast(ts_train, fcst_len, freq, p)
        
        if err is None:
            wfa = models_util.compute_wfa(ts_test.values, yhat.values, epsilon)
            
        else:
            wfa = 0
            print(err)
            
    else:
        wfa = 0
        
    return 1 - wfa


def tune(train_fact, test_fact, fcst_len, model, model_param_space, freq, epsilon):
    
    ts_train = train_fact['y']
    ts_test = test_fact['y']
    
    best, trials = optimize_param(ts_train, ts_test, fcst_len, model, model_param_space, freq, epsilon)
    
    return best, trials


def optimize_param(ts_train, ts_test, fcst_len, model, model_param_space, freq, epsilon):
    
    # TODO: fill out function description
    
    if model == 'ewm_model':
        
        try:
            span_lb = 2
            span_ub = model_param_space
            
            space = hp.quniform('span', span_lb, span_ub, 1)
            
            f_obj = lambda p: _model_wfa(p, ts_train, ts_test, model, freq, epsilon)
            
            trials = Trials()
            
            best = fmin(f_obj, space, algo=tpe.suggest, trials=trials, max_evals=100, show_progressbar=False, verbose=False)
            
            best = best['span']
            
        except Exception as e:
            best = str(e)
            
    elif model == 'holt_winters':
        
        try:
            space = {
                        's_level': hp.uniform('s_level', 0, 1),
                        's_slope': hp.uniform('s_slope', 0, 1),
                        's_season': hp.uniform('s_season', 0, 1),
                        'd_slope': hp.uniform('d_slope', 0, 1)
                    }
            
            f_obj = lambda p: _model_wfa(p, ts_train, ts_test, model, freq, epsilon)
            
            trials = Trials()
            
            best = fmin(f_obj, space, algo=tpe.suggest, trials=trials, max_evals=200, show_progressbar=False, verbose=False)
            
        except Exception as e:
            best = str(e)
        
    elif model == 'fft':
        
        try:
            nh_lb = 2
            nh_ub = model_param_space
            
            space = hp.quniform('nh', nh_lb, nh_ub, 1)
            
            f_obj = lambda p: _model_wfa(int(p), ts_train, ts_test, model, freq, epsilon)
            
            trials = Trials()
            
            best = fmin(f_obj, space, algo=tpe.suggest, trials=trials, max_evals=100, show_progressbar=False, verbose=False)
            
            best = int(best['nh'])
            
        except Exception as e:
            best = str(e)
            
        
    elif model == 'sarimax':
        
        try:
            max_p = model_param_space['p']
            max_d = model_param_space['d']
            max_q = model_param_space['q']
            max_cp = model_param_space['cp']
            max_cd = model_param_space['cd']
            max_cq = model_param_space['cq']
            
            space = {
                        'p': hp.randint('p', max_p),
                        'd': hp.randint('d', max_d),
                        'q': hp.randint('q', max_q),
                        'cp': hp.randint('cp', max_cp),
                        'cd': hp.randint('cd', max_cd),
                        'cq': hp.randint('cq', max_cq)
                    }
            
            f_obj = lambda p: _model_wfa(p, ts_train, ts_test, model, freq, epsilon)
            
            trials = Trials()
            
            best = fmin(f_obj, space, algo=tpe.suggest, trials=trials, max_evals=200, show_progressbar=False, verbose=False)
            
        except Exception as e:
            best = str(e)
            print(best)
        
    else:
        raise ValueError(model)
        
    return best, trials
    

