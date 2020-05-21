import os
import glob
import re

import pandas as pd
from tqdm import tqdm

from VEnCode import internals_extensions as iext
from VEnCode.utils import validation_utils as val_util
from VEnCode.utils import pandas_utils as pd_util
from VEnCode.utils import general_utils as gen_util


class Settings:
    CELL_TYPE = "Iris Pigment Epithelial Cells"
    TYPE = "primary cells"
    DATA_TYPE = "promoters"
    ALGORITHM = "sampling"
    K = 4
    NUMBER_VENCODES_TO_GET = 50

    PATH_OUT_VEN = "D:/Utilizador HDD/OneDrive - Nova Medical School Faculdade de Ciências Médicas da UNL/1-Research/" \
                   "3-Vencode/Fantom5/VEnCodes/A549 200 vencodes - heu"

    # Next ones you may not need to change:
    NON_TARGET_CELLTYPES_INACTIVITY = 0
    if DATA_TYPE == "enhancers":
        TARGET_CELLTYPE_ACTIVITY = 0.1
    elif DATA_TYPE == "promoters":
        TARGET_CELLTYPE_ACTIVITY = 0.5
    else:
        raise AttributeError("data_type - {} - currently not supported".format(DATA_TYPE))
    if ALGORITHM == "heuristic":
        REG_ELEMENT_SPARSENESS = 0
    elif ALGORITHM == "sampling":
        REG_ELEMENT_SPARSENESS = 90  # For some, you probably have to reduce sparseness to 0.
    else:
        raise AttributeError("Algorithm - {} - currently not supported".format(ALGORITHM))


class EncodeValidateVencodes:
    def __init__(self, settings):
        self.set_up = settings
        thresholds = (
            settings.NON_TARGET_CELLTYPES_INACTIVITY, settings.TARGET_CELLTYPE_ACTIVITY,
            settings.REG_ELEMENT_SPARSENESS)

        self.vencodes_object = iext.GetVencode(cell_type=settings.CELL_TYPE,
                                               data_type=settings.DATA_TYPE, algorithm=settings.ALGORITHM,
                                               n_regulatory_elements=settings.K,
                                               number_vencodes=settings.NUMBER_VENCODES_TO_GET,
                                               parsed=val_util.status_parsed(settings.CELL_TYPE),
                                               thresholds=thresholds, n_samples=10000, sample_type=settings.TYPE,
                                               files_path="outside")
        self.vencodes_data = self.vencodes_object.vencodes.get_vencode_data(method="return")

    def validate(self):
        encode_derived_data = pd.DataFrame(index=[self.vencodes_object.cell_type])

        METADATA_PATH = "D:/Utilizador HDD/OneDrive - Nova Medical School Faculdade de Ciências Médicas da " \
                        "UNL/1-Research/3-Vencode/Fantom5/Files/Validation_files/ENCODE/Metadata_curated.csv"

        metadata = pd.read_csv(METADATA_PATH, sep="\t", engine="python")

        ENCODE_DATA_PATH = "D:/Utilizador HDD/OneDrive - Nova Medical School Faculdade de Ciências Médicas da " \
                           "UNL/1-Research/3-Vencode/Fantom5/Files/Validation_files/ENCODE/Data/"

        for filename in tqdm(glob.glob(os.path.join(ENCODE_DATA_PATH, '*.bed'))):
            file_data = pd.read_csv(filename, sep="\t", engine="python", usecols=range(0, 3),
                                    names=["Chromosome", "Start", "End"])
            file_data['range'] = file_data.apply(lambda row: [row["Start"], row["End"]], axis=1)
            experiment = re.search(r"\\(ENCS.*?)_(rep.)_", filename)
            experiment_accession = experiment.group(1)
            try:
                cell_type = \
                    metadata[metadata["Experiment accession"] == experiment_accession]["Biosample term name"].values[0]
            except IndexError:
                print(" File /n {} /n not included because it is not in metadata".format(filename))
                continue

            is_expressed = []
            for vencode in self.vencodes_data:
                vencode = self._index_cleaner_promoters(vencode)
                data_matches = pd.Series(index=vencode.index)
                for index, col in vencode.iterrows():
                    range1 = col["range"]
                    data_filtered_chr = file_data[file_data["Chromosome"] == col.Chromosome]
                    range2_list = data_filtered_chr["range"].tolist()
                    status = False
                    for range2 in range2_list:
                        condition = gen_util.partial_subset_of_span(range1, range2)
                        if condition:
                            status = True
                            break
                        else:
                            continue
                    if status:
                        data_matches[index] = 1
                    else:
                        data_matches[index] = 0
                if data_matches.all():
                    is_expressed.append(1)
                else:
                    is_expressed.append(0)

            if cell_type in encode_derived_data.columns:
                cell_type = self._cell_type_name(cell_type, encode_derived_data)
            encode_derived_data[cell_type] = sum(is_expressed)
        encode_derived_data.to_csv("FANTOM5 VEnCodes expression in ENCODE Dnase-seq data.csv", sep=";")
        return encode_derived_data

    def get_matrix(self):
        encode_data_path = """\
        D:/Utilizador HDD/OneDrive - Nova Medical School Faculdade de Ciências Médicas da UNL/1-Research/3-Vencode/\
        Fantom5/Files/Validation_files/ENCODE/ENCODE DNase expression in FANTOM5 {}.csv""".format(self.set_up.DATA_TYPE)

        file_data = pd.read_csv(encode_data_path, sep=";", engine="python", index_col=0)

    def _cell_type_name(self, name, data, i=1):
        if i == 1:
            name_new = "{}_{}".format(name, i)
        else:
            name_new = name[:-2]
            name_new = "{}_{}".format(name_new, i)
        if name_new in data.columns:
            i += 1
            name_new = self._cell_type_name(name_new, data, i=i)
            return name_new
        else:
            return name_new

    @staticmethod
    def _index_cleaner_promoters(data):
        data["Id"] = data.index
        data[["Chromosome", "temp"]] = data.Id.str.split(":", expand=True)
        data[["Start", "ignore", "End_pre"]] = data.temp.str.split(".", expand=True)
        data[["End", "ignore2"]] = data.End_pre.str.split(",", expand=True)
        data = data[["Chromosome", "Start", "End"]]
        pd_util.columns_to_numeric(data, "Start", "End")
        data["range"] = [[dt["Start"], dt["End"]] for ids, dt in data.iterrows()]
        return data


if __name__ == "__main__":
    _settings = Settings()
    ven = EncodeValidateVencodes(_settings)
    validate = ven.validate()

