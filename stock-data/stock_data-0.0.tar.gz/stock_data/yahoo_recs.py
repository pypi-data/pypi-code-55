import requests
import pandas as pd 
from pandas_datareader import DataReader
import numpy as np

# Defining a class
class yahoo_recs:
    
    def __init__(self, stock):
        self.stock = stock

    def get_yahoo_recs(self):
        # Parameters 
        if type(self.stock) == str:
            tickers = ['{}'.format(self.stock)]
        else: 
            tickers = self.stock
            
        for ticker in tickers:
            lhs_url = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/'
            rhs_url = '?formatted=true&crumb=swg7qs5y9UP&lang=en-US&region=US&' \
                      'modules=upgradeDowngradeHistory,recommendationTrend,' \
                      'financialData,earningsHistory,earningsTrend,industryTrend&' \
                      'corsDomain=finance.yahoo.com'
                      
            url =  lhs_url + ticker + rhs_url
            r = requests.get(url)
            if not r.ok:
                recommendation = 0
            try:
                result = r.json()['quoteSummary']['result'][0]
                recommendation =result['financialData']['recommendationMean']['fmt']
            except:
                recommendation = 0
                
            print (recommendation)
