import pandas as pd
import numpy as np

stocks = ['AAPL', 'MSFT', 'SBUX']

from bs4 import BeautifulSoup as bs
import requests


def get_fundemental_data(df):
    for symbol in df.index:
        try:
            url = ('http://finviz.com/quote.ashx?t=' + symbol.lower())
            soup = bs(requests.get(url).content, features="lxml")
            for m in df.columns:
                df.loc[symbol, m] = fundemental_metric(soup, m)
        except Exception as e:
            print(symbol, 'not found')
    return df


def fundemental_metric(soup, metric):
    return soup.find(text=metric).find_next(class_='snapshot-td2').text


metric = ['P/B',
          'P/E',
          'Market Cap',
          'Current Ratio',
          'Forward P/E',
          'PEG',
          'Debt/Eq',
          'EPS (ttm)',
          'Dividend %',
          'ROE',
          'ROI',
          'EPS Q/Q',
          'Insider Own'
          ]

df = pd.DataFrame(index=stocks, columns=metric)
df = get_fundemental_data(df)

# CLEAN UP THE DATA

# Replace '-' and '' values with NaN
df = df.replace('-', np.NaN)
df = df.replace('', np.NaN)

# Some metrics have 'B' or 'M' at the end to indicate billions or millions of $
# Convert all those values to floats measured in billions of $
#df.loc[df['Market Cap'].str.strip().str[-1] == 'M', 'Market Cap'] = df['Market Cap'].str.strip().str[:-1].astype(float)\
             #                                                      / 1000
#df.loc[df['Market Cap'].str.strip().str[-1] == 'B', 'Market Cap'] = df['Market Cap'].str.strip().str[:-1].astype(float)

# Remove "%" signs
'''df['ROI'] = (df['ROI'].str[:-1])
df['ROE'] = (df['ROE'].str[:-1])
df['Dividend %'] = (df['Dividend %'].str[:-1])
df['EPS Q/Q'] = (df['EPS Q/Q'].str[:-1])
df['Insider Own'] = (df['Insider Own'].str[:-1])
df['Inst Own'] = (df['Inst Own'].str[:-1])'''

# Convert all values to floats
df = df.astype(float)

print (df)