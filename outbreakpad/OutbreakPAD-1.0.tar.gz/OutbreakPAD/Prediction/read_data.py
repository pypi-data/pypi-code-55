import pandas as pd
def read_data(file):
    ts=pd.read_csv(file,header=None)
    start_date==ts.iloc[0][0]
    ts_number=ts.iloc[:,1]
    ts_number=ts_number.values
    ts_time=pd.date_range(start_date,periods=len(ts_number),freq="D")
    ts=pd.Series(ts_number,index=ts_time)
    return ts
