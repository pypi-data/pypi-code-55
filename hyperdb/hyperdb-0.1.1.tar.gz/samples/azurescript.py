"""save the script on azure storage account and provide blob_uri to pivotal app""


import requests
import pandas as pd
from io import BytesIO


def create_df():
    """requests data from http and returns dataframe to be converted to hyper

    Returns:
        pandas dataframe
    """

    url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/abalone/abalone.data'
    response = requests.request('GET', url, verify=False)
    print(
        f'response code for request to {response.url} is {response.status_code}')
    in_mem_file = BytesIO(response.content)
    in_mem_file.seek(0)
    col_names = ['Sex', 'Length', 'Diameter', 'Height', 'Whole_weight',
                 'Shucked_weight', 'Viscera_weight', 'Shell_weight', 'Rings']
    return pd.read_csv(in_mem_file, sep=',', header=None, names=col_names)
