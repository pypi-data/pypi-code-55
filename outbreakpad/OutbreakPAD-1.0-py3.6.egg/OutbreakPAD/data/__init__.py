import pandas as pd
import os

_ROOT = os.path.abspath(os.path.dirname(__file__))
data=pd.read_csv(os.path.join(_ROOT, 'example.csv'))
