import os
import io
import logging
import json
import pandas as pd
import datetime
import pytz
from google.cloud import bigquery
from google.cloud import storage

def download_blob_gcs(gcs_uri, filepath=None, storage_client=None, output_option='FILE', delete_blob=False):
    """ Downloads blob from Google Cloud Storage to local drive or buffer

    Arguments:
        gcs_uri {str} -- google cloud storage blob uri e.g. gs://bucketname/foldername/blobname.csv

    Arguments:
        filepath {str} -- folder_path/new_filename (default: current_working_directory/blob_name)
        storage_client {google.storage.Client} -- storage client instantiated with non-default credentials (default: {None})
        output_option {str} -- determines function output type. (default: {'FILE'})
        delete_blob {bool} -- flag for deleting the blob after download is successful (default: {False})

    Returns:
        output_option : return type
        {STRING : unicode string}
        {IO : io.BytesIO}
        {URL: downloadable link}
        {CREDENTIALS: google.oauth2.service_account.Credentials}
        {JSON: DICT}
        {FILE: filepath} 
    """
    from google.oauth2.service_account import Credentials
    
    if not storage_client:
        logging.debug(
        "instantiating storage client from defualt environment variable")
        storage_client = storage.Client()

    bucket = gcs_uri[5:].split('/')[0]
    blob = '/'.join(gcs_uri[5:].split('/')[1:])
    blob = storage_client.get_bucket(bucket).get_blob(blob)
    
    logging.debug(
    f"storage client {storage_client.get_service_account_email()} is requesting access to blob: {blob} at {gcs_uri} ")

    if output_option == 'IO':
        output = io.BytesIO()
        blob.download_to_file(output)
        output.seek(0)

    elif output_option == 'STRING':
        output = blob.download_as_string().decode()
    
    elif output_option == 'JSON':
        output = json.loads(blob.download_as_string().decode())

    
    elif output_option == 'CREDENTIALS':
        output = Credentials.from_service_account_info(json.loads(blob.download_as_string().decode()))
    
    elif output_option == 'URL':
        expiration_duration = datetime.timedelta(weeks=1)
        output = blob.generate_signed_url(expiration_duration)
        

    else:
        if not filepath:
            filepath = gcs_uri.split("/")[-1]
        with open(filepath, mode="wb") as file_obj:
            storage_client.download_blob_to_file(gcs_uri, file_obj)
        output = filepath

    if delete_blob:
        blob.delete()

    return output

def upload_blob_gcs(content, bucket_id=None, blobname=None,storage_client=None):
    """ Uploads content to Google Cloud Storage

    Arguments:
        content {str, filepath, io.BytesIO} -- string, filepath or BytesIO to be uploaded

    Keyword Arguments:
        bucket_id {str} -- google cloud storage bucket id (default: default bucket from env variable "STORAGE_BUCKET")
        blobname {str} -- blob name, for string and BytesIO name should be provided (default: {unname_blob_uploaded_at_timestamp})
        storage_client {google.storage.Client} -- storage client instantiated with non-default credentials (default: {None})

    Return:
        {str} -- returns google cloud storage uri of uploaded blob
    """

    if not storage_client:
        logging.debug(
        "instantiating storage client from defualt environment variable")
        storage_client = storage.Client()
        
    if not bucket_id:
        bucket_id = os.environ.get("STORAGE_BUCKET")
    
    if not blobname:
        if os.path.isfile(content):
            blobname = os.path.basename(content)
            storage_client.get_bucket(bucket_id).blob(blobname).upload_from_filename(content)
            return f'gs://{bucket_id}/{blobname}'
        else:
            blobname = 'unname_blob_uploaded_at' + datetime.datetime.now().isoformat().replace('-','_').replace(':','_')[:19]

    if isinstance(content, io.BytesIO):
        storage_client.get_bucket(bucket_id).blob(blobname).upload_from_file(content)
    else:
        storage_client.get_bucket(bucket_id).blob(blobname).upload_from_string(content)

    return f'gs://{bucket_id}/{blobname}'

