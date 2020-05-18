import datetime as dt
import pandas as pd
from os import path
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay
import time

class urlsYahooFinance(dict):
    def __init__(self):
        self.url_base = 'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={start_date:.0f}&period2={end_date:.0f}&interval=1d'
        super().__init__(
            {'px':self.url_base+'&events=history',
            'div':self.url_base+'&events=div',                
            'splits':self.url_base+'&events=split'}
        )
        
class dtUtils():
    def Bday(self,days):
        return CustomBusinessDay(days,holidays=USFederalHolidayCalendar().holidays())
        
        
    def parseDateToUnix(self, date):
        return time.mktime(dt.datetime(
            date.year,date.month,date.day,12,0
        ).timetuple())
        
class yahooFinance():
    def __init__(self):        
        self.dtU = dtUtils()
        self.urls = urlsYahooFinance()
        
    def __saveHistFile(self,dfs,ticker,folder_to_save=''):
        self.__saveDfToCsv(
            dfs,ticker,folder_to_save,
            sufix='h_',mode='w',
            header=True
        )
        
    def __saveDailyFile(self,dfs,ticker,folder_to_save=''):
        self.__saveDfToCsv(
            dfs,ticker,folder_to_save,
            sufix='d_',mode='a',
            header=False
        )
        
    def __saveDfToCsv(self,dfs,ticker,folder_to_save='',sufix='',mode='w',header=True):        
        for df_name,df in dfs.items():            

            file_full_add = folder_to_save+'{sufix}{ticker}_{name}.csv'.format(
                ticker=ticker.lower(),
                name = df_name.lower(),
                sufix = sufix.lower(),
            )            

            if not path.exists(file_full_add):
                header = True

            df.to_csv(file_full_add,index=False,mode=mode,header=header)
                
    
    def __historicalDownload(self,ticker,start_date,end_date):
        dfs ={}
        for url_name,url_base in self.urls.items():        
            url = url_base.format(
                ticker = ticker,
                start_date = self.dtU.parseDateToUnix(start_date),
                end_date = self.dtU.parseDateToUnix(end_date)
            )
            df = pd.read_csv(url)
            df['Date'] = pd.to_datetime(df['Date'])            
            dfs[url_name] = df.sort_values('Date',ascending=False)
        return  dfs
    
    def getPrice(self, tickers, start_date, end_date):
        '''
        get historical prices from yahoo finance 
        '''
        return {ticker:self.__historicalDownload(ticker,start_date,end_date) for ticker in tickers}
    
    # def getLastPrice(self,ticker,dayref = None,folder_to_save='repository/equity/'):
        
    #     try:
    #         if dayref is None:            
    #             dayref = dt.datetime.now()
    #         else:            
    #             dayref = dayref

    #         if dayref.hour > 14:
    #             day = dt.datetime.today()
    #         else:
    #             day = dt.datetime.today() - self.dtU.Bday(1)

    #         last_price = self.__historicalDownload(ticker,day,day)    
    #         self.__saveDailyFile(last_price,ticker,folder_to_save)
    #         log.printLog('SUCESS',['daily yahoo price:',ticker,dayref])
    #     except Exception as e:
    #         log.printException(e)
        
    # def historical_price(self,ticker,start_date,end_date,folder_to_save='repository/equity/'):                        
    #     dfs = self.__historicalDownload(ticker,start_date,end_date)        
    #     self.__saveHistFile(dfs,ticker,folder_to_save)           
    #     #return  dfs
 