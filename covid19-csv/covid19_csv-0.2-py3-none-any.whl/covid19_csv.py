import pandas as pd

def covid_csv(csvfile):
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    data = pd.read_csv(url)
    data = data.drop(['Lat','Long','Province/State'], axis = 1)
    data = data.melt(id_vars=['Country/Region'], var_name='date', value_name="Confirmed")
    data = data.astype({'date':'datetime64[ns]', "Confirmed":'Int64'}, errors='ignore')
    data['dateStr'] = data['date'].dt.strftime('%b %d, %Y')  # https://strftime.org/
    data.to_csv(csvfile)