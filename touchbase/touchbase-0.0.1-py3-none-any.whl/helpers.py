import json
import numpy as np
import pandas as pd
import requests
import os

with open('config/global.json') as f: config = json.load(f)    

def get_job(filename):
    with open('config/jobs.json') as f:
        jobs = json.load(f)
    job = jobs[filename]
    return job

def stringify_datetime_columns(df):
    datetime_columns = df.select_dtypes(include=[np.datetime64]).columns
    for col in datetime_columns:
        df[col] = df[col].dt.strftime('%Y-%m-%d')    
    return df

def get_df(filename): 
    watch_path = config['watched_folders'][0]
    df = pd.read_csv(watch_path + '/' + filename)
    df = stringify_datetime_columns(df)
    return df

def push_report(df, job, api_key):
    payload = {
        'table': df.to_json(orient='records'),
        'report_path': job['report_path'],
        'report_name': job['report_name'],
        'id_headers': job['id_headers'] if 'id_headers' in job else [],
        'api_key': api_key
    }
    r = requests.post(config['api_url'] + 'report/', json=payload)
    print('pushed ' + job['report_name'] +'; status: ' + str(r.status_code))
