import pickle
import datetime
import requests
import bs4 as bs
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from yahoo_fin import stock_info as si
from pandas_datareader import DataReader
import seaborn as sns

# Defining a class
class rolling_sharpe:
    
    def __init__(self, stock):
        self.stock = stock

    def calculate_rolling_sharpe(self):
        start_date = datetime.datetime.now() - datetime.timedelta(days=365)
        end_date = datetime.date.today()
        df = DataReader(self.stock, 'yahoo', start_date, end_date) 
        x = 5000
        
        y = (x)
        
        stock_df = df
        stock_df['Norm return'] = stock_df['Adj Close'] / stock_df.iloc[0]['Adj Close']
        
        allocation = float(x/y)
        stock_df['Allocation'] = stock_df['Norm return'] * allocation
        
        stock_df['Position'] = stock_df['Allocation'] * x
        pos = [df['Position']]
        val = pd.concat(pos, axis=1)
        val.columns = ['WMT Pos']
        val['Total Pos'] = val.sum(axis=1)
        
        val.tail(1)
        
        val['Daily Return'] = val['Total Pos'].pct_change(1)
        
        Sharpe_Ratio = val['Daily Return'].mean() / val['Daily Return'].std()
        
        A_Sharpe_Ratio = round((252**0.5) * Sharpe_Ratio, 2)
        
        print (A_Sharpe_Ratio)
