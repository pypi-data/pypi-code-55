"""
@author: Rob Lantz
@contact: rob@cloudframe.io
@doc: Connect to a Redshift instance, with helpers for common operations.
@note: MUST update .profile and .bashrc with the appropriate environment variables
       to find your Redshift cluster.  Also, must have the appropriate VPC security 
       group settings to allow communication between the instance and the cluster.
@todo: create setter functions
"""

import os
import psycopg2 as psy
import sys
import json
from time import time
from pathlib import Path
import numpy as np
import pandas as pd
import re
import io
import boto3

HM = str(Path.home())

# A simple date format for checking dates.
DT_FORMAT = "(\d{4}[-/]\d{1,2}[-/]\d{1,2})|(\d{1,2}[-/]\d{1,2}[-/]\d{4})"

from datascientist.special import s3session

### Look for the appropriate environment variables.

username = os.environ.get("RS_USER")
dbname = os.environ.get("RS_DBNM")
port = os.environ.get("RS_PORT")
passwd = os.environ.get("RS_PASS")
host = os.environ.get("RS_HOST")

### If they're not present, get them from a creds file

rscred_keys = ["REDSHIFT_USER_NAME", "REDSHIFT_DBNAME", "REDSHIFT_PORT", "REDSHIFT_PASSWORD", "REDSHIFT_HOST"]

if username is None:
    try:
        creds = json.load(open(hm + "/rs_creds.json", "r"))
        try:
            username = creds["REDSHIFT_USER_NAME"]
            dbname = creds["REDSHIFT_DBNAME"]
            port = creds["REDSHIFT_PORT"]
            passwd = creds["REDSHIFT_PASSWORD"]
            host = creds["REDSHIFT_HOST"]
        except:
            print("Found rs_creds.json, but it's not in the right format")
            print("Keys should include: {}".format(rscred_keys))
    except:
        print("Could not load credentials either from environment variables or rs_creds.json")
        print("Please set REDSHIFT_USER_NAME, etc either in your config (e.g. .bashrc) or in ~/rs_creds.json")

    
def get_connection():
    """
    @doc: Use psycopg2 to create a connection to a Redshift cluster.  Pulls from
          environment variables (accessible as statics in this module).
    @args: None
    @return: a psycopg2 connection object
    """
    connection = psy.connect(dbname = dbname, 
                             port = port, 
                             host = host, 
                             user = username, 
                             password = passwd)
    connection.set_session(autocommit = True)
    return connection

def get_engine_str():
    """
    @doc: a convenience function for examining the engine string.
    @args: None
    @return: a str with the postgresql engine string
    """
    return "postgresql://{0}:{1}@{2}:{3}/{4}".format(username,
                                                     passwd,
                                                     host,
                                                     port,
                                                     dbname)

def table_check(tname):
    """
    @doc: determnine whether or not a table exists in the Redshift cluster
    @args: tname is a str of the table name to check
    @return: a boolean that is True of it exists and False if it doesn't
    """
    con = get_connection()
    cur = con.cursor()
    q = """
    SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name = '{}')
    """.format(tname)
    cur.execute(q)
    ret = cur.fetchone()[0]
    con.close()
    return ret

def create_table(tname, fields, primary = None):
    """
    @doc: create a table in the Redshift cluster
    @args: tname is a str of the table name to create
           fields is a dictionary with field name as the key and data type as the value
           primary is the field name to set as the primary key (default: None)
    @return: the SQL string used to create the table
    @note: can use `infer_schema` to generate fields dictionary
    """
    con = get_connection()
    cur = con.cursor()
    f = ""
    
    if isinstance(primary, str):
        primary_key = "{0} {1} PRIMARY KEY".format(primary, fields[primary])
    elif isinstance(primary, list):
        primary_key = "("
        for prim in primary:
            primary_key = primary_key + prim + ", "
        primary_key = "PRIMARY KEY {})".format(primary_key[:-2])
    else:
        primary_key = ""
    
    for key in fields.keys():
        if key != primary:
            f = f + "{0} {1}, ".format(key, fields[key])
    
    f = f + primary_key
    sql = """
    CREATE TABLE {0} (\n{1}\n)
    """.format(tname, f)
    
    cur.execute(sql)
    cur.close()
    con.commit()
    con.close()
    return sql

