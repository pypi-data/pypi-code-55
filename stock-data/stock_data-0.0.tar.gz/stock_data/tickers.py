import requests
import pickle
import bs4 as bs 
from yahoo_fin import stock_info as si
from get_all_tickers import get_tickers as gt

# Defining a class
class tickers:
    
    def __init__(self, index):
        self.index = index

    def get_tickers(self):
        if self.index.lower() in ['s&p 500', 's&p500']:
            # save_sp500_tickers()
            def save_spx_tickers():
                resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
                soup = bs.BeautifulSoup(resp.text, 'lxml')
                table = soup.find('table', {'class':'wikitable sortable'})
                tickers = []
                for row in table.findAll('tr')[1:]:
                    ticker = row.find_all('td') [0].text.strip()
                    tickers.append(ticker)
                    
                with open('spxTickers.pickle', 'wb') as f:
                        pickle.dump(tickers, f)       
                return tickers
                    
            tickers = save_spx_tickers()
            tickers = [item.replace(".", "-") for item in tickers]
            print (tickers)
        
        elif self.index.lower() == 'nasdaq':
            tickers = si.tickers_nasdaq()
            print (tickers)
        
        elif self.index.lower() == 'dow':
            tickers = si.tickers_dow()
            print (tickers)
            
        elif self.index.lower() == 'nyse':
            tickers = gt.get_tickers(NYSE=True, NASDAQ=False, AMEX=False)
            print (tickers)
            
        elif self.index.lower() == 'amex':
            tickers = gt.get_tickers(NYSE=False, NASDAQ=False, AMEX=True)
            print (tickers)