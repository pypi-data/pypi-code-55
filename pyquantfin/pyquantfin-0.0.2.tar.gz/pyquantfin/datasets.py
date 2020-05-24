import pandas as pd
#import numpy as np
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "data/")

def load_assets() -> 'df':
    return pd.read_csv(DATA_PATH + 'assets.csv',encoding='gbk').set_index('date')

#def load_hs300_5min() -> 'df':
#    return pd.read_hdf(DATA_PATH + 'hs300_5min.h5')

def load_intraday(name = 'hs300', bar_size = '5min') -> 'df':
    return pd.read_hdf(DATA_PATH + name + '_' + bar_size + '.h5')

def load_hs300() -> 'df':
    print('--- data from tushare ---')
    df= pd.read_csv(DATA_PATH + 'hs300.csv', dtype = {'trade_date':str})
    return df.set_index('trade_date')

def load_sp500() -> 'df':
    print('--- data from wind ---')
    df = pd.read_excel(DATA_PATH + 'sp500.xlsx')
    df = df.rename(columns = {'开盘价(元)':'open',
                              '最高价(元)':'high',
                              '收盘价(元)':'close',
                              '最低价(元)':'low',
                              '日期':'date'})
    df = df[['date','high','open','low','close']]
    return df