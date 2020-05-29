# -*- coding: utf-8 -*-
#import pandas as pd
import os
from ..Prediction import read_data
_ROOT = os.path.abspath(os.path.dirname(__file__))
example=read_data(os.path.join(_ROOT, 'example.csv'),)