def drop_table(tname):
    """
    @doc: drop (delete) a table from the Redshift cluster
    @args: tname is a str of the table name to drop
    @return: None
    """
    con = get_connection()
    cur = con.cursor()
    cur.execute("DROP TABLE {}".format(tname))
    cur.close()
    con.commit()
    con.close()
    return

def write_data(tname, bucket, key, delim = "|"):
    """
    @doc: copy data from a CSV stored on S3 into a blank table in Redshift
    @args: tname is a str of the landing table name
           bucket is a str of the bucket where the CSV is stored (e.g. 'cloudframe-bucket' NOT 's3://cloudframe-bucket')
           key is the fully specified location of the CSV file on S3 (e.g. 'directory/location/file.csv')
           delim is a str character to use as the delimiter (defaults to '|')
    @return: the SQL string for the copy operation
    @todo: figure out the case where IAM is already configured for access (no need for access and secret)
    """
    con = get_connection()
    cur = con.cursor()
    usql = """
    COPY {0}
    FROM '{1}'
        access_key_id '{2}'
        secret_access_key '{3}'
    DELIMITER '{4}'
    CSV IGNOREHEADER 1 NULL 'NaN' ACCEPTINVCHARS;
    """.format(tname, "s3://{0}/{1}".format(bucket, key), s3session.access, s3session.secret, delim)
    
    cur.execute(usql)
    con.commit()
    cur.close()
    con.close()
    return usql

def upsert_table(tname, fields, bucket, key, primary = None):
    """
    @doc: update/insert new records into a table in Redshift
    @args: tname is a str for the table name
           fields is a dict with the field name as the key and data type as the value
               (NOTE: fields must match the existing table's schema)
           bucket is a str of the bucket where the CSV is stored (e.g. 'cloudframe-bucket' NOT 's3://cloudframe-bucket')
           key is the fully specified location of the CSV file on S3 (e.g. 'directory/location/file.csv')
           primary is the field to use as the primary key (default is None)
    @return: None
    """
    con = get_connection()
    cur = con.cursor()
    
    if primary is None:
        primary = 'ID'
    
    if table_check(tname + "_staging"):
        drop_table(tname + "_staging")
        
    _ = create_table(tname + "_staging", fields, primary = primary)
    _ = write_data(tname + "_staging", bucket, key)
    
    if isinstance(primary, str):
        primary_where = "WHERE {0}.{1} = {2}.{1}".format(tname,
                                                         primary,
                                                         tname + "_staging")
    elif isinstance(primary, list):
        primary_where = "WHERE "
        for prim in primary:
            primary_where = "{0} {1}.{2} = {3}.{2} AND ".format(primary_where,
                                                                tname,
                                                                prim,
                                                                tname + "_staging",
                                                                prim)
        primary_where = primary_where[:-4]
    
    dsql = """
    DELETE FROM {0}
    USING {1}
    {2};
    """.format(tname, tname + "_staging", primary_where)
    cur.execute(dsql)
    con.commit()
    
    isql = """
    INSERT INTO {0}
    SELECT * FROM {1}
    """.format(tname, tname + "_staging")
    cur.execute(isql)
    con.commit()
    
    cur.close()
    con.close()
    return

def calc_max_len(ser):
    """
    @doc: find the maximum length of a pandas Series of strings (for schema inference)
    @args: ser is a pandas Series of type 'O'
    @return: the maximum length of a string in ser
    """
    retser = ser.apply(lambda x: len(str(x)))
    ret = retser.max()
    return ret

