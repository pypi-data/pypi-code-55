import os
import re
import glob

import pandas as pd
from tqdm import tqdm
import numpy as np

from VEnCode import internals
from VEnCode import common_variables as cv
from VEnCode import internals_extensions as iext
from VEnCode.utils import validation_utils as val_util
from VEnCode.utils import exceptions
from VEnCode.scripts import encode_vencode_val_variables as val_var


class Settings:
    TYPE = "primary cells"
    DATA_TYPE = "promoters"
    ALGORITHM = "sampling"
    K = 4
    NUMBER_VENCODES_TO_GET = 500

    if DATA_TYPE == "promoters":
        CELL_TYPES = val_var.index_promoter_active
    elif DATA_TYPE == "enhancers":
        CELL_TYPES = val_var.index_enhancer_active
    else:
        CELL_TYPES = "MODIFY"

    PATH_OUT_VEN = "D:/Utilizador HDD/OneDrive - Nova Medical School Faculdade de Ciências Médicas da UNL/1-Research/" \
                   "3-Vencode/Fantom5/Files/Validation_files/ENCODE/"

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
    """
    Retrieves VEnCodes in FANTOM5 data and then Validates them using ENCODE data. Output is a matrix of number of
    VEnCodes for each FANTOM5 celltype that is fully active in each ENCODE cell type.
    """

    def __init__(self, settings, merged=True, data_path=None, random_assay=False, real_random=False):
        self.settings = settings
        self.random_assay = random_assay
        self.real_random = real_random
        if data_path is not None:
            encode_data_path = data_path
        else:
            if merged:
                encode_data_path = "D:/Utilizador HDD/" \
                                   "OneDrive - Nova Medical School Faculdade de Ciências Médicas da UNL/" \
                                   "1-Research/3-Vencode/Fantom5/Files/Validation_files/ENCODE/" \
                                   "ENCODE DNase expression in FANTOM5 {}_merged.csv".format(self.settings.DATA_TYPE)
            else:
                encode_data_path = "D:/Utilizador HDD/" \
                                   "OneDrive - Nova Medical School Faculdade de Ciências Médicas da UNL/" \
                                   "1-Research/3-Vencode/Fantom5/Files/Validation_files/ENCODE/" \
                                   "ENCODE DNase expression in FANTOM5 {}.csv".format(self.settings.DATA_TYPE)

        self.encode_data = pd.read_csv(encode_data_path, sep=";", engine="python", index_col=0)
        self.matrix = pd.DataFrame(columns=self.encode_data.columns)
        self.vencode_numbers = pd.Series()

    def validate(self):
        for cell_type in tqdm(self.settings.CELL_TYPES):
            thresholds = [self.settings.NON_TARGET_CELLTYPES_INACTIVITY, self.settings.TARGET_CELLTYPE_ACTIVITY,
                          self.settings.REG_ELEMENT_SPARSENESS]
            if self.random_assay:
                vencodes_data = self._get_random_combinations(self._get_data_filtered(cell_type, thresholds,
                                                                                      files_path="outside"))
                self.vencode_numbers[cell_type] = 500
            else:
                ctn = False
                while True:
                    try:
                        vencodes_object = self._search_vencodes_full(cell_type=cell_type,
                                                                     thresholds=thresholds,
                                                                     files_path="outside")
                        break
                    except exceptions.NoVencodeError:
                        thresholds[2] -= 5
                        if thresholds[2] < 0:
                            vencodes_object = None
                            print("Warning: no VEnCodes found for {}".format(cell_type))
                            ctn = True
                            break
                if ctn:
                    continue
                vencodes_data = vencodes_object.vencodes.get_vencode_data(method="return")
                self.vencode_numbers[cell_type] = len(vencodes_object.vencodes.vencodes)
            self.matrix.loc[cell_type] = self._vencode_in_encode(vencodes_data)

    def validate_active(self, delete=None):
        if self.settings.DATA_TYPE == "promoters":
            encode_cells = val_var.columns_promoter_active
        else:
            encode_cells = val_var.columns_enhancer_active
        if delete:
            delete.sort(reverse=True)
            for index in delete:
                del self.settings.CELL_TYPES[index]
                del encode_cells[index]
        cell_type_dict = dict(zip(self.settings.CELL_TYPES, encode_cells))
        for cage, enc in tqdm(cell_type_dict.items()):
            if self.real_random:
                index_filter = self.encode_data.loc[self.encode_data.any(axis="columns")]
            else:
                index_filter = self.encode_data.loc[self.encode_data[enc] == 1]
            index_filter = index_filter.index
            thresholds = [self.settings.NON_TARGET_CELLTYPES_INACTIVITY, self.settings.TARGET_CELLTYPE_ACTIVITY,
                          self.settings.REG_ELEMENT_SPARSENESS]
            if self.random_assay:
                vencodes_data = self._get_random_combinations(self._get_data_filtered(cage, thresholds,
                                                                                      files_path="outside",
                                                                                      index_filter=index_filter))
                self.vencode_numbers[cage] = 500
            else:
                ctn = False
                while True:
                    try:
                        data_filtered = self._get_data_filtered(cage, thresholds, files_path="outside",
                                                                index_filter=index_filter)
                        if len(data_filtered.data.index) < (2 * self.settings.K):
                            ctn = True
                            break
                        vencodes_object = self._search_vencodes_from_data(data_filtered)
                        break
                    except exceptions.NoVencodeError:
                        thresholds[2] -= 5
                        if thresholds[2] < 85:
                            vencodes_object = None
                            print("Warning: no VEnCodes found for {}".format(cage))
                            ctn = True
                            break
                if ctn:
                    continue
                vencodes_data = vencodes_object.get_vencode_data(method="return")
                self.vencode_numbers[cage] = len(vencodes_object.vencodes)
            self.matrix.loc[cage] = self._vencode_in_encode(vencodes_data)

    def total_random(self, validate=False, rows=20, comb=500):
        if validate:
            data = self.encode_data.loc[self.encode_data.any(axis="columns")]
        else:
            data = self.encode_data
        for i in tqdm(range(rows)):
            vencodes_data = self._get_random_combinations(data, n=comb)
            self.vencode_numbers[str(i)] = comb
            self.matrix.loc[str(i)] = self._vencode_in_encode(vencodes_data)

    def get_matrix(self, file_name="matrix.csv", sep=";"):
        """
        Retrieves the matrix and normalized matrix including a file with the normalization factor:
        the number of VEnCodes per cell type used in the analysis.
        :param file_name: name for the file, with extension (.csv, .tsv, .txt, etc)
        :param sep: separator used in the file.
        """
        search = re.search(r"(.+)(\.[a-zA-Z]{3}$)", file_name)
        name = search.group(1)
        extension = search.group(2)
        self.matrix.to_csv(file_name, sep=sep)
        self.vencode_numbers.to_csv(name + "-VEnCode number" + extension, sep=sep)
        normalize_multiplier = self.vencode_numbers.apply(lambda x: 100 / x)
        matrix_normalized = self.matrix.multiply(normalize_multiplier, axis="index")
        matrix_normalized.to_csv(name + "-normalized" + extension, sep=sep)

    def _vencode_in_encode(self, data):
        val_series = pd.Series(index=self.encode_data.columns,
                               data=np.zeros(len(self.encode_data.columns)), dtype=int)
        for vencode in data:
            encode_ven = self.encode_data.loc[vencode.index]
            total = encode_ven.sum(numeric_only=True, axis=0)
            total = total.floordiv(4)
            val_series = val_series.add(total, fill_value=0)
        return val_series

    def _search_vencodes_full(self, cell_type, thresholds, files_path="outside"):
        return iext.GetVencode(cell_type=cell_type,
                               data_type=self.settings.DATA_TYPE, algorithm=self.settings.ALGORITHM,
                               n_regulatory_elements=self.settings.K,
                               number_vencodes=self.settings.NUMBER_VENCODES_TO_GET,
                               parsed=val_util.status_parsed(cell_type),
                               thresholds=thresholds, n_samples=10000,
                               sample_type=self.settings.TYPE,
                               files_path=files_path)

    def _search_vencodes_from_data(self, data):
        vencodes = internals.Vencodes(data, algorithm="sampling", number_of_re=self.settings.K, n_samples=10000)
        vencodes.next(amount=self.settings.NUMBER_VENCODES_TO_GET)
        if vencodes.vencodes:
            return vencodes
        else:
            raise exceptions.NoVencodeError("No VEnCodes found!")

    def _get_data_filtered(self, cell_type, thresholds, files_path="outside", index_filter=None):
        # Get data:
        data_tpm = internals.DataTpmFantom5(file="parsed", sample_types=self.settings.TYPE, data_type=self.settings.DATA_TYPE,
                                            files_path=files_path)
        data_tpm.make_data_celltype_specific(cell_type)
        # Filter data:
        non_tgt_ctp_inact, tgt_ctp_act, reg_el_spsness = thresholds
        data_tpm.filter_by_target_celltype_activity(threshold=tgt_ctp_act, binarize=False)
        data_tpm.filter_by_reg_element_sparseness(threshold=reg_el_spsness)
        data_tpm.define_non_target_celltypes_inactivity(threshold=non_tgt_ctp_inact)
        if index_filter is not None:
            data_tpm.data = data_tpm.data.filter(items=index_filter, axis=0)
        else:
            pass
        return data_tpm

    def _get_random_combinations(self, data_tpm, n=500):
        # Get random combinations of rows in data:
        combinations_list = list()
        for i in range(n):
            if isinstance(data_tpm, pd.DataFrame):
                comb = data_tpm.sample(n=self.settings.K, replace=False)
            else:
                comb = data_tpm.data.sample(n=self.settings.K, replace=False)
            combinations_list.append(comb)
        return combinations_list


if __name__ == "__main__":
    settings_ = Settings()

    # Optional:
    enc_data_path = "D:/Utilizador HDD/" \
                    "OneDrive - Nova Medical School Faculdade de Ciências Médicas da UNL/" \
                    "1-Research/3-Vencode/Fantom5/Files/Validation_files/ENCODE/" \
                    "ENCODE DNase expression in FANTOM5 {}_merged.csv".format(settings_.DATA_TYPE)

    ven = EncodeValidateVencodes(settings_, merged=True, data_path=enc_data_path, random_assay=False, real_random=False)
    path = os.path.join(settings_.PATH_OUT_VEN, "matrix_{}_totalrandom_validated.csv".format(settings_.DATA_TYPE))
    # ven.validate_active(delete=[5, 8, 13])  # delete=[6, 9]
    ven.total_random(rows=20, comb=500, validate=True)
    ven.get_matrix(file_name=path)
