import numpy as np
import pandas as pd
import datetime
from pandas_datareader import DataReader

# Defining a class
class rolling_sortino:
    
    def __init__(self, stock, target_return, start_date, end_date):
        self.stock = stock
        self.target_return = target_return        

    def calculate_sortino(self):
        start_date = datetime.datetime.now() - datetime.timedelta(days=365)
        end_date = datetime.date.today()

        df = DataReader(self.stock, 'yahoo', start_date, end_date)['Close']
        
        rfr = 0
        target = self.target_return
        
        df['Returns'] = df.pct_change()
        
        returns = df['Returns']
        sharpe_ratio = ((returns.mean() - rfr) / returns.std())
        
        df['downside_returns'] = 0
        df.loc[df['Returns'] < target, 'downside_returns'] = df['Returns']**2
        expected_return = df['Returns'].mean()
        down_stdev = np.sqrt(df['downside_returns'].mean())
        sortino_ratio = (expected_return - rfr)/down_stdev
        print(sortino_ratio)