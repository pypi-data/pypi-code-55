import talib as ta
import datetime
from pandas_datareader import DataReader

# Defining a class
class rsi:
    
    def __init__(self, stock):
        self.stock = stock

    def calculate_rsi(self):
        start_date = datetime.datetime.now() - datetime.timedelta(days=365)
        end_date = datetime.date.today()

        df = DataReader(self.stock, 'yahoo', start=start_date, end=end_date)

        df["rsi"] = ta.RSI(df["Close"])

        self.rsi_value = round(df["rsi"].tail(14).mean(), 2)
        
        print (self.rsi_value)
