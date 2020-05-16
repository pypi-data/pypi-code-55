from fmi import FMI
from regression_model.config import config
from datetime import date, datetime
import pandas as pd
import numpy as np

def get_forecast(place):
    f = FMI(place=place)
    forecast = f.forecast()
    #make it into a dataframe
    df = pd.DataFrame()
    for i,observation in enumerate(forecast):
        df_temp = pd.DataFrame(observation.__dict__, index=np.arange(i,i+1))
        df = pd.concat([df,df_temp], axis=0)

    #get the global radiation to proper values
    df[config.GLOBAL_RADIATION] = df[config.RADIATION_ACCUMULATION].diff()/3600
    # discard first row
    df = df.loc[1:]
    df =  df.drop(columns=config.FORECAST_TO_DROP)
    df.columns = config.FEATURES
    # to go along with WeatherDataRequestSchema of the API we change
    # 'datetime_converted' to a string
    df[config.DATETIME_INDEX] = df[config.DATETIME_INDEX].astype(str)
    return df
