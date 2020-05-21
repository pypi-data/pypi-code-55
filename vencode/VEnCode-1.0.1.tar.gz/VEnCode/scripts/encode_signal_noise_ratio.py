
import os

import numpy as np
import pandas as pd

DATA_TYPE = "enhancers"

path = "D:/Utilizador HDD/" \
       "OneDrive - Nova Medical School Faculdade de Ciências Médicas da UNL/" \
       "1-Research/3-Vencode/Fantom5/Files/Validation_files/ENCODE/"


data_file_name = "CAGE VEn in ENCODE DNase matrix {}_validated-normalized.csv".format(DATA_TYPE)
data_matrix = pd.read_csv(os.path.join(path, data_file_name), sep=";", engine="python", index_col=0)

random_file_name = "CAGE VEn in ENCODE DNase matrix {}_validated_realrandom-normalized.csv".format(DATA_TYPE)
random_data = pd.read_csv(os.path.join(path, random_file_name), sep=";", engine="python", index_col=0)

data_subtracted = data_matrix.subtract(random_data)
data_subtracted.dropna(axis=0, inplace=True)
output_path = os.path.join(path, "signal_noise_subtraction_matrix_{}_validated.csv".format(DATA_TYPE))
data_subtracted.to_csv(output_path, sep=";")

# data_ratio = data_matrix.divide(random_data.loc[data_matrix.index], fill_value=0)
# data_ratio.replace([np.inf, -np.inf], np.nan, inplace=True)
# data_ratio.fillna(0, inplace=True)
# output_path = os.path.join(path, "signal_noise_ratio_matrix_{}.csv".format(DATA_TYPE))
# data_ratio.to_csv(output_path, sep=";")
