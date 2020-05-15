# live function
import numpy as np
import pandas as pd
import statsmodels.api as sm
from datetime import timedelta, datetime
from math import sqrt

### reference this for future improvements
#DEFAULT_INTERVAL = timedelta(minutes=10)
#DEFAULT_PERIODS = 6 * 48  # 10 mins * 6 * 48 = 2 days
#DEFAULT_MODEL_OPTIONS = {"type": "areg"}
# df in, dictionary out
# def forecast(
#     df, interval=DEFAULT_INTERVAL, periods=DEFAULT_PERIODS, model_options=None
# ):
#    model_options = model_options or DEFAULT_MODEL_OPTIONS
#    return {
#        "forecast_status": "success",
#        "data": out[output_rows_to_keep].to_dict(orient="records"),
#    }


# clean() functions
def dict_to_df(dict_input):
    df = pd.DataFrame(dict_input)
    return(df)

def format_delta(df):
    df.read_time = pd.to_datetime(df.read_time) 
    delta = df.volume.diff()
    delta = delta.rename('delta')
    df = pd.concat([df, delta], axis = 1)
    cols = [0,1,2,6]
    df = df.drop(df.columns[cols], axis = 1)
    df = pd.DataFrame(df, columns = ['read_time', 'delta'])
    df.columns = ['ds','y']
    df.y = df.y.clip(lower = 0, upper = 250)    
    return(df)

def half_hour(df):
    df = df.set_index('ds').groupby(pd.Grouper(freq='30min')).sum()
    df.reset_index(level = 0, inplace = True)
    df.drop(df.tail(1).index, inplace = True)
    return(df)

# this is the function you should call to clean the dict list
def clean(dict_input):
    df = dict_to_df(dict_input)
    df = format_delta(df)
    df = half_hour(df)
    return(df)


# forecast_near() functions
def gen_future(df, periods = 48):
    start_0 = df.iloc[-1, 0]  
    future = pd.date_range(start=start_0, freq="30min", periods=periods) + pd.Timedelta(minutes = 30)
    future = pd.Series(future)
    return(future)

def ar8(df, prediction_count):
    df = df[::-1].reset_index().drop('index', axis = 1)
    mod = sm.tsa.SARIMAX(df.y, order=(8, 0, 0))
    res = mod.fit()
    yhat = res.get_prediction(start=1, end=prediction_count).summary_frame()
    yhat = yhat.reset_index().drop('index', axis = 1)
    return(yhat)

def forecast_near(df, length = 48):
    future = gen_future(df, periods = length)
    yhat = ar8(df, prediction_count = length)
    out = pd.concat([future, yhat], axis = 1)
    
    out.rename(columns = {0:'ds', 
                      'mean':'yhat',
                      'mean_se':'se',
                      'mean_ci_lower':'lower',
                      'mean_ci_upper':'upper'
                     }, inplace = True)
        
    for field in ["yhat", "lower", "upper"]:
        out.loc[out[field] < 0, field] = 0
        
    out = out.to_dict(orient="records")

    return(out)


# forecast far functions
def aggregate_to_daily(df):
    df = df.set_index('ds').groupby(pd.Grouper(freq='D')).sum()
    df.reset_index(inplace = True)
    return(df)

def gen_future_daily(df, periods = 30): 
    start_0 = df.iloc[-1, 0] # timedelta + 1 is used to properly start prediction interval
    future = pd.date_range(start=start_0, freq="1D", periods=periods) + pd.Timedelta(days = 1)
    future = pd.DataFrame(future)
    future.rename(columns = {0:'ds'}, inplace = True)
    return(future)

def add_dow(df): # this just adds labels for mon - sun (0-6)
    day_of_week = pd.Series([], dtype='int', name ='dow')
    for i in range(0, len(df)):
        day_of_week[i] = datetime.weekday(df.ds[i])
    return(pd.concat([day_of_week, df], axis = 1))

# forecast_far is the actual function to call for a full prediction
def forecast_far(df, length = 30):
    
    # make sure the previous data is given in daily interval
    past = aggregate_to_daily(df)
    past_dow = add_dow(past)
    
    # three and four week averages dampen the seasonality too much
    # four_week = past_dow.rolling(4, on = 'dow').mean()
    # three_week = past_dow.rolling(3, on = 'dow').mean()
    two_week = past_dow.rolling(2, on = 'dow').mean()
    one_week = past_dow.rolling(1, on = 'dow').mean()

   # if sum(past.y.tail(28) == 0) == 0:
   #     pred = four_week
   # elif sum(past.y.tail(21) == 0) == 0:
   #     pred = three_week
    if sum(past.y.tail(14) == 0) == 0:
        pred = two_week
    elif sum(past_dow.y.tail(7) == 0) == 0:
        pred = one_week
    else:
        return(print('error not enough data'))
    
    # confidence interval calculation
    sample = past_dow.tail(14)  # take the last two weeks
    var = sample.groupby('dow').var() # calculate the variance by day
    se = var.y.apply(sqrt)/2 # square root and divide by 2
    se = pd.DataFrame(se) # add se to output
    se.reset_index(inplace=True) 
    se.rename(columns = {'y':'se'}, inplace = True)
    
    # estimates are the most recent moving averages
    yhat = pred.tail(7)
    
    # create future dataframe
    future = gen_future_daily(past, periods = length)
    future = add_dow(future)
    
    # combine future output with predictions and standard errs
    out = pd.merge(left = future, right =  yhat)
    out = pd.merge(left = out, right = se, on = 'dow')
    out = out.sort_values(by='ds')
    out.rename(columns = {'y':'yhat'}, inplace = True)
    out.reset_index(inplace=True)
    out = out.drop('index', axis = 1)
    out['lower'] = out.yhat - (2*out.se) 
    out['upper'] = out.yhat + (2*out.se)
    
    # non-negative estimates only
    for field in ["yhat", "lower", "upper"]:
        out.loc[out[field] < 0, field] = 0
    
    out = out.to_dict(orient="records")

    return(out)




