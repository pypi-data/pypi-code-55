import numpy as np
import pandas as pd
import statsmodels.api as sm
from datetime import timedelta, datetime
from sklearn.metrics import mean_absolute_error
from fbprophet import Prophet
from math import sqrt

### reference this for future improvements
#DEFAULT_INTERVAL = timedelta(minutes=10)
#DEFAULT_PERIODS = 6 * 48  # 10 mins * 6 * 48 = 2 days
#DEFAULT_MODEL_OPTIONS = {"type": "areg"}
# df in, dictionary out
# def forecast(
#     df, interval=DEFAULT_INTERVAL, periods=DEFAULT_PERIODS, model_options=None
# ):


### clean functions
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

# this is the function that should be called to clean the data
def clean(dict_input):
    df = dict_to_df(dict_input)
    df = format_delta(df)
    df = half_hour(df)
    return(df)



# forecast near functions
def gen_future(df, periods = 48):
    start_0 = df.iloc[-1, 0]  
    future = pd.date_range(start=start_0, freq="30min", periods=periods) + pd.Timedelta(minutes = 30)
    future = pd.DataFrame(future)
    future.rename(columns = {0:'ds'}, inplace = True) 
    return(future)

def fbp(df, future):
    m = Prophet(changepoint_prior_scale=0.5, 
                weekly_seasonality = True, 
                yearly_seasonality = False).add_seasonality(name = 'custom',
                                                            period = 48, 
                                                            fourier_order = 8, 
                                                            prior_scale=0.01)
    mod = m.fit(df)
    yhat = m.predict(future)
    out = yhat[['ds','yhat_lower', 'yhat_upper', 'yhat']]

    return(out)

# this is the function that should be called to make the forecast
def forecast_near(df, length = 48, output = 'dict'):
    
    status_dict = {
        0: 'Forecast Failed: not enough data were provided.',
        1: 'Forecast Failed: prediction accuracy threshold was not met.',
        2: 'Warning: Unstable forecast - not enough data were provided.',
        3: 'Warning: Unstable forecast - predicted values are unreliable.',
        4: 'Forceast Succeeded'
    }
    
    if len(df.y) >= 400:
        status = 4
    elif len(df.y) >= 310:
        status = 2
    else:
        return({'status': status_dict[0]}) # not enough data
    
### Backcasting for accuracy check ###  
 #   index = len(df)-144
 #   train = df[:index]
 #   test_yhat = fbp(train, test)
 #   mae = mean_absolute_error(test_yhat['yhat'], test.y) # calculate MAE

 #   if mae <= 150:
 #       status = 4
 #   elif mae <= 200:
 #       status = 3
 #   else:
     #   return({'status': status_dict[1]}) # bad predictions
 #       status = 1
        
    future = gen_future(df, periods = length)
    out = fbp(df, future)
    
    # clean up output
    out.rename(columns = {                  
                      'yhat_lower':'lower',
                      'yhat_upper':'upper'
                     }, inplace = True)
        
    for field in ["yhat", "lower", "upper"]:
        out.loc[out[field] < 0, field] = 0

    # return desired output (dict or df)
    if output == 'df':
        return(out)
    else:
        return(
            {
                "status": status_dict[status],
                "data": out.to_dict(orient="records"),
            }
            )



### forecast far functions
def aggregate_to_daily(df):
    df = df.set_index('ds').groupby(pd.Grouper(freq='D')).sum()
    df.reset_index(inplace = True)
    return(df)

def gen_future_daily(df, periods = 30): 
    start_0 = df.iloc[-2, 0] # starts on current, uncompleted day
    future = pd.date_range(start=start_0, freq="1D", periods=periods) + pd.Timedelta(days = 1)
    future = pd.DataFrame(future)
    future.rename(columns = {0:'ds'}, inplace = True)
    return(future)

def add_dow(df): # this just adds labels for mon - sun (0-6)
    day_of_week = pd.Series([], dtype='int', name ='dow')
    for i in range(0, len(df)):
        day_of_week[i] = datetime.weekday(df.ds[i])
    return(pd.concat([day_of_week, df], axis = 1))

# this is the function that should be called to make the forecast
def forecast_far(df, length = 30, output = 'dict'):
    
    status_dict = {
        0: 'Forecast Failed: Not enough data were provided.',
        1: 'Warning: Unstable forecast - not enough data were provided.',
        2: 'Warning: Unstable forecast - predicted values may be unreliable.',
        3: 'Forceast Succeeded'
    }

    # make sure the previous data is given in daily interval
    past = aggregate_to_daily(df)
    past_dow = add_dow(past)
    
    # define rolling averages
    two_week = past_dow.rolling(2, on = 'dow').mean()
    one_week = past_dow.rolling(1, on = 'dow').mean()
    
    # calculate differences the two predicted values
    diff = one_week.iloc[-8:-1] - two_week.iloc[8:-1]
    any(diff.y > 1000) or any(diff.y < -1000)

    # verify there is at least 1 week of data, preferrably 2
    if len(past.tail(15).y) == 15 and all(past.tail(15).y != 0):
        status = 3
        pred = two_week
        
        # if the predictions are very different, throw a warning
        diff = one_week.iloc[-8:-1] - two_week.iloc[8:-1]
        if any(diff.y > 1000) or any(diff.y < -1000): 
            status = 2
            pred = two_week
    
    # only the previous week's data can be used
    elif len(past.tail(15).y) >= 8 and all(past.tail(8).y != 0):
        status = 1
        pred = one_week
    
    # not enough data to use mean method
    else:
        status = 0
        return({'status': status_dict[0]})

    # confidence interval calculation
    if status == 3 or status == 2: # for the two week means prediction se = sigma/sqrt(n)
        sample = past_dow.iloc[-15:-1]  
        var = sample.groupby('dow').var() 
        se = var.y.apply(sqrt)/1.414 
        se = pd.DataFrame(se) 
        se.reset_index(inplace=True) 
        se.rename(columns = {'y':'se'}, inplace = True)
    elif status == 1: # for the one week mean, se = 20%
        se = pd.DataFrame(past_dow.iloc[-8:-1]) 
        se.y = se.y * 0.2 # 
        se.rename(columns = {'y':'se'}, inplace = True)
        se.drop(columns='ds', inplace = True)

    # estimates are always based on the most recent moving averages, excluding current day
    yhat = pred.iloc[-8:-1]
    
    # create future dataframe
    future = gen_future_daily(past, periods = length)
    future = add_dow(future)
    
    # combine future output with predictions and standard errs by day of week
    out = pd.merge(left = future, right = yhat)
    out = out.sort_values(by='ds')

    # clean up output
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
    
    # return desired output (dict or df)
    if output == 'df':
        return(out)
    else:
        return(
            {
                "status": status_dict[status],
                "data": out.to_dict(orient="records"),
            }
            )