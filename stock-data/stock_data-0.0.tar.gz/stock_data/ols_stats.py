import datetime
import numpy as np
import pandas as pd
from pandas_datareader.data import DataReader
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats

# Defining a class
class ols_stats:
    
    def __init__(self, stock, index):
        self.stock = stock
        self.index = index

    def get_ols_stats(self):
        start_date = datetime.datetime.now() - datetime.timedelta(days=1826)
        end_date = datetime.date.today()

        # Grab time series data for 5-year history for the stock 
        # and for S&P-500 Index
        df = DataReader(self.stock,'yahoo', start_date, end_date)['Close']
        dfb = DataReader(self.index,'yahoo', start_date, end_date)['Close']

        # joining the closing prices of the two datasets 
        monthly_prices = pd.concat([df, dfb], axis=1)
        monthly_prices.columns = [self.stock, self.index]
        
        
        # calculate monthly returns
        monthly_returns = monthly_prices.pct_change(1)
        clean_monthly_returns = monthly_returns.dropna(axis=0)  # drop first missing row
        
        # split dependent and independent variable
        X = clean_monthly_returns[self.index]
        y = clean_monthly_returns[self.stock]
        
        # Add a constant to the independent value
        X1 = sm.add_constant(X)
        
        # make regression model 
        model = sm.OLS(y, X1)
        
        # fit model and print results
        results = model.fit()
        print(results.summary())
        
