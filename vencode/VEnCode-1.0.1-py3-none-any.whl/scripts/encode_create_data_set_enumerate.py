import os
import glob

import pandas as pd
import re
from tqdm import tqdm

from VEnCode.utils import pandas_utils as pd_util
from VEnCode.utils import general_utils as gen_util
from VEnCode import common_variables as cv


def index_cleaner_enhancers(data):
    data["Id"] = data.index
    data[["Chromosome", "temp"]] = data.Id.str.split(":", expand=True)
    data[["Start", "End"]] = data.temp.str.split("-", expand=True)
    data = data[["Chromosome", "Start", "End"]]
    pd_util.columns_to_numeric(data, "Start", "End")
    data["range"] = [[dt["Start"], dt["End"]] for ids, dt in data.iterrows()]
    return data


def index_cleaner_promoters(data):
    data["Id"] = data.index
    data[["Chromosome", "temp"]] = data.Id.str.split(":", expand=True)
    data[["Start", "ignore", "End_pre"]] = data.temp.str.split(".", expand=True)
    data[["End", "ignore2"]] = data.End_pre.str.split(",", expand=True)
    data = data[["Chromosome", "Start", "End"]]
    pd_util.columns_to_numeric(data, "Start", "End")
    data["range"] = [[dt["Start"], dt["End"]] for ids, dt in data.iterrows()]
    return data


def cell_type_name(name, i=1):
    if i == 1:
        name_new = "{}_{}".format(name, i)
    else:
        name_new = name[:-2]
        name_new = "{}_{}".format(name_new, i)
    if name_new in encode_derived_data.columns:
        i += 1
        name_new = cell_type_name(name_new, i=i)
        return name_new
    else:
        return name_new


DATA_TYPE = "promoters"

DATA_FANTOM_PATH = "D:/Utilizador HDD/OneDrive - Nova Medical School Faculdade de Ciências Médicas da " \
                   "UNL/1-Research/3-Vencode/Fantom5/Files/"

if DATA_TYPE == "enhancers":
    FILE_NAME_ENHANCER = cv.test_enhancer_file_name
    FILE_PATH = os.path.join(DATA_FANTOM_PATH, FILE_NAME_ENHANCER)
    data_fantom = pd.read_csv(FILE_PATH, sep="\t", index_col=0, engine="python", skiprows=None)
    fantom_coord = index_cleaner_enhancers(data_fantom)

elif DATA_TYPE == "promoters":
    FILE_NAME_PROMOTER = cv.promoter_file_name
    FILE_PATH = os.path.join(DATA_FANTOM_PATH, FILE_NAME_PROMOTER)
    data_fantom = pd.read_csv(FILE_PATH, sep="\t", index_col=0, engine="python", skiprows=1831)
    data_fantom.drop(data_fantom.index[:2], inplace=True)
    print("Finished opening fantom5 file")
    fantom_coord = index_cleaner_promoters(data_fantom)

else:
    raise Exception("Wrong data_type")

encode_derived_data = pd.DataFrame(index=data_fantom.index)
data_fantom = 1

METADATA_PATH = "D:/Utilizador HDD/OneDrive - Nova Medical School Faculdade de Ciências Médicas da " \
                "UNL/1-Research/3-Vencode/Fantom5/Files/Validation_files/ENCODE/Metadata_curated.csv"

metadata = pd.read_csv(METADATA_PATH, sep="\t", engine="python")

ENCODE_DATA_PATH = "D:/Utilizador HDD/OneDrive - Nova Medical School Faculdade de Ciências Médicas da " \
                   "UNL/1-Research/3-Vencode/Fantom5/Files/Validation_files/ENCODE/Data/"

for filename in tqdm(glob.glob(os.path.join(ENCODE_DATA_PATH, '*.bed'))):
    file_data = pd.read_csv(filename, sep="\t", engine="python", usecols=range(0, 3),
                            names=["Chromosome", "Start", "End"])
    file_data['Start'] = file_data.apply(lambda row: row["Start"] - 200, axis=1)
    file_data['End'] = file_data.apply(lambda row: row["End"] + 200, axis=1)

    experiment = re.search(r"\\(ENCS.*?)_(rep.)_", filename)
    experiment_accession = experiment.group(1)
    try:
        cell_type = metadata[metadata["Experiment accession"] == experiment_accession]["Biosample term name"].values[0]
    except IndexError:
        print(" File /n {} /n not included because it is not in metadata".format(filename))
        continue

    data_matches = pd.Series(index=fantom_coord.index)
    for index, col in fantom_coord.iterrows():
        range1 = col["range"]
        data_filtered_chr = file_data[file_data["Chromosome"] == col.Chromosome]

        end2 = data_filtered_chr["End"].values
        start2 = data_filtered_chr["Start"].values
        for idx, val in enumerate(end2):
            if val >= range1[0]:
                if range1[1] >= start2[idx]:
                    data_matches[index] = 1
                else:
                    data_matches[index] = 0
                break
            else:
                continue

    if cell_type in encode_derived_data.columns:
        cell_type = cell_type_name(cell_type)
    encode_derived_data[cell_type] = data_matches

path_out = "D:/Utilizador HDD/OneDrive - Nova Medical School Faculdade de Ciências Médicas da " \
           "UNL/1-Research/3-Vencode/Fantom5/Files/Validation_files/ENCODE/"
filename = "ENCODE DNase expression in FANTOM5 {}_200bp.csv".format(DATA_TYPE)
path_out = os.path.join(path_out, filename)

encode_derived_data.to_csv(path_out, sep=";")
