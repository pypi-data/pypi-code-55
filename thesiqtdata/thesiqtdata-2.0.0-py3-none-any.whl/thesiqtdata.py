import pandas as pd
import glob
import os
import pickle
def __get_full_path_files(path, _list_files):
    """a function re get full path file in a folder"""
    for x in os.walk(path):
        for y in glob.glob(os.path.join(x[0], '*.xls')):
            _list_files.append(y)
    for x in os.walk(path):
        for y in glob.glob(os.path.join(x[0], '*.xlsx')):
            _list_files.append(y)
def __get_field(path):
    field = os.path.basename(path) 
    return field
def __get_city(path):
    city = os.path.basename(os.path.dirname(path))
    return city
def __add_header_field_city(all_dfs,field, city):
    all_dfs['field'] = field
    all_dfs['city'] = city      
def __bonus_header_filename(all_dfs, filename, full_name = False):
    #all_dfs['filename'] = os.path.basename(filename)
    if full_name==False:
        all_dfs['filename'] = os.path.basename(filename)
    else:
        all_dfs['filename'] = filename
def __set_header(dataframe, list_header):
    """set header of a dataframe follow up list_header"""
    if dataframe.empty:
        return dataframe
    while dataframe.columns.tolist()!=list_header:
        if dataframe.empty: return dataframe
        dataframe.columns = dataframe.iloc[0]
        dataframe = dataframe.drop(0)
        dataframe = dataframe.reset_index(drop = True)
    return dataframe   
def __write_to_file(data_to_write, file_to_write):
    try:
        with open(file_to_write, 'wb') as data_file:
            pickle.dump(data_to_write, data_file)
    except IOError as err:
        print(str(err))
    except pickle.PickleError as pickle_err:
        print(str(pickle_err))
def __set_unwanted_sheet(file_name, sheet_name, list_unwanted_sheet):
    """list of sheets that dont have header as list_header"""
    list_unwanted_sheet.append(file_name + ':' + sheet_name)
def __set_list_dataframe(list_dataframe, file_name, list_header, list_unwanted_sheet):
    xl = pd.ExcelFile(file_name)
    for sheet in xl.sheet_names:
        df = xl.parse(sheet_name=sheet)
        df = __set_header(df, list_header)
        if df.empty:
            list_unwanted_sheet.append(file_name + ':' + sheet)
        else:
            list_dataframe.append(df)
        __bonus_header_filename(df, file_name, full_name=True)
haeder_list=['user_personal_id_type', 'user_personal_id', 'user_phone_type', 'user_phone_number', 
            'username', 'email', 'event_category', 'sub_event_category', 'event_at', 'event_from', 
            'event_to', 'event_description', 'event_location', 'apartment_number', 'apartment_name', 
            'house_type', 'house_address', 'live_here', 'is_owner']
def __main_function(path, unwanted_file_to_write, result_file):
    list_files = []
    __get_full_path_files(path, list_files)
    combined_dfs = pd.DataFrame()
    dfs = []
    list_unwanted_sheet=[]
    for _file in list_files:
        __set_list_dataframe(dfs, _file, haeder_list, list_unwanted_sheet)
    combined_dfs = pd.concat(dfs, ignore_index=True)
    field =__get_field(path)
    city = __get_city(path)
    __add_header_field_city(combined_dfs, field, city)
    combined_dfs.to_excel(result_file,index=False, engine='xlsxwriter')
    __write_to_file(list_unwanted_sheet, unwanted_file_to_write)