def bq_to_df(sql, client=None, **job_config):
    """ Returns bigquery query result as pandas dataframe

    Arguments:
        sql {str} -- bigquery SELECT statement in standard SQL or stored procedure containing SELECT statement

    Keyword Arguments:
        client {bigquery.Client} -- defaults to client instantiated with default credentials
        job_config {dict} -- keyword arguemnt for bigquery.QueryJob.Config()

    Returns:
        pandas.DataFrame -- query result as df
    """
    if not client:
        logging.debug(
        "instantiating bigquery client from defualt environment variable")
        client = bigquery.Client()

    def get_date_columns(job):
        """ returns list of DATE columns from bigquery.job object
        """
        return [field.name for field in job.result().schema if field.field_type == 'DATE']

    def transform_date(date_colums):
        """ castes datetime.date to pd.datetime as pantab doesn't handle datetime.date objects"""
        for col in date_colums:
            df[col] = pd.to_datetime(df[col])

    job_config = bigquery.QueryJobConfig(**job_config)

    dry_run = bigquery.QueryJobConfig(
        dry_run=True, use_query_cache=False)
    job = client.query(sql, job_config=dry_run)

    if job.statement_type == 'SELECT':
        job_id = create_bq_job_id(
            'hyper publiser app SELECT Statment request')

        job = client.query(sql, job_id=job_id, job_config=job_config)
        # job.result()
        df = job.to_dataframe()
        # job_info = get_job_info(job,client=client)
        date_colums = get_date_columns(job)

        if date_colums:
            transform_date(date_colums)

    elif job.statement_type == 'SCRIPT':
        job_id = create_bq_job_id(
            'hyper publiser app script request')
        job = client.query(sql, job_id=job_id, job_config=job_config)
        job.result()
        job_id = get_job_info(job,client=client, output_option='LIST')

        if len(job_id) == 1:
            df = client.get_job(job_id[0]).to_dataframe()
            # job_info = get_job_info(job,client=client)
            date_colums = get_date_columns(job)

            if date_colums:
                transform_date(date_colums)

        elif len(job_id) > 1:
            df = client.get_job(job_id[-1]).to_dataframe()
            # job_info = get_job_info(job,client=client)
            logging.waring(
                " multi select stored procedure returns data for the last SELECT statement only")
            date_colums = get_date_columns(job)

            if date_colums:
                transform_date(date_colums)

        else:
            logging.error(f"{sql} script did not return any data")
            df = None
    else:
        logging.error(
            f"{job.statement_type} are not suppoted. Please provide a SELECT statement or a stored procedure containing SELECT statement")
        return
        # job_info = get_job_info(job,client=client)
        # logging.info(f"job execution detail: {job_info}")
    logging.info(f"{job.statement_type} statement returned {len(df)} rows")

    return df

def df_to_bq(df, table_id, client=None, write_mode='WRITE_APPEND', schema=None, autodetect=False, job_id=None,**job_config):
    """ loads dataframe to bigquery with custom datatype and schema

    Arguments:
        df {pd.DataFrame} -- pandas dataframe to be updoad
        table_id {str} -- fully qualified bq table id as write destination e.g. project_id.dataset.new_tablename
        client {bigquery.Client} -- defaults to client instantiated with default credentials
        write_mode {str} -- optional argument. Valid values are 'WRITE_APPEND' , 'WRITE_TRUNCATE' OR 'WRITE_EMPTY'. defaults to WRITE_APPEND mode
        schema {bigquery table schema} -- optional, schema of bigquery table, use get_table_schema(table_id) to enforce existing table schema
        autodetect {bool} -- optional, if True, infers datatype, deaults to False
        job_id {str} -- optional argument, use function create_bq_job_id(description=None) to create custom job id

    Returns:
        Biqquery job object
        """
    if not client:
        logging.debug(
        "instantiating bigquery client from defualt environment variable")
        client = bigquery.Client()

    job_config = bigquery.LoadJobConfig(**job_config)
    job_config.autodetect = autodetect
    job_config.write_disposition = write_mode
    job_config.create_disposition = 'CREATE_IF_NEEDED'
    if schema:
        job_config.schema = schema

    load_job = client.load_table_from_dataframe(
        df, table_id, job_id=job_id, job_config=job_config)
    return load_job


def create_bq_job_id(description=None):
    """creates custom job id for bigquery jobs (load job, export, query, DML statements etc) with yyymmdd_hhmmss_EST_description pattern

    Arguments:
        description {str} -- description of job, use searchable terms to pull the job from logs (default: service_account_email prefix)

    Returns:
        job_id {str} -- custom job Id with yyymmdd_hhmmss_EST_description pattern
    """
    timezone = pytz.timezone("America/New_York")
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    est_now_str = utc_now.astimezone(pytz.timezone(
        "America/New_York")).strftime("%Y%m%d_%H%M%S_EST")

    if description:
        description = description.replace(' ', '_')
        job_id = est_now_str + f"_{description}"
    else:
        agent = client.get_service_account_email()
        job_id = est_now_str + f"_{agent.split('@')[0]}"
    return job_id


def get_table_schema(table_id, client=None, output_option='OBJECT'):
    """Returns table schema of Biqquery Table

    Arguments:
        table_id {str} -- fully qualified table id e.g. project_id.dataset.new_tablename

    Keyword Arguments:
        client {bigquery.Client} -- defaults to client instantiated with default credentials
        output_option {str} -- determines return data type {'OBJECT'|'LIST'|'DICT'} where 'object' is bigquery.table.schema object
        , 'list' returns list of columns names, 'dict' returns list of dictionary for each field : field_type. (default: bigquery schema object)

    Returns:
        biqquery schema object|list of str|list of dict containing fields definition
    """
    if not client:
        logging.debug(
        "instantiating bigquery client from defualt environment variable")
        client = bigquery.Client()

    if output_option == 'LIST':
        return [field.name for field in client.get_table(table_id).schema]
    elif output_option == 'DICT':
        return [{field.name: field.field_type for field in client.get_table(table_id).schema}]
    else:
        return client.get_table(table_id).schema


