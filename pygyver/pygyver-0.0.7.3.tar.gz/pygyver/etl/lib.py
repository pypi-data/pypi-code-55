""" Functions used in different places ;) """
import os
from os import path
import json
from datetime import date, timedelta
from google.cloud import bigquery
from pygyver.etl.toolkit import validate_date


def set_write_disposition(write_disposition):
    """ Sets bigquery.WriteDisposition based on write_disposition """
    if write_disposition == 'WRITE_APPEND':
        return bigquery.WriteDisposition.WRITE_APPEND
    elif write_disposition == 'WRITE_EMPTY':
        return bigquery.WriteDisposition.WRITE_EMPTY
    elif write_disposition == 'WRITE_TRUNCATE':
        return bigquery.WriteDisposition.WRITE_TRUNCATE
    else:
        raise KeyError("{} is not a valid write_disposition key".format(write_disposition))


def set_priority(priority):
    """ Sets bigquery.QueryPriority based on write_disposition """
    if priority == 'BATCH':
        return bigquery.QueryPriority.BATCH
    elif priority == 'INTERACTIVE':
        return bigquery.QueryPriority.INTERACTIVE
    else:
        raise KeyError("{} is not a valid priority key".format(priority))


def read_table_schema_from_file(path):
    """
    Read table schema from json file.

    Arguments:
        - path: full path to schema file from folder pipelines
    """
    full_path = os.path.join(os.environ.get("PROJECT_ROOT"), path)
    with open(full_path, 'r') as file_path:
        json_schema = json.load(file_path)
        return bigquery.schema._parse_schema_resource({'fields': json_schema})


def bq_token_file_path():
    """
    Returns GOOGLE_APPLICATION_CREDENTIALS if env is set
    """
    return os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '')


def bq_token_file_path_exists(token_path):
    """
    Returns True if the file exists, False otherwise
    """
    return path.exists(token_path)


def bq_token_file_valid():
    """
    Checks whether the token file is valid.
    """
    token_path = bq_token_file_path()
    if token_path == '':
        raise ValueError(
            "Please set GOOGLE_APPLICATION_CREDENTIALS to the path to the access token."
        )
    elif bq_token_file_path_exists(token_path) is False:
        raise ValueError(
            "Token file could not be found. Please reset your GOOGLE_APPLICATION_CREDENTIALS env var. Current:",
            token_path
        )
    else:
        return True


def bq_use_legacy_sql():
    """
    Returns BIGQUERY_LEGACY_SQL if env is set
    """
    return os.environ.get('BIGQUERY_LEGACY_SQL', 'TRUE')


def bq_default_project():
    """
    Returns BIGQUERY_PROJECT if env is set
    """
    return os.environ.get('BIGQUERY_PROJECT', '')


def bq_default_dataset():
    """
    Returns BIGQUERY_DATASET if env is set
    """
    return os.environ.get('BIGQUERY_DATASET', '')


def bq_billing_project():
    """
    Returns BIGQUERY_PROJECT if env is set
    """
    return bq_default_project()


def bq_start_date():
    """
    Returns BIGQUERY_START_DATE if env is set. Defaults to '2016-01-01'.
    """
    start_date = os.environ.get('BIGQUERY_START_DATE', '2016-01-01')
    validate_date(
        start_date,
        error_msg="Invalid BIGQUERY_START_DATE: {} should be YYYY-MM-DD".format(start_date)
    )
    return start_date


def bq_end_date():
    """
    Returns BIGQUERY_LEGACY_SQL if env is set. Defaults to Yesterday.
    """
    yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    end_date = os.environ.get('BIGQUERY_END_DATE', yesterday)
    validate_date(
        end_date,
        error_msg="Invalid BIGQUERY_END_DATE: {} should be YYYY-MM-DD".format(end_date)
    )
    return end_date


def remove_first_slash(word=''):
    if word == '':
        return word
    if word[0] == '/':
        return word[1:]
    return word

# AWS


def s3_default_bucket():
    """
    Returns BIGQUERY_PROJECT if env is set
    """
    return os.getenv('AWS_S3_BUCKET', '')


def s3_default_root():
    """
    Returns BIGQUERY_PROJECT if env is set
    """
    return os.environ.get('AWS_S3_ROOT', '')


def extract_args(content, to_extract: str):
    return [x.get(to_extract, '') for x in content if x.get(to_extract, '') != '']


def gcs_default_project():
    """
    Returns GOOGLE_CLOUD_PROJECT if env is set
    """
    return os.environ.get('GCS_PROJECT', '')


def gcs_default_bucket():
    """
    Returns GCS_BUCKET if env is set
    """
    return os.environ.get('GCS_BUCKET', '')
