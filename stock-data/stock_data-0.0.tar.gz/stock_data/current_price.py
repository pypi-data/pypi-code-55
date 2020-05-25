import requests 
from yahoo_fin import stock_info as si
import pandas as pd

# Defining a class
class current_price:
    
    def __init__(self, stock):
        self.stock = stock

    def get_current_price(self):
        
        # Parameters 
        if type(self.stock) == str:
            tickers = ['{}'.format(self.stock)]
        else: 
            tickers = self.stock

        prices = []
        for ticker in tickers: 
            price = si.get_live_price(ticker)
            prices.append(price)

        df = pd.DataFrame(list(zip(tickers, prices)), columns =['Ticker', 'Current Price']) 
        df = df.set_index('Ticker')
        print (df)