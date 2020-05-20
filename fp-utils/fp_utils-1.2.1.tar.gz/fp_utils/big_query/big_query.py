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
def df_to_big_query(df, proj, ds, tb, creds_path, schema=None, overwrite=True):
    '''
    df (pandas dataframe): The data that you want uploaded to Big Query.
    proj (str): The name of the Big Query project.
    ds (str): The name of the Big Query dataset.
    tb (str): The name of the Big Query table.
    creds_path (str): Path to the service account json file (_eg. 'creds/google_creds.json'_)
    schema (dict): Schema of the Big Query dataset. Default is None. (UNTESTED)
    overwrite (bool):  True overwrites the existing table, False appends data to the end of the table.

    returns: Nothing (Might want to change this). 
    '''

    #Authenticate Big Query.
    client = bigquery.Client.from_service_account_json(creds_path, project=proj)

    #Connect to client.
    dataset = client.dataset(ds)
    table_id = proj + "." + ds + "." + tb
    table = dataset.table(tb)

    if overwrite:
        #Delete the table.
        client.delete_table(table_id)
        print("Deleted table " + table_id)

        #Create the table.
        if schema:
            table_ref = dataset.table('my_table')
            table = bigquery.Table(table_ref, schema=schema)
            table = client.create_table(table)  # API request
            table = bigquery.table.Table(table_id, schema)
        else:
            client.create_table(table_id)
        print("Created table " + table_id)

    #Load data to the table.
    client.load_table_from_dataframe(df, table).result()
    print("Uploaded DF to " + table_id)