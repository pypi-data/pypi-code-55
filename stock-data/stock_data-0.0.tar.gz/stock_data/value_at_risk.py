import pandas as pd
from pandas_datareader import DataReader
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import scipy 
from scipy.stats import norm

# Defining a class
class value_at_risk:
    
    def __init__(self, stock, weights, allocation, start_date, end_date):
        self.stock = stock
        self.weights = weights
        self.allocation = allocation
        self.start_date = start_date
        self.end_date = end_date
        

    def calculate_value_at_risk(self):
        
        # Parameters 
        if type(self.stock) == str:
            tickers = ['{}'.format(self.stock)]
            self.weights = [1.0]
        else: 
            tickers = self.stock
         
        # Set the investment weights (I arbitrarily picked for example)
        weights = np.array(self.weights)
         
        # Set an initial investment level
        initial_investment = 1000000
         
        # Download closing prices
        data = DataReader(tickers, 'yahoo', start=self.start_date, end=self.end_date)['Close']
         
        #From the closing prices, calculate periodic returns
        returns = data.pct_change()
        
        returns.tail()
        
        # Generate Var-Cov matrix
        cov_matrix = returns.cov()
        cov_matrix
        
        # Calculate mean returns for each stock
        avg_rets = returns.mean()
         
        # Calculate mean returns for portfolio overall, 
        port_mean = avg_rets.dot(weights)
         
        # Calculate portfolio standard deviation
        port_stdev = np.sqrt(weights.T.dot(cov_matrix).dot(weights))
         
        # Calculate mean of investment
        mean_investment = (1+port_mean) * initial_investment
                     
        # Calculate standard deviation of investmnet
        stdev_investment = initial_investment * port_stdev
        
        # Select our confidence interval (I'll choose 95% here)
        conf_level1 = 0.05
        
        # Using SciPy ppf method to generate values for the
        # inverse cumulative distribution function to a normal distribution
        # Plugging in the mean, standard deviation of our portfolio
        # as calculated above
        cutoff1 = norm.ppf(conf_level1, mean_investment, stdev_investment)
        
        #Finally, we can calculate the VaR at our confidence interval
        var_1d1 = initial_investment - cutoff1
        print (round(var_1d1, 2))