# live function
import numpy as np
import pandas as pd
import statsmodels.api as sm
from datetime import timedelta, datetime
from sklearn.metrics import mean_absolute_error
from math import sqrt

### reference this for future improvements
#DEFAULT_INTERVAL = timedelta(minutes=10)
#DEFAULT_PERIODS = 6 * 48  # 10 mins * 6 * 48 = 2 days
#DEFAULT_MODEL_OPTIONS = {"type": "areg"}
# df in, dictionary out
# def forecast(
#     df, interval=DEFAULT_INTERVAL, periods=DEFAULT_PERIODS, model_options=None
# ):


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



# forecast_near functions
def gen_future(df, periods = 48):
    start_0 = df.iloc[-1, 0]  
    future = pd.date_range(start=start_0, freq="30min", periods=periods) + pd.Timedelta(minutes = 30)
    future = pd.Series(future)
    return(future)

def ar8(df, prediction_count):
    mod = sm.tsa.SARIMAX(df.y, order=(8, 0, 0), trend = 't')
    res = mod.fit()
    yhat = res.get_prediction(start=1, end=prediction_count).summary_frame()
    yhat = yhat[::-1] # this is it?
    yhat = yhat.reset_index().drop('index', axis = 1)
    return(yhat)

def forecast_near(df, length = 48):
    
    status_dict = {
        0: 'Forecast Failed: Not enough data were provided.',
        1: 'Warning: Unstable forecast - not enough data were provided.',
        2: 'Warning: Unstable forecast - predicted values are unreliable.',
        3: 'Forceast Succeeded'
    }
    
    if len(df.y) >= 144:
        status = 3
    elif len(df.y) >= 24:
        status = 1
    else:
        status = 0
        return(status_dict[status])
    
    # test accuracy of recent predictions
    index = len(df)-144
    train = df[:index] # make a model excluding last 72 hours of obs
    test_yhat = ar8(train, 144) 
    test = df[index:] # test against last 72 hours
    mae = mean_absolute_error(test_yhat['mean'], test.y) # calculate MAE
    
    if mae < 100: # arbitrary cutoff
        status = 3 # good model
    elif mae < 200: 
        status = 2 # bad model
    else:
        status = 0 # horrible model
        return(status_dict[status])

    # 72-hour check isn't horrible, continue
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
        
  #  return(out)

    return(
    {
        "status": status_dict[status],
        "data": out.to_dict(orient="records"),
    }
    )



# forecast_far functions
def aggregate_to_daily(df):
    df = df.set_index('ds').groupby(pd.Grouper(freq='D')).sum()
    df.reset_index(inplace = True)
    return(df)

def gen_future(df, periods = 30): 
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
def aggregate_to_daily(df):
    df = df.set_index('ds').groupby(pd.Grouper(freq='D')).sum()
    df.reset_index(inplace = True)
    return(df)

def gen_future(df, periods = 30): 
    start_0 = df.iloc[-2, 0]
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
    
    status_dict = {
        0: 'Forecast Failed: Not enough data were provided.',
        1: 'Warning: Unstable forecast - not enough data were provided.',
        2: 'Warning: Unstable forecast - predicted values are unreliable.',
        3: 'Forceast Succeeded'
    }

    # make sure the previous data is given in daily interval
    past = aggregate_to_daily(df)
    past_dow = add_dow(past)
    
    # define rolling averages
    two_week = past_dow.rolling(2, on = 'dow').mean()
    one_week = past_dow.rolling(1, on = 'dow').mean()

    # verify there is at least 1 week of data, preferrably 2
    if len(past.tail(15).y) == 15 and all(past.tail(15).y != 0):
        status = 3
        pred = two_week
    elif len(past.tail(15).y) >= 8 and all(past.tail(8).y != 0):
        status = 1
        pred = one_week
    else:
        status = 0
        return({'status': status_dict[0]})
    
    # confidence interval calculation
    if status == 3:
        sample = past_dow.iloc[-15:-1]  # take the last two weeks
        var = sample.groupby('dow').var() # calculate the variance by day
        se = var.y.apply(sqrt)/2 # square root and divide by 2
        se = pd.DataFrame(se) # add se to output
        se.reset_index(inplace=True) 
        se.rename(columns = {'y':'se'}, inplace = True)
    elif status == 1:
        se = pd.DataFrame(past_dow.iloc[-8:-1]) # add se to output
        se.y = se.y * 0.2 # 
        se.rename(columns = {'y':'se'}, inplace = True)
        se.drop(columns='ds', inplace = True)

    # estimates are always based on the most recent moving averages
    yhat = pred.iloc[-8:-1]
    
    # create future dataframe
    future = gen_future(past, periods = length)
    future = add_dow(future)
    
    # combine future output with predictions and standard errs
    out = pd.merge(left = future, right = yhat)
    out = out.sort_values(by='ds')

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
   
   # return(out)
    
    return(
    {
        "status": status_dict[status],
        "data": out.to_dict(orient="records"),
    }
    )