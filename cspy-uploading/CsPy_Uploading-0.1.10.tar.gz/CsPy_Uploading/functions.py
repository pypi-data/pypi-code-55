import pandas as pd
import numpy as np
import datetime as dt
import os as os
import openpyxl as xl
import pyodbc as odbc
import humanfriendly as hf
import platform as pl
import win32com.client as win32
import sys
from google.cloud.bigquery import Client, LoadJobConfig, DatasetReference
from google.cloud.bigquery import SchemaField as sf
from google.oauth2 import service_account

# TODO: Add better error exceptions
# TODO: Add full function descriptions
# TODO: Delete Big Query Tables Function


def read_query_from_file(file_path):
    with open(file_path, 'r') as text:
        query = text.read()
        text.close()
    return query


def left(s, amount):
    return s[:amount]


def right(s, amount):
    return s[-amount:]


def mid(s, offset, amount):
    return s[offset:offset+amount]


def insert_line():
    print('===================================================================================================')


def thg_log():
    print("""
--=================================================================================================--                                                                                                                                                                                                  
     @&&&&&&&&&&&&&&&&&&&&&&&       &&&&&&&%           &&&&&&&.              &&&&&&&&&&&@&&.        
     &&&&&&&&&&&&&&&&&&&&&&&&       &&&&&&&%           &&&&&&&.          @@&&&&&&&&&&&&&&&&&&&&/    
     ,.......&&&&&&&&........       &&&&&&&%           &&&&&&&.        @&&&&&&&&&&/..*&&&&&&&@      
             &&&&&&&@               &&&&&&&%           &&&&&&&.      ,&&&&&&&@             @        
             &&&&&&&@               &&&&&&&%           &&&&&&&.      &&&&&&&&                       
             &&&&&&&@               &&&&&&&&&&&&&&&&&&&&&&&&&&.     .&&&&&&&             ,,,,,,.    
             &&&&&&&@               &&&&&&&&&&&&&&&&&&&&&&&&&&.      &&&&&&&.            &&&&&&*    
             &&&&&&&@               &&&&&&&%           &&&&&&&.      @&&&&&&@/           &&&&&&*    
             &&&&&&&@               &&&&&&&%           &&&&&&&.       &&&&&&&&&@        /@&&&&&*    
             &&&&&&&@               &&&&&&&%           &&&&&&&.         &&&&&&&&&&&&&&&&&&&&&&&*    
             &&&&&&&@               &&&&&&&%           &&&&&&&.            &&&&&&&&&&&&&&&&@&.       
--=================================================================================================--
    """)


def log(string):
    """
    INTERNAL FUNCTION
    """
    print(dt.datetime.now(), ': ', string)


def copy_excel(source, destination):
    """
    FUNCTION: copy_excel
        DESC: Copys a excel workbook to another location.
        EXAMPLE: copy_excel("C:Documents/file.xslx", "C:Documents/new_file.xslx")

    PARAM(STRING): source
        DESC: File path of excel document ou wish to copy.
        EXAMPLE: "C:Documents/file.xslx"

    PARAM(STRING): destination
        DESC: File path you wish to copy the excel workbook to.
        EXAMPLE: "C:Documents/new_file.xslx"
    """
    wb1 = xl.load_workbook(source, data_only=True)
    wb1.save(str(destination))


def save_excel_sheets_to_csv(xls_path, save_path, sheet_names=None):
    """
    FUNCTION: save_excel_sheets_to_csv
        DESC: Converts a xlsx file into csv files of each sheet.
        EXAMPLE: save_excel_sheet_to_csv("C:Documents/file.xslx", "C:Documents/{}.csv", sheet_names=['sheet1','sheet3'])

    PARAM(STRING): xls_path
        DESC: File path of the excel workbook you wish to split out.
        EXAMPLE: "C:Documents/file.xslx"

    PARAM(STRING): save_path
        DESC: Folder location that you wish to save the csv files to.
        EXAMPLE: "C:Documents/{}.csv"

    OPTIONAL(LIST): sheet_names
        DESC: Use if you only need specific sheets.
        EXAMPLE: ['sheet1','sheet3']
    """
    log('Loading {} into pandas.'.format(xls_path))
    wb = pd.ExcelFile(xls_path)
    for idx, name in enumerate(wb.sheet_names):
        if sheet_names is not None:
            if name in sheet_names:
                log('Reading sheet #{0}: {1}'.format(idx, name))
                sheet = wb.parse(name)
                sheet.to_csv(save_path.format(name), index=False)

        elif sheet_names is None:
            log('Reading sheet #{0}: {1}'.format(idx, name))
            sheet = wb.parse(name)
            sheet.to_csv(save_path.format(name), index=False)


def delete_folder_contents(directory):
    """
    FUNCTION: delete_folder_contents
        DESC: Deletes every file from input folder location.
        EXAMPLE: delete_folder_contents("C:Documents/folder/")

    PARAM(STRING): directory
        DESC: Folder Path that you wish to delete the contents of.
        EXAMPLE: "C:Documents/folder/"
    """
    log('Deleting files from: {}'.format(directory))
    for file in os.listdir(directory):
        log('Deleteing: {}'.format(file))
        os.unlink(directory + file)


def date_convert(data_frame, schema):
    """
    FUNCTION: date_convert
        DESC: Converts each date column in a dataframe to datekeys
        EXAMPLE: date_convert(pd.dataframe(), schema)

    PARAM(PANDAS DATAFRAME): data_frame
        DESC: Data Frame you wish to convert
        EXAMPLE: pd.dataframe()

    PARAM(ARRAY): schmea
        EXAMPLE: schema = [sf(name="Locale", field_type="STRING", mode="NULLABLE"),
                           sf(name="Revenue", field_type="FLOAT", mode="NULLABLE"),
                           sf(name="Order_Date", field_type="DATE", mode="NULLABLE")]
        NOTE: Column names and data types of dataframe having date columns labeled 'DATE' or 'DATETIME'

    """
    convert_columns = []
    new_schema = []
    for i in schema:
        if i.field_type in ('DATETIME', 'DATE'):
            convert_columns.append(i.name)

    if len(convert_columns) != 0:
        log('Date columns to be converted to keys: '.format(str(convert_columns)))

    for i in convert_columns:
        try:
            log('Converting date column '.format(i))
            data_frame[i] = pd.to_datetime(data_frame[i])
            data_frame[i] = data_frame[i].fillna(dt.datetime(1990, 1, 1))
            data_frame[i] = data_frame[i].dt.strftime('%Y%m%d').astype(int)
            data_frame[i] = data_frame[i].replace(19900101, np.nan)
        except Exception as e:
            log('Failed to convert {} column to a date.'.format(i))
            log('Error: {}'.format(e))

    for i in schema:
        if i.name in convert_columns:
            x = sf(name=i.name, field_type='INTEGER', mode=i.mode)
            new_schema.append(x)
        else:
            new_schema.append(i)

    return data_frame, new_schema


def sql_to_workbook(query, dsn, save_path_file, num_tables, sheet_names=None):
    # TODO: finish this function using temp query and select queries
    """
    WORK IN PROGRESS
    """
    print('Reading Sql Query using {0} connection.'.format(dsn))
    connection = odbc.connect(dsn)
    for i in range(0, num_tables):
        print()