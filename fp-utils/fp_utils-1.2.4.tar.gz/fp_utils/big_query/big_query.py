from google.oauth2 import service_account #Service Account
import pandas_gbq #Pandas GBQ.
from google.cloud import bigquery #To connect to BigQuery.


def read_big_query(query, project, creds_path):
    '''
    query (str): SQL query
    project (str): Then name of the Big Query project
    creds_path (str): Path to service account json file (_eg. 'creds/google_creds.json'_)

    returns: Pandas dataframe with query data.
    '''

    #Authenticate
    credentials = service_account.Credentials.from_service_account_file(creds_path)
    pandas_gbq.context.credentials = credentials

    #Read in dataframe.
    data_frame = pandas_gbq.read_gbq(
        query,
        project_id=project,
        dialect='standard')

    return data_frame

#Write DF to Big Query
def df_to_big_query(dataframe, project, dataset, table, creds_path):
    '''
    dataframe (pandas dataframe): The data that you want uploaded to Big Query.
    project (str): The name of the Big Query project.
    dataset (str): The name of the Big Query dataset.
    table (str): The name of the Big Query table.
    creds_path (str): Path to the service account json file (_eg. 'creds/google_creds.json'_)

    returns: Nothing (Might want to change this).
    '''

    client = bigquery.Client.from_service_account_json(creds_path, project=project)

    query = (f'SELECT * FROM `{dataset}.{table}`')
    query_job = client.query(query)
    big_query_table = query_job.result()
    table_ = big_query_table

    dataset_ref = client.dataset(dataset)
    dataset = bigquery.Dataset(dataset_ref)
    table_ref = dataset.table(table)
    table = bigquery.Table(table_ref)
    tschema = big_query_table.schema
    # convert dataframe to a list
    data = dataframe.values
    # convert list to dictionary
    macro = []
    for entry in data:
        micro = {}
        for i,item in enumerate(entry):
            micro[tschema[i].name] = item
        macro.append(micro.copy())

    errors = client.insert_rows(table,macro,selected_fields=tschema)
    return errors