def get_job_info(job, client=None, output_option=None):
    """ For query jobs: returns job_id, statement_type, number_of_row_affected, destination_table_path and children job info
    For laod jobs: return job_id, job_type, destination_table, write_mode, number of output rows and errors encountered

    Arguments:
        job {bigquery job object} -- query or load job

    Keyword Arguments:
        client {bigquery.Client} -- defaults to client instantiated with default credentials
        output_option {str} -- optional output for SCRIPT statement. 'LIST' retruns filtered list of children job_id of SELECT type where result total_row > 1. 'DICT' returns details of children jobs of SELECT type (default: {None})

    Returns:
        dict | list -- job info is dict, while children job info is list

    Example:
    get_job_info(client.query(sql_statement)) # returns job_info

    # for SCRIPT, returns detail of children jobs of SELECT statements
    get_job_info(script_job, output_option='DICT')
    """
    if not client:
        logging.debug(
        "instantiating bigquery client from defualt environment variable")
        client = bigquery.Client()

    def extract_table_id(job_destination_path):
        return f"{job_destination_path.split('/')[2]}.{job_destination_path.split('/')[4]}.{job_destination_path.split('/')[6]}"

    if job.job_type == 'query':
        if job.statement_type == 'SCRIPT':
            child_jobs_iterable = client.list_jobs(parent_job=job)
            children = [{'job_id': job.job_id, 'statement_type': job.statement_type, 'destination': extract_table_id(job.destination.path),
                         'num_dml_affected_rows': job.num_dml_affected_rows} if job.statement_type != 'SELECT' else {'job_id': job.job_id, 'statement_type': job.statement_type,
                                                                                                                     'total_rows': job.result().total_rows, 'destination': extract_table_id(job.destination.path), 'schema': get_table_schema(extract_table_id(job.destination.path), client=client, output_option='DICT')} for job in child_jobs_iterable]
            data = {'job_id': job.job_id, 'statement_type': job.statement_type,
                    'num-child_jobs': job.num_child_jobs, 'child_job': children}

            if output_option == 'LIST':
                children_job_id_SELECT = [job.get('job_id') for job in data.get(
                    'child_job') if job.get('statement_type') == 'SELECT' and job.get('total_rows') > 1]
                data = children_job_id_SELECT

            elif output_option == 'DICT':
                children_job_id_SELECT = [job.get('job_id') for job in data.get(
                    'child_job') if job.get('statement_type') == 'SELECT']
                data = [{'job_id': child, 'statement_type': 'SELECT', 'total_rows': client.get_job(child).result(
                ).total_rows, 'destination': extract_table_id(client.get_job(child).destination.path)} for child in children_job_id_SELECT]

        elif job.statement_type == 'SELECT':
            data = {'job_id': job.job_id, 'statement_type': job.statement_type,
                    'total_rows': job.result().total_rows, 'destination': extract_table_id(job.destination.path), 'schema': get_table_schema(extract_table_id(job.destination.path), client=client,output_option='DICT')}
        else:
            data = {'job_id': job.job_id, 'statement_type': job.statement_type,
                    'destination': extract_table_id(job.destination.path), 'num_dml_affected_rows': job.num_dml_affected_rows}
    else:
        data = {'job_id': job.job_id, 'job_type': job.job_type,
                'destination': extract_table_id(job.destination.path), 'write_mode': job.write_disposition, 'output_rows': job.output_rows, 'errors': job.errors}
    return data


def get_gcp_service_account(credentials):
    """ returns google.oauth2.service_account.Credentials from local filepath, gcs_uri or dict

    Arguemnts:
    credentials {str, bytes, dict}
    """
    from google.oauth2.service_account import Credentials
    if isinstance(credentials,dict):
        credentials = Credentials.from_service_account_info(credentials)
        logging.debug(f"project_id: {credentials.project_id} service_account_email: {credentials.service_account_email}")
    else:
        if os.path.isfile(credentials):
            credentials = Credentials.from_service_account_file(credentials)
            logging.debug(f"project_id: {credentials.project_id} service_account_email: {credentials.service_account_email}")
            
        elif isinstance(credentials,bytes):
            credentials = Credentials.from_service_account_info(json.loads(credentials))
            logging.debug(f"project_id: {credentials.project_id} service_account_email: {credentials.service_account_email}")

        elif 'gs://' in credentials:
            credentials = download_blob_gcs(credentials,output_option='CREDENTIALS')
            logging.debug(f"project_id: {credentials.project_id} service_account_email: {credentials.service_account_email}")
        else:
            credentials = Credentials.from_service_account_info(json.loads(credentials))
            logging.debug(f"project_id: {credentials.project_id} service_account_email: {credentials.service_account_email}")

    return credentials
