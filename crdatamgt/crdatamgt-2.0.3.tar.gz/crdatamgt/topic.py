from collections import defaultdict
from crdatamgt.helpers import workbook_load_path, data_extraction, rename_dictionary
import pandas as pd

def load_topic(path):
    print(path)
    wb = workbook_load_path(path)
    return wb


def read_topic(wb, formulation_path):
    df_dictionary = defaultdict()
    for sheet in wb.sheetnames:
        df_dictionary[sheet] = data_extraction(wb, sheet)
    if 'Results' in df_dictionary.keys():
        column_names = df_dictionary['Results'].columns.values
        if 'Replicate' in column_names or 'Replicate #' in column_names:
            df_dictionary['Results'].rename(columns={'Replicate #': 'Replicate'}, inplace=True)
            df_dictionary['Results'] = pd.DataFrame(
                df_dictionary['Results'].set_index('Replicate').mean().round(2)).transpose().add_suffix(' Average')

    return df_dictionary


def formulation_group(formulas):
    temp_formulation_group = []
    result = formulas.drop(columns='Formulation').mean().round(0)
    fc = pd.DataFrame(result[result > 5]).transpose()
    fc.columns = map(str.lower, fc.columns)
    fc.rename(columns=rename_dictionary(), inplace=True)
    for item in fc:
        temp_formulation_group.append(f"{item} {fc[item].values[0]}")
    fg = ' '.join(temp_formulation_group)
    return pd.DataFrame(columns=['Formulation Group'], data=[fg])

