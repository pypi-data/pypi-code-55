# -*- coding: utf-8 -*-
"""
fitter class
"""

import os
import sys

# import local modules

#module_path = os.path.abspath(os.path.join('..'))
#if module_path not in sys.path:
#    sys.path.append(module_path+'\\models')
    
from foresee.models.holt_winters import fit_holt_winters
from foresee.models.sarimax import fit_sarimax
from foresee.models.ewm import fit_ewm
from foresee.models.prophet import fit_prophet
from foresee.models.fft import fit_fft

class fitter:
    
    FIT_MODELS = {
                    'holt_winters':     fit_holt_winters,
                    'sarimax':          fit_sarimax,
                    'ewm_model':        fit_ewm,
                    'prophet':          fit_prophet,
                    'fft':              fit_fft,
                 }
    
    
    def __init__(self, model):
         self.model = model
         
    
    def fit(self, data_dict, freq, forecast_len, model_params, run_type, tune, epsilon):
        """

        :param data_param_dict: ts values and parameters
        """
        fit_model = self.FIT_MODELS[self.model]
        
        return fit_model(data_dict, freq, forecast_len, model_params, run_type, tune, epsilon)