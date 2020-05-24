import pandas as pd
from matplotlib import pyplot as plt, transforms
import matplotlib.ticker as ticker
import matplotlib.ticker as mtick
import numpy as np
from os.path import dirname, basename, join, abspath, exists
import csv
import glob
from os import listdir
from matplotlib import pyplot as plt
from shutil import copy

def get_index_of_topvalue(df, row_name='PSNR', asc=True):
    """

    :param df:
    :param row_name:
    :param asc: Boolean. Default is True. Gets the index with maximum values, otherwise, with minim value.
    :return: name of column (str)
    """

    # file = join(working_folder, file_pre_name + region + "_" + region + file_rest_name)
    if asc:
        res =  df.idxmax(axis=1)
    else:
        res =  df.idxmin(axis=1)
    return res.loc[row_name]

def get_biggest_col_num(df):
    """
    Finds the biggest number in columns of a dataframe
    :param df: Pandas data frame
    :return: Returns the biggest number
    """
    biggest_num = 0

    num_zfill = np.int(np.ceil(np.log10(df.columns.__len__())))

    for i in range(0, df.columns.__len__()):

        name = df.columns[i]
        prefix, num = name.split('.')
        num = int(num)
        if num > biggest_num:
            biggest_num = num

    return biggest_num

def enumerate_columns(df, sort_index=False, num_zfill=3, inplace=False):

    num_zfill = np.int(np.ceil(np.log10(get_biggest_col_num(df))))

    for i in range(0, df.columns.__len__()):

        name = df.columns[i]
        prefix, num = name.split('.')
        str_num = str(num).zfill(num_zfill)
        new_name = prefix + '.' + str_num
        df.rename(columns={name:new_name}, inplace=True)

    if sort_index:
        df.sort_index(axis=1, inplace=inplace)

    return df

def get_log(log_file):

    training_log = []

    if exists(log_file):

        with open(log_file) as log:
            csv_reader = csv.reader(log, delimiter=',')

            # print('log file: ', log)
            for row in csv_reader:
                training_log.append(row[1])

            training_log[1:] = [float(x) for x in training_log[1:]]

    else:
        print("Log file, " , log_file , " can not be found!")

    return training_log

def collect_logs():

    df = pd.DataFrame(columns=index_columns + test_sets)
    df.set_index(index_columns, inplace=True)
    df_all = df.copy()
    df_logs = pd.DataFrame(index=training_sets, columns=list(range(1, 101)))

    for dataset in training_sets:
        working_folder = join(abspath(root_folder), file_pre_name + dataset)
        working_folder = join(working_folder, sub_path)

        tmp_df = df.copy()

        # log_file = join(working_folder, region + ".training_tf.log")
        log_file = join(working_folder, "training_tf.log")
        training_log = get_log(log_file)
        df_logs.loc[dataset]= training_log[1:]

    return df_logs

def get_top_ncolumns(df, row_by, in_top=10, asc=True):
    """
    Returns the columns having n number of largest or smallest values in a given row
    :param df: Pandas DataFrame
    :param row_by: The row in which the values are sought
    :param in_top: Number of top values
    :param asc: Bool. Defaul is True, which means Largest (since ascending order), Smallest otherwise.
    :return: Returns the Pandas DataFrame with top n columns
    """

    d = df.transpose()

    if asc:
        d= d.nlargest(in_top, row_by)
    else:
        d= d.nsmallest(in_top, row_by)

    return df[d.index.to_list()]

def get_best_epoch(df, index_name, row_by=None, in_top=1, asc_by_index=True, asc_by_row=False):
    """
    Returns the column header of a Pandas DataFrame. The header belongs to corresponding best epoch.
    It is possible to search the best epoch within a certain number of columns constrained by a parameter (row_by).
    'row_by' parameter designates the name of constraint row (index name of a DataFrame's row). This mechanism
    offers a neat way to find the best epoch at which the Deep Network is not over fitting, by searching the best
    epoch within a number of epochs having the one of minimum training loss.

    :param df: Pandas DataFrame from which the column name of the best epoch to be extracted.
    :param index_name: The name of the row (index) in which best value is being sought.
    :param row_by: String. The name of constraint row (another row in the DataFrame). If 'row_by' paraameter is not given
    the top value (minimum or maximum, depending on 'asc_by_index') is searched in index row without applying any
    constrain.
    :param in_top: The number of top values (top values can be minimum or maximum based on asc_by_row
    :param asc_by_index: Boolean. Indicates if largest or smallest values to be sought in index row (row with name 'PSNR' for example).
    :param asc_by_row:  Boolean. Indicates if largest or smallest values to be sought in constraint row.
    :return: Returns the column's header (index) containing the best value.
    """

    if row_by is not None:
        df = get_top_ncolumns(df, row_by=row_by, in_top=in_top, asc=asc_by_row)

    idx = get_index_of_topvalue(df,index_name, asc=asc_by_index)

    return idx

def best_epochs(excel_file, sheet_name, cols=None, nrows=None, log_file=None, in_top=1, metric='PSNR'):
    """
    Returns the best epoch's name and index based on PSNR value

    :param excel_file:
    :param sheet_name:
    :param cols:
    :param nrows:
    :return: Returns index name and index position
    """

    row_by=None

    xl = pd.read_excel(excel_file, usecols=cols, sheet_name=sheet_name, nrows=nrows)
    xl.set_index(xl.columns[0], inplace=True)

    org_cols = xl.columns
    x = enumerate_columns(xl)
    new_cols = x.columns
    x.sort_index(axis=1, inplace=True)

    dic = dict(zip(new_cols, org_cols))

    if log_file:
        log = get_log(log_file)

        if not np.isnan(np.sum(log[1:])):
            x.loc[log[0]] = log[1:]
            row_by = 'loss'
        else:
            print('Warning: Log file {} has nan values. Log is not used for constraint! \
                  Best value will straightforwardly be taken from index!'.format(log_file))


    i = get_best_epoch(x, metric, row_by=row_by, in_top=in_top,  asc_by_index=True, asc_by_row=False)


    return dic[i]

def collect_best_epochs(folder, log_file=r"training_tf.log", scale='2', metric='PSNR'):

    model_names= listdir(folder)
    epochs = dict()

    for model in model_names:

        model_path = join(folder, model, 'output', scale)
        log = join(model_path, log_file)

        excel_file = glob.glob(join(model_path, '*.xlsx'))

        if len(excel_file) == 1:
            epoch = best_epochs(excel_file[0], sheet_name='Mean', log_file=log, in_top=1 )

            epochs[model] = epoch

    with open(join(folder, 'best epochs by ' + metric + '.txt'), 'w') as f:
        for key in epochs.keys():
            f.write("%s,%s\n"%(key,epochs[key]))

        for key in epochs.keys():
            old_file = join(folder, key+ '/output/'+ scale + '/' + epochs[key] + '.h5')
            new_file = join(folder, key + '.h5')

            copy(old_file, new_file)


folder = r"D:\calismalarim\projeler\Activations on SR\Results"

sheet_name = 'Mean'

if __name__ == "__main__":
    import sys

    if len(sys.argv) >1:
        folder = sys.argv[0]

    collect_best_epochs(folder,)







