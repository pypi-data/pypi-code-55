import re
from collections import defaultdict

import numpy as np
import pandas as pd
from tqdm import tqdm

DATA_TYPE = "enhancers"
encode_data_path = "D:/Utilizador HDD/OneDrive - Nova Medical School Faculdade de Ciências Médicas da UNL/" \
                   "1-Research/3-Vencode/Fantom5/Files/Validation_files/ENCODE/" \
                   "ENCODE DNase expression in FANTOM5 {}_200bp.csv".format(DATA_TYPE)
encode_data = pd.read_csv(encode_data_path, sep=";", engine="python", index_col=0)

cols = defaultdict(list)
reg_pattern = r"([^_]*)_(_|[0-9]{1,2})"
for bio_rep in encode_data.columns:
    search = re.search(reg_pattern, bio_rep)
    if search is None:
        cols[bio_rep].append(bio_rep)
    else:
        cell_type = search.group(1)
        cols[cell_type].append(bio_rep)

new_df = pd.DataFrame(index=encode_data.index.values, columns=[key for key in cols.keys()])

for cell_type, bio_rep in tqdm(cols.items()):
    celltypes_averaged = encode_data[bio_rep].apply(np.mean, axis=1)
    new_df[cell_type] = celltypes_averaged
new_df = new_df.apply(lambda x: [1 if y > 0 else 0 for y in x], axis=0)
new_df.to_csv("ENCODE DNase expression in FANTOM5 {}_200bp_merged.csv".format(DATA_TYPE), sep=";")