def check_date(ser):
    """
    @doc: do a simple check on object type Series in case they're a date format that we recognize in `DT_FORMAT`
    @args: ser is a pandas Series of type 'O'
    @return a boolean for if a sample of ser meets the `DT_FORMAT` criteria
    """
    sample = ser.sample(10)
    dates = 0
    zeros = 0
    for samp in sample:
        samp = str(samp)
        if samp is None or len(samp) == 0:
            zeros += 1
        elif re.search(DT_FORMAT, samp):
            dates += 1
    if (dates + zeros) == 10 and zeros < 10:
        ret = True
    else:
        ret = False
    return ret

def infer_schema(df):
    """
    @doc: check the columns of a pandas DataFrame and build the simple schema dict
    @args: df is a pandas DataFrame to infer
    @return: a dict of field name -> data type for use in `create_table` and `upsert_table` above.
    """
    cols = df.columns.tolist()
    types = []
    for col in cols:
        typ = df[col].dtype
        
        if np.issubdtype(typ, np.datetime64):
            types.append('DATE')
            print("Check date: {}".format(col))
            
        elif typ == int:
            types.append('INT')
        elif typ == float:
            types.append('FLOAT')
        elif typ == object:
            if check_date(df[col]):
                types.append('DATE')
                print("Check date: {}".format(col))
            else:
                max_len = calc_max_len(df[col])
                if max_len > 150:
                    types.append('VARCHAR({})'.format(4000))
                else:
                    max_len = str(max_len + 64)
                    types.append('VARCHAR({})'.format(max_len))
            
    flds = dict(zip(cols, types))
    return flds

def sql_to_df(sql, verbose = False):
    """
    @doc: query the Redshift cluster and put the results into a pandas DataFrame
    @args: sql is a str of valid PostgreSQL
    @return: a pandas DataFrame
    @note: all column names are UPPER CASE
    """
    con = get_connection()
    cur = con.cursor()
    start = time()
    
    cur.execute(sql)
    end = time()
    emins = round((end - start)/60, 2)
    if verbose:
        print("It has taken {} minutes to execute the query.".format(emins))
    df = pd.DataFrame(cur.fetchall(), columns = [desc[0].upper() for desc in cur.description])
    tmins = round((time() - end)/60, 2)
    if verbose:
        print("It has taken {} minutes to read the results into a DataFrame.".format(tmins))
    con.close()
    return df

def df_to_s3(df, bucket, key, primary = None, filepath = "{}/file.csv".format(hm)):
    """
    @doc: upload a pandas DataFrame to an S3 bucket
    @args: df is a pandas DataFrame to upload
           bucket is a str of the bucket name (e.g. 'cloudframe-test' NOT 's3://cloudframe-test')
           key is a str of the destination path for the file (e.g. 'directory/file.csv')
           primary is a str field name that is in the DataFrame's column space
           filepath is a str of the intermediate write location of the CSV locally
    @return: a tuple of (bucket, key)
    @note: filepath is automatically cleaned up with os.remove()
    """
    if isinstance(primary, str):
        cols = df.columns.tolist()
        cols.remove(primary)
        
        df = df[cols + primary]
        
    df.to_csv(filepath, index = False, sep = "|")
    
    try:
        s3 = boto3.resource('s3')
        s3.meta.client.upload_file(Filename = filepath, Bucket = bucket, Key = key)
    except:
        try:
            s3 = s3session.get_resource()
            s3.meta.client.upload_file(Filename = filepath, Bucket = bucket, Key = key)
        except:
            print("Could not upload {}".format(filepath))
        
    os.remove(filepath)
    return bucket, key

def get_tables(public = False):
    """
    @doc: get the table names of the Redshift cluster
    @args: public is a boolean for whether or not to filter on just the public tables
    @return: a list of str table names
    """
    add = ""
    if public:
        add = " where schemaname = 'public'"
    df = sql_to_df("select * from pg_table_def{}".format(add))
    tbls = df.TABLENAME.unique().tolist()
    return tbls