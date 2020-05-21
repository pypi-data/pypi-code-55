""" internals.py: Classes module for the VEnCode project """

import os
import random
import re
import tkinter as tk
from tkinter import filedialog
from copy import copy, deepcopy
from pathlib import Path
from collections import defaultdict
import inspect

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pylab

import VEnCode.utils.dir_and_file_handling as d_f_handling
from VEnCode import common_variables as cv
from VEnCode.utils import general_utils as gen_util, pandas_utils as pd_util


class DataTpm:
    """
    An Object representing a data set to retrieve VEnCodes from. Contains optional filtering methods and other tools.
    Create this object to help prepare the data for VEnCode generation. The essential and recommended methods to call
    before feeding this data set to a VEnCode object is shown in the Methods section. All the other methods are helper
    functions that facilitate the preparation of the data.

    Attributes
    ----------
    data : pd.DataFrame
        This object is a pandas DataFrame representation of the initial input data set.
    target : str
        The celltype or celltypes that are going to be the target of the VEnCode search algorithms.
        By calling the method make_data_celltype_specific(), the user can define this object and then apply activity,
        inactivity, sparseness filters, and other methods.
    target_replicates
        The target celltype/s replicates in the data.
    shape

    Parameters
    ----------
    file : str, pd.DataFrame
        The file containing the data set to convert into DataTpm object. This can be a complete path to the file,
        or just the file name, provided the path is given in the argument `files_path`. Alternatively, use 'custom'
        to open a file dialog to pick the file. Supported file formats are .csv, .txt, .tsv, or any format
        supported by the pandas read_csv function. Finally, a pandas DataFrame object can be supplied in this parameter
        instead of any file. Default is 'custom'.
    sep : str
        The column separator used in the input file. Default is ','.
    nrows : int, None
        The number of rows to open in the file. Default is 'None', which will open the entire file.
    files_path : str, None
        In case the argument `file` does not contain a complete path, input that path here. This argument is also
        useful to access the module's test files by inputting 'test'. Default is 'None'.
    kwargs
         Optional keyword arguments available to use are any used by pandas DataFrame object.
         Please refer to the pandas DataFrame documentation for specific details.

    Methods
    -------
    load_data()
        Essential method to call after DataTpm class object generation. Data is not automatically accessed at object
        generation to give this class more flexibility to subclassing.

    make_data_celltype_specific(target_celltype, replicates=True)
        Method recommended to provide the VEnCode object with the information on which celltype is the target.
    """

    def __init__(self, file="custom", files_path=None, sep=";", nrows=None, **kwargs):
        self._file, self._nrows, self._sep, self.kwargs = file, nrows, sep, kwargs
        self.target, self.target_replicates, self.data = None, defaultdict(list), None
        if files_path == "test":
            self._parent_path = os.path.join(str(Path(__file__).parents[0]), "Files")
        elif files_path == "outside":
            self._parent_path = os.path.join(str(Path(__file__).parents[2]), "Files")
        else:
            self._parent_path = files_path
        self._file_path, self.data = None, None

    @property
    def shape(self):
        """
        Outputs the shape of the data's data frame.

        Returns
        -------
        list
            The shape of the data in (rows, cols).
        """
        return self.data.shape

    def __eq__(self, other):
        """ Allows to check equality between two DataTpm objects. """
        if isinstance(other, DataTpm):
            args_list = [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a))]
            for arg in args_list:
                arg_self, arg_other = "self." + arg, "other." + arg
                if isinstance(eval(arg_self), pd.DataFrame):
                    try:
                        condition = eval(arg_self + ".equals(" + arg_other + ")")
                    except ValueError:
                        cols = eval(arg_self + ".columns.values.tolist()") == eval(arg_other
                                                                                   + ".columns.values.tolist()")
                        rows = eval(arg_self + ".index.values.tolist()") == eval(arg_other
                                                                                 + ".index.values.tolist()")
                        condition = cols and rows
                    except AttributeError as e:
                        print(e)
                        return False
                    if not condition:
                        return False
                    else:
                        continue
                try:
                    if eval(arg_self + "==" + arg_other):
                        continue
                except ValueError:
                    return False
                else:
                    return False
            return True
        return False

    def load_data(self):
        """
        Opens the data file with the previously provided arguments, storing the data set into the class attribute
        `data`.
        This method is not called during initialization to allow the DataTpm object to be easily extended by users.
        """
        self._file_path = self._filename_handler()
        if isinstance(self._file, pd.DataFrame):
            self.data = self._file
        else:
            self.data = pd.read_csv(self._file_path, sep=self._sep, index_col=0, nrows=self._nrows, engine="python",
                                    **self.kwargs)

    def copy(self, deep=True):
        """
        Method to generate a shallow, or deep copy of DataTpm object.

        Parameters
        ----------
        deep : bool
            True if deep copy.
        """
        if deep:
            return deepcopy(self)
        else:
            return copy(self)

    def sort_columns(self, col_to_shift=None, pos_to_move=None):
        """
        Sorts columns alphabetically.
        """
        if not col_to_shift or pos_to_move:
            cols = sorted(self.data.columns, key=str.lower)
            self.data = self.data.reindex(cols, axis=1)
        else:
            arr = self.data.columns.values
            idx = self.data.columns.get_loc(col_to_shift)
            if idx == pos_to_move:
                pass
            elif idx > pos_to_move:
                arr[pos_to_move + 1: idx + 1] = arr[pos_to_move: idx]
            else:
                arr[idx: pos_to_move] = arr[idx + 1: pos_to_move + 1]
            arr[pos_to_move] = col_to_shift
            self.data.columns = arr

    def make_data_celltype_specific(self, target_celltype, replicates=True):
        """
        Determines celltype/replicate (columns) of interest to analyse later.

        Parameters
        ----------
        target_celltype : str, dict
            The celltype to target for analysis, as a string. If the celltype has replicates in the data, either supply
            `target_celltype` with a dictionary in the shape dict[celltype] = [replicates], or let the function
            guess the replicates by supplying the argument `replicates` as True.
        replicates : bool
            If the celltype to target have replicates in the data, use True. Else, use False.
            Default is True.
        """
        if replicates:
            if isinstance(target_celltype, dict):
                self.target = list(target_celltype.keys())[0]
                self.target_replicates = target_celltype
            else:
                self.target = target_celltype
                self.target_replicates = self._code_selector(self.data, self.target, to_dict=True, regex=False)
        else:
            self.target = target_celltype
            self.target_replicates[target_celltype] = target_celltype

    def merge_replicates(self, replicate_suffix=None, celltype_list=None, replicate_dict=None, exclude_target=False,
                         not_include=None):
        """
        Merges replicate samples into one celltype.
        A more conservative, but faster approach to data set mining.
        Cell type columns are created by merging all replicates for that cell type. The value for the merged
        column corresponds the average of all donors.

        Parameters
        ----------
        replicate_suffix : str, None
            If the replicates have a defined suffix, this parameter helps the algorithm to find the correct replicates.
            e.g. if the samples are in the format - celltype_rep1, then use `replicate_suffix='_rep'`. Note that after
            the suffix there must be the unique number for that replicate.
        celltype_list: list
            Alternatively, provide the common characters in each group of replicates to merge and the function will try
            to merge by inference. Make sure to provide the list of characters as a complete list of columns to merge.
        replicate_dict: dict
            As a last alternative, provide a dictionary with the names for the merged celltypes and their corresponding
            replicates. Use full names for the replicates here.
            e.g.::

                rep_dict = {celltype1: [rep1, rep2, rep3], celltype2: [rep1, rep2]}

        exclude_target : bool
            True if the target celltype replicates are not to be merged. Otherwise, False.
        not_include : dict
            Dictionary containing key:value pairs where key are the celltype names (as provided in the first arguments)
            and values are partial- or complete-matching strings to columns that are not to be merged with the others
            for that celltype, but could be getting caught up by the algorithm. e.g. celltype "adipocyte" could be
            merging all replicates for the pre-adipocytes. In this case supplying the dictionary {adipocyte: ["pre"]
            would exclude all pre-adipocyte replicates from merging with the adipocyte replicates}. Default is `None`.
        """
        if replicate_suffix is not None:
            codes_merging = defaultdict(list)
            regex_pattern = r"(.+){}".format(replicate_suffix)
            for col in self.data.columns:
                match = re.match(regex_pattern, col)
                if match:
                    codes_merging[match.group(1)].append(col)
            if not_include is not None:  # remove some codes that regex might have not been able to differentiate
                for key, values in not_include.items():
                    if key not in codes_merging.keys():
                        continue
                    codes_df = self.data[codes_merging.get(key)]
                    not_codes = self._not_include_code_getter(values, codes_df)
                    codes_merging[key] = list(set(codes_merging[key]) - set(not_codes))
            self.data = self._merging_main(codes_dict=codes_merging, exclude_target=exclude_target)

        elif celltype_list is not None:
            codes_merging = self._code_selector(self.data, celltype_list, not_include=not_include, to_dict=True,
                                                regex=False)
            self.data = self._merging_main(codes_dict=codes_merging, exclude_target=exclude_target)

        elif replicate_dict is not None:
            self.data = self._merging_main(codes_dict=replicate_dict, exclude_target=exclude_target)

        if not exclude_target:
            self.target_replicates[self.target] = self.target  # The replicates are gone from data.

    def filter_by_target_celltype_activity(self, threshold=1, replicates="all", binarize=True):
        """
        Applies a filter to the Data, retaining only the regulatory elements that are expressed in the celltype of
        interest at >= x TPM, x being the threshold variable.

        Parameters
        ----------
        threshold : int, float
            TPM value used to filter the data.
        replicates : list
            Used to select only a few replicates from all the target celltype replicates. Can be the full name of the
            replicates to use in the filter, or their column index numbers relative to all that celltype's replicates.
        binarize : bool
            Convert target cell type expression to 0 and 1, for values below or above the threshold, respectively.
        """
        celltype_target = self.target_replicates[self.target]
        if isinstance(celltype_target, (list, tuple, np.ndarray)):
            if replicates == "all":
                for rep in celltype_target:
                    self.data = self.data[self.data[rep] >= threshold]
            else:
                for i in replicates:
                    try:
                        rep = celltype_target[i]
                    except TypeError:
                        rep = i
                    self.data = self.data[self.data[rep] >= threshold]
        else:
            self.data = self.data[self.data[celltype_target] >= threshold]
        if binarize:
            try:
                self.data[celltype_target] = self.data[celltype_target].applymap(lambda x: 0 if x <= threshold else 1)
            except AttributeError:
                self.data[celltype_target] = self.data[celltype_target].apply(lambda x: 0 if x <= threshold else 1)

    def define_non_target_celltypes_inactivity(self, threshold=0):
        """
        Converts the non-target celltypes' data to binary (0 - inactive; 1- active) given a threshold.

        Parameters
        ----------
        threshold : int, float
            Maximum TPM that non-target celltypes can have to be considered inactive.
        """
        try:
            celltypes_non_target = self.data.columns.difference(self.target_replicates[self.target])
        except TypeError:
            celltypes_non_target = self.data.columns.difference([self.target_replicates[self.target]])
        try:
            self.data[celltypes_non_target] = self.data[celltypes_non_target].applymap(
                lambda x: 0 if x <= threshold else 1)
        except AttributeError:
            self.data[celltypes_non_target] = self.data[celltypes_non_target].apply(
                lambda x: 0 if x <= threshold else 1)

    def filter_by_reg_element_sparseness(self, threshold=90, min_re=50, exclude_target=True):
        """
        Applies a filter to the Data, retaining only the regulatory elements in which xth percentile (x being the
        threshold variable) value is 0 (that is: not expressed). It will exclude the target celltype from the
        calculations. This filter will, then, retain only the REs with most 0 TPM for all non-target celltypes.
        The data must be made celltype specific first.

        Parameters
        ----------
        threshold : int
            Percentile value used to filter the data.
        min_re : int
            Minimum number of regulatory elements (RE) to keep in the data.
        exclude_target : bool
            Usually we want target expression to be the opposite of sparse, but in case the opposite is true, inputting
            `False` in this parameter will include the target in the sparseness filter.
        """
        if exclude_target:
            self.data, column_name = pd_util.df_percentile_calculator(self.data, threshold,
                                                                      celltype=self.target_replicates[self.target])
        else:
            self.data, column_name = pd_util.df_percentile_calculator(self.data, threshold,
                                                                      celltype=None)
        rows_to_keep = self.data[column_name] == 0
        while sum(rows_to_keep) < min_re and threshold > 5:
            threshold -= 5
            self.data.drop(column_name, axis=1, inplace=True)
            if exclude_target:
                self.data, column_name = pd_util.df_percentile_calculator(self.data, threshold,
                                                                          celltype=self.target_replicates[self.target])
            else:
                self.data, column_name = pd_util.df_percentile_calculator(self.data, threshold,
                                                                          celltype=None)
            rows_to_keep = self.data[column_name] == 0
        if sum(rows_to_keep) >= min_re:
            self.data = pd_util.df_filter_by_column_value(self.data, column_name, value=0)
            self.data.drop(column_name, axis=1, inplace=True)
        else:
            self.data.drop(column_name, axis=1, inplace=True)

    def sort_sparseness(self, exclude_target=True, descending=True):
        """
        Sorts the data by sparsest RE.

        Parameters
        ----------
        exclude_target : bool
            Usually we want to sort the sparseness of just the non-target celltypes, but in case the opposite is true,
            inputting `False` in this parameter will include the target in the sorting method.
        descending : bool
            `True` if the data is to be sorted in descending sparseness (most sparse appear on top). `False` otherwise.
        """
        if exclude_target:
            self.data["sum"] = self.data.drop(self.target_replicates[self.target], axis=1).sum(
                axis=1)  # create a extra column with the sum of 1s for each row (Reg. Element)
        else:
            self.data["sum"] = self.data.sum(axis=1)  # create a extra column with the sum of 1s for each row (RE)
        self.data.sort_values(["sum"], inplace=True, ascending=descending)  # sort REs based on the previous sum.
        self.data.drop(["sum"], axis=1, inplace=True)  # now remove the sum column

    def remove_celltype(self, celltypes):
        """
        Removes a specific celltype (column) from data.

        Parameters
        ----------
        celltypes : str, list
            celltype(s) to remove (columns).
        """
        try:
            self.data.drop(celltypes, axis=1, inplace=True)
        except (ValueError, KeyError) as e:
            print("Celltype not removed. {} is not contained in the data".format(e.args[0]))

    def remove_element(self, elements):
        """
        Removes a specific regulatory element (row) from data.

        Parameters
        ----------
        elements : str, list
            Regulatory element/s to remove (rows).
        """
        try:
            self.data.drop(elements, axis=0, inplace=True)
        except ValueError as e:
            print("Regulatory elements not removed due to: {}".format(e.args[0]))

    def add_celltype(self, celltypes=False, data_from="custom", **kwargs):
        """
        Adds expression data for celltypes from other data sets (with similar regulatory element information).
        Examples include adding data from a cancer celltype to a primary celltype data set.

        Parameters
        ----------
        celltypes : str, list, dict
            Celltypes to merge with the DataTpm data. If false it will add all provided data.
        data_from : str, DataTpm
            Data containing the celltypes to add. Can be either another DataTpm object or the path to a file eligible
            to be converted into a DataTpm object.
            "custom" will open a file dialog.
        kwargs :
            Are used to create a new DataTpm object from "data_from" to add to the data set.
            So, if that is the case, check DataTpm documentation.
        """
        # Deal with possible "celltypes" dict input type:
        if isinstance(celltypes, dict):
            celltypes = list(celltypes.values())[0]
        # Deal with different "data_from" variable input types:
        if isinstance(data_from, DataTpm):
            data_new = data_from.copy(deep=True)
        else:
            nrows = kwargs.pop("nrows", None)
            if nrows is None:
                nrows = self._nrows
            data_new = DataTpm(file=data_from, nrows=nrows, **kwargs)
            data_new.load_data()
        assert isinstance(data_new, DataTpm), "data_from parameter should be a DataTpm object, or a path to a file" \
                                              "capable of being turned into one."
        # add data to self.data:
        if celltypes:
            data_concat = data_new.data[celltypes]
        else:
            data_concat = data_new.data
        self.data = pd.concat([self.data, data_concat], axis=1)

    def drop_target_ctp(self, inplace=True):
        """
        Shortcut function to drop the target celltypes from the data set. It handles the fact that the data may have
        been merged or not.

        Parameters
        ----------
        inplace : bool
            `True` modifies the class attribute `data` in place, and the function returns `None`. `False` tells the
            function to return the data after dropping the target celltypes.

        Returns
        -------
        DataTpm
            The data without the target celltypes. But also modifies it in place
        """
        data = self.data.drop(self.target_replicates[self.target], axis=1, inplace=inplace)
        return data

    def binarize_data(self, threshold=0):
        """
        Converts all data to 0 and 1, where 1 is any value above threshold.

        Parameters
        ----------
        threshold : int
            Maximum expression value for a RE to be considered inactive.
        """
        self.data = self.data.applymap(lambda x: 0 if x <= threshold else 1)

    def to_csv(self, *args, **kwargs):
        """
        Generates a csv file. args and kwargs passed must be compatible to Pandas DataFrame.to_csv()

        Parameters
        ----------
        args
            Arguments to be passed on to pandas DataFrame.to_csv()
        kwargs
            Keyword arguments to be passed on to pandas DataFrame.to_csv()
        """
        self.data.to_csv(*args, **kwargs)

    def _filename_handler(self):
        """ Handles different file names inputs in the arguments. """
        if isinstance(self._file, pd.DataFrame):
            file_path = None
        elif self._file == "custom":
            root = tk.Tk()
            root.withdraw()
            file_path = tk.filedialog.askopenfilename()
        elif re.search(r"\....", self._file[-4:]):
            if self._parent_path is not None:
                file_path = os.path.join(self._parent_path, self._file)
            else:
                file_path = self._file
                self._parent_path, self._file = os.path.split(os.path.abspath(self._file))
        else:
            raise AttributeError
        return file_path

    def _code_selector(self, data, celltype, not_include=None, to_dict=False, regex=True):
        """ Selects celltype codes from database using their general name. """
        if isinstance(celltype, str):  # celltype can be provided as a list or string
            celltype = [celltype]
        codes = []
        code_dict = {}
        for item in celltype:
            if regex:
                codes_list = pd_util.df_complete_regex_columns_finder(item, data)
            else:
                codes_list = pd_util.df_minimal_regex_columns_finder(item, data)

            if to_dict:
                code_dict[item] = codes_list
            else:
                codes.append(codes_list)
        if not to_dict:
            codes = [item for sublist in codes for item in sublist]  # make one list from nested lists of codes

        if not_include is not None:  # remove some codes that regex might have not been able to differentiate
            for key, values in not_include.items():
                if key not in code_dict.keys():
                    continue
                codes_df = data[code_dict.get(key)]
                not_codes = self._not_include_code_getter(values, codes_df)
                code_dict[key] = list(set(code_dict[key]) - set(not_codes))

        if to_dict:
            codes = code_dict
        self._code_tester(codes, celltype)
        return codes

    def _merging_main(self, codes_dict, exclude_target=False):
        if exclude_target:
            codes_dict.pop(self.target, None)
        data_merged = pd.DataFrame(index=self.data.index.values, columns=[key for key in codes_dict.keys()])
        if exclude_target:
            data_merged = pd.concat([data_merged, self.data[self.target_replicates[self.target]]], axis=1)
        for code, donors in codes_dict.items():
            celltypes_averaged = self.data[donors].apply(np.mean, axis=1)
            data_merged[code] = celltypes_averaged
        data = data_merged
        return data

    @staticmethod
    def _not_include_code_getter(not_include, data_frame):
        """
        Function streamlined to deduce the names of columns from `DataTpm.data` for celltypes that are not to be
        included.
        """
        if isinstance(not_include, list):
            not_include_codes = []
            for item in not_include:
                not_codes_item = pd_util.df_regex_columns_finder(item, data_frame)
                not_include_codes.append(not_codes_item)
            not_include_codes = [item for sublist in not_include_codes for item in sublist]
        else:
            not_include_codes = pd_util.df_regex_columns_finder(not_include, data_frame)
        return not_include_codes

    @staticmethod
    def _code_tester(codes, celltype, codes_type="list"):
        """ Tests if any codes were generated. """
        if codes_type == "list":
            if not codes:
                raise Exception("No codes for {}!".format(celltype))
        elif codes_type == "dict":
            if bool([a for a in codes.values() if a == []]):
                print([item for item, value in codes.items() if not value])
                raise Exception("Some celltypes might not have had codes generated!")
        elif codes_type == "ndarray":
            if codes.size == 0:
                raise Exception("No codes for {}!".format(celltype))
        else:
            raise Exception("Wrong codes type to test for the generation of codes!")


class DataTpmFantom5(DataTpm):
    """
    An Object specifically representing the initial FANTOM5 CAGE-seq data set with some universal data treatment and
    with optional filtering methods.
    Create this object to help prepare the FANTOM5 CAGE-seq data for VEnCode generation. The recommended method to call
    before feeding this data set to a VEnCode object is shown in the Methods section. All the other methods are helper
    functions that facilitate the preparation of the data.

    Attributes
    ----------
    data : pd.DataFrame
        This object is a pandas DataFrame representation of the initial input data set.
    target : str
        The celltype or celltypes that are going to be the target of the VEnCode search algorithms.
        By calling the method make_data_celltype_specific(), the user can define this object and then apply activity,
        inactivity, sparseness filters, and other methods.
    target_replicates
        The target celltype/s replicates in the data.
    sample_type
        The origin/type of samples to be analysed from the CAGE-seq data.
    data_type
        The type of RE that comprises the data.
    shape

    Parameters
    ----------
    file : str, pd.DataFrame
        The file containing the data set to convert into DataTpm object. This can be a complete path to the file,
        or just the file name, provided the path is given in the argument `files_path`. Alternatively, use 'custom'
        to open a file dialog to pick the file. Supported file formats are .csv, .txt, .tsv, or any format
        supported by the pandas read_csv function. Finally, a pandas DataFrame object can be supplied in this parameter
        instead of any file. Default is 'custom'.
    sep : str
        The column separator used in the input file. Default is ','.
    nrows : int, None
        The number of rows to open in the file. Default is 'None', which will open the entire file.
    sample_types : str
        The origin/type of samples to be analysed from the CAGE-seq data. Currently offering full support for
        `primary cells` and `cell lines`.
    data_type : str
        The type of RE that comprises the data. `promoters` or `enhancers`.
    files_path : str, None
        In case the argument `file` does not contain a complete path, input that path here. This argument is also
        useful to access the module's test files by inputting 'test'. Default is 'test'.
    kwargs
         Optional keyword arguments available to use are any used by pandas DataFrame object.
         Please refer to the pandas DataFrame documentation for specific details.

    Methods
    -------
    make_data_celltype_specific(target_celltype, replicates=True)
        Method to provide the VEnCode object with the information on which celltype is the target.
    """

    def __init__(self, file="custom", sample_types="primary cells", data_type="promoters", keep_raw=False, nrows=None,
                 files_path="test", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._file, self.sample_type, self.data_type, self._nrows = file, sample_types, data_type, nrows
        self.target, self.target_replicates, self.ctp_not_include, self.data = None, None, None, None
        self._file_path = None
        if files_path == "test":
            self._parent_path = os.path.join(str(Path(__file__).parents[0]), "Files")
        elif files_path == "outside":
            self._parent_path = os.path.join(str(Path(__file__).parents[2]), "Files")
        else:
            self._parent_path = files_path

        if sample_types in ("cell lines", "tissues"):
            celltype_exclude = None
        elif sample_types == "primary cells":
            celltype_exclude = cv.primary_exclude_list
        else:
            celltype_exclude = None

        if self._file != "parsed":
            self.ctp_exclude = celltype_exclude
            self._file_path = self._filename_handler()
            self.sample_type_file = pd.read_csv(os.path.join(self._parent_path, cv.sample_type_file), sep=",",
                                                index_col=0,
                                                engine="python")
            if data_type == "promoters":
                skiprows = 1831
                if self._nrows is not None:
                    self._nrows += 2
            else:
                skiprows = None
            self.raw_data = pd.read_csv(self._file_path, sep="\t", index_col=0,
                                        skiprows=skiprows, nrows=self._nrows, engine="python")
            if data_type == "promoters":
                if self._nrows is not None:
                    self._nrows -= 2
                self._raw_data_promoters()
            elif data_type == "enhancers":
                self.names_db = pd.read_csv(os.path.join(self._parent_path, cv.enhancer_names_db), sep="\t",
                                            index_col=1,
                                            header=None, names=["celltypes"], engine="python")
                self._raw_data_enhancers()
            else:
                raise AttributeError("data_type argument is not supported")
            self.raw_data.apply(pd.to_numeric, downcast='float')  # optimizes memory usage by downcasting to lower float
            if sample_types in ("primary cells", "cell lines", "cancer", "time courses", "tissues"):
                self.data = self._raw_data_cleaner()
            else:
                self.data = self.raw_data
            if not keep_raw:
                self.raw_data = None
        else:
            pass

    def make_data_celltype_specific(self, target_celltype, supersets=cv.primary_cells_supersets):
        """
        Determines celltype/donors (columns) of interest to analyse later.
        For previously parsed files, opens the specific file for that celltype.

        Parameters
        ----------
        target_celltype : str, dict
            The celltype to target for analysis.
        supersets : dict
            When a celltype is a subset of other, we must remove that superset celltype to analyse the subset.
        """
        if self.sample_type == "cell lines":
            self.ctp_not_include = cv.cancer_not_include_codes
        elif self.sample_type == "primary cells":
            self.ctp_not_include = cv.primary_not_include_codes
        elif self.sample_type == "time courses":
            self.ctp_not_include = cv.time_courses_not_include_codes
        else:
            self.ctp_not_include = None
        if isinstance(target_celltype, dict):  # to deal with situations such as mesothelioma cell line
            target_ctp_in_data = list(target_celltype.values())[0]
        else:
            target_ctp_in_data = target_celltype

        if self._file == "parsed":
            if isinstance(target_celltype, dict):
                self.target = list(target_celltype.keys())[0]
            else:
                self.target = target_celltype
            self._file_path = self._filename_handler()
            self.data = pd.read_csv(self._file_path, sep=";", index_col=0,
                                    skiprows=None, nrows=self._nrows, engine="python")
            self.target_replicates = self._code_selector(self.data, target_ctp_in_data,
                                                         not_include=self.ctp_not_include,
                                                         to_dict=True, regex=True)
            # enhancers might need regex to be False:
            if isinstance(target_ctp_in_data, str):
                target_ctp_in_data = [target_ctp_in_data]
            else:
                target_ctp_in_data = target_ctp_in_data
            for celltype in target_ctp_in_data:
                if not self.target_replicates[celltype]:
                    self.target_replicates = self._code_selector(self.data, target_ctp_in_data,
                                                                 not_include=self.ctp_not_include,
                                                                 to_dict=True, regex=False)
                    break
                else:
                    continue
            if isinstance(target_celltype, dict):
                temp_dict = {self.target: list(
                    gen_util.flatten_irregular_nested_lists(list(self.target_replicates.values())))}
                self.target_replicates = temp_dict

        else:
            self.target_replicates = self._code_selector(self.data, target_ctp_in_data,
                                                         not_include=self.ctp_not_include,
                                                         to_dict=True, regex=False)
            if isinstance(target_celltype, dict):  # to deal with situations such as mesothelioma cell line
                self.target = list(target_celltype.keys())[0]
                temp_dict = \
                    {self.target: list(
                        gen_util.flatten_irregular_nested_lists(list(self.target_replicates.values())))}
                self.target_replicates = temp_dict
            else:
                self.target = target_celltype
        if supersets and self.target in supersets.keys():
            self.data.drop(supersets[self.target], axis=1, inplace=True)

    def merge_donors_primary(self, exclude_target=True):
        """
        Merges replicate samples into one celltype. Specific method to use when dealing with FANTOM5 primary celltypes.

        A more conservative, but faster approach to data set mining.
        Celltype columns are created by merging all replicates/donors for that celltype. The value for the merged
        column corresponds the average of all replicates/donors.

        Parameters
        ----------
        exclude_target : bool
            True if the target celltype replicates are not to be merged. Otherwise, False.
        """
        if self._file == "parsed":
            return
        codes = self._code_selector(self.data, cv.primary_cell_list, not_include=cv.primary_not_include_codes,
                                    to_dict=True, regex=False)
        self.data = self._merging_main(codes, exclude_target=exclude_target)
        return

    def add_celltype(self, celltypes=False, data_from="custom", sample_types="cell lines", fantom=True, **kwargs):
        """
        Adds expression data for celltypes from other data sets (with similar regulatory element information).
        Examples include adding data from a cancer cell type to a primary cell type data set.

        Parameters
        ----------
        celltypes : str, list, dict
            Celltypes to merge with the DataTpmFantom5 data. If false it will add all provided data.
        data_from : str, DataTpm
            Data containing the celltypes to add. Can be either another DataTpm object or the path to a file eligible
            to be converted into a DataTpm object.
            "custom" will open a file dialog.
        sample_types : str
            Sample type ("primary cells", for e.g.) of the data set to add.
        fantom : bool
            Is your data to add from FANTOM5 CAGE-seq? if so put True. Else, False.
        kwargs :
            Are used to create a new DataTpmFantom5 object from "data_from" to add to the data set.
            So, if that is the case, check DataTpmFantom5 documentation.
        """
        # handle possible supersets in the data
        if sample_types == "cell lines":
            supersets = None
        elif sample_types == "primary cells":
            supersets = cv.primary_cells_supersets
        else:
            supersets = None
        # Deal with different "celltypes" variable input types
        if isinstance(celltypes, str):
            celltypes = [celltypes]
        elif isinstance(celltypes, dict):  # to deal with situations such as mesothelioma cell line
            celltypes = list(celltypes.values())[0]
        # Deal with different "data_from" variable input types
        if isinstance(data_from, DataTpm):
            data_new = data_from.copy()
        else:
            nrows = kwargs.pop("nrows", None)
            if nrows is None:
                nrows = self._nrows
            if fantom:
                data_new = DataTpmFantom5(file=data_from, sample_types=sample_types,
                                          nrows=nrows, **kwargs)
            else:
                data_new = DataTpm(file=data_from, nrows=nrows, **kwargs)
        assert isinstance(data_new, DataTpm), "data_from parameter should be a DataTpm object, or a path to a file" \
                                              "capable of being turned into one."
        # add data to self.data
        if celltypes:
            data_copy = data_new.copy(deep=True)
            for celltype in celltypes:
                if fantom:
                    data_new.make_data_celltype_specific(celltype, supersets=supersets)
                    data_new.data = data_new.data[data_new.target_replicates[celltype]]
                else:
                    data_new.data = data_new.data[celltype]
                self.data = pd.concat([self.data, data_new.data], axis=1)
                data_new = data_copy.copy(deep=True)
        else:
            self.data = pd.concat([self.data, data_new.data], axis=1)

    def remove_celltype(self, celltypes, merged=True):
        """
        Removes a specific celltype from the data.

        Parameters
        ----------
        celltypes : in, list
            Celltype(s) to remove.
        merged : bool
            If the data has been previously merged into celltypes, True. If columns represent replicates/donors, False.
        """

        def _remove(to_remove):
            try:
                self.data.drop(to_remove, axis=1, inplace=True)
            except (ValueError, KeyError) as e:
                print("Celltype not removed. {} is not contained in the data".format(e.args[0]))

        if not merged:
            celltypes_dict = self._code_selector(self.data, celltypes, not_include=self.ctp_not_include,
                                                 to_dict=True, regex=False)
            celltypes = [sub_item for item in list(celltypes_dict.values()) for sub_item in item]
        _remove(celltypes)

    def _filename_handler(self):
        if self._file == "custom":
            root = tk.Tk()
            root.withdraw()
            file_path = tk.filedialog.askopenfilename()
        elif re.search(r"\....", self._file[-4:]):
            file_path = os.path.join(self._parent_path, self._file)
        elif self._file == "parsed":
            celltype_name = self.target.replace(":", "-").replace("/", "-")
            file_path = os.path.join(self._parent_path, "Dbs", f"{celltype_name}_tpm_{self.data_type}-1.csv")
        else:
            raise AttributeError
        return file_path

    def _raw_data_promoters(self):
        self.raw_data.drop(self.raw_data.index[:2], inplace=True)

    def _raw_data_enhancers(self):
        column_names = {}
        for column_code in self.raw_data.columns.values.tolist():
            try:
                column_names[column_code] = self.names_db.loc[column_code, "celltypes"]
            except KeyError:
                pass
        self.raw_data.rename(columns=column_names, inplace=True)

    def _raw_data_cleaner(self):
        data_1 = self.raw_data.copy()
        universal_rna = self._code_selector(data_1, "universal", not_include=None)
        data_1.drop(universal_rna, axis=1, inplace=True)
        if self.data_type == "promoters":
            to_keep = self._sample_category_selector()
        else:
            to_keep = self._sample_category_selector(get="name")
        data = pd.DataFrame(index=data_1.index.values)
        for sample in to_keep:
            if self.data_type == "promoters":
                data_temp = data_1.filter(regex=sample)
                column_name = self.sample_type_file.loc[sample, "Name"]
                try:
                    data_temp.columns = [column_name]
                except ValueError:
                    column_name = [column_name + ", tech_rep1", column_name + ", tech_rep2"]
                    data_temp.columns = column_name
            else:
                try:
                    data_temp = data_1.loc[:, sample]
                except KeyError:
                    data_temp = pd_util.df_minimal_regex_columns_searcher(sample, data_1)
            try:
                data = data.join(data_temp)
            except ValueError:
                continue
        # Exclude some specific, on-demand, cell-types from the data straight away:
        if self.ctp_exclude is not None:
            codes_exclude = self._code_selector(data, self.ctp_exclude, not_include=None, regex=False)
            data.drop(codes_exclude, axis=1, inplace=True)
        return data

    def _sample_category_selector(self, get="index"):
        """
        Returns a list of cell types to keep/drop from a file containing the list of cell types and a
        'Sample category' column which determines which cell types to retrieve.
        """
        types = self.sample_type
        if not isinstance(types, list):
            types = [types]
        database = self.sample_type_file.copy()
        try:
            possible_types = database["Sample category"].drop_duplicates().values.tolist()
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            raise
        assert all(
            sample in possible_types for sample in types), "Sample type is not valid.\nValid sample types: {}" \
            .format(possible_types)
        celltypes = []
        for sample in types:
            selected = database[database["Sample category"] == sample]
            if get == "index":
                for value in selected.index.values:
                    celltypes.append(value)
            elif get == "name":
                for value in selected["Name"].tolist():
                    celltypes.append(value)
            else:
                pass
        return celltypes


class Vencodes:
    """
    An Object representing the VEnCodes found for a specific celltype. VEnCodes are combinations of regulatory elements
    that are active specifically in one celltype and inactive in all others.
    This class contains methods to search, retrieve, classify and visualize VEnCodes from a matrix of regulatory
    element (rows) expression levels per celltype (columns).

    Attributes
    ----------
    vencodes : list of str
        List of coordinates for the regulatory elements that constitute the VEnCodes found. There are other ways of
        retrieving VEnCode information, see Methods. To generate a list of VEnCodes, use the `next()` method.
    e_values : list of int
        `E` value score for the VEnCodes found. Must be first determined using the `determine_e_values()` method.
    data : DataTpm
        The original data set used to find VEnCodes.
    algorithm : str
        Algorithm used to find VEnCodes.
    k : int
        The VEnCode size. In other words, the number of regulatory elements that form each VEnCode.
    target_replicates : list of str, str
        The target samples names to retrieve VEnCodes from.
    target_replicates_data : pd.DataFrame
        A shortcut to the subset of the data corresponding to the target samples.

    Parameters
    ----------
    data_object : DataTpm, pd.DataFrame
        Data to use in finding VEnCodes. This should be a matrix of regulatory elements (rows) expression levels per
        celltype (columns). The matrix can be supplied as a DataTpm object, which has methods to quickly prepare the
        data, or as a pandas DataFrame object.
    algorithm : str
        Algorithm to find VEnCodes. Currently accepted: `heuristic`, `sampling`.
    number_of_re : int
        VEnCode size. In other words, the number of regulatory elements that should form each VEnCode.
    n_samples : int
        Number of random samples to take to try to find a VEnCode. Used only if ``algorithm="sampling"``
    stop : int
        Number of promoters to test per node level. Used only if ``algorithm="heuristic"``
    second_data_object : DataTpm, None
        If the current VEnCode object contains as source a set of promoter expression, supplying an enhancer DataTpm
        object here will allow retrieval of hybrid enhancer-promoter VEnCodes.
    using : str, list, None
        Allows the user to force some REs to be in the VEnCode, if possible.
    target : str, None
        When supplying the VEnCode object with a DataFrame, the target celltype must be specified here.

    Methods
    -------
    next(amount=1)
        Call this function to generate the next VEnCode. The VEnCode is appended to the variable `vencodes` and
        can also be returned as a variable.
    determine_e_values(repetitions=100)
        Call this function to generate e-values for the current VEnCodes. E-values will be stored in the variable
        called e_values. Method applied to calculate e-values is a Monte-Carlo simulation.
    export(*args, path=None, verbose=True):
        Call this method to export vencode related values to CSV files.
        Put "vencodes" in the arguments to export each VEnCode to a CSV file, "e-values" to export the e-values,
        and "TPP" to export the tags per million expression of the REs that comprise the VEnCodes for the target
        celltype.
        You can put any amount of these arguments in the same function as long as they are supported.
        Use `path` to define a specific directory to store the file. (must be a complete path)
    """

    def __init__(self, data_object, algorithm, number_of_re=4, n_samples=10000, stop=5, second_data_object=None,
                 using=None, target=None):
        if isinstance(data_object, pd.DataFrame):
            assert target is not None, "Error: No target supplied. When supplying the VEnCode object with a DataFrame" \
                                       ", always input the target celltype in the target argument."
            data_tpm = DataTpm(file=data_object)
            data_tpm.load_data()
            data_tpm.make_data_celltype_specific(target)
            self._data_object = data_tpm.copy(deep=True)
        elif data_object.target is None:
            self._data_object = data_object.copy(deep=True)
            self._data_object.make_data_celltype_specific(target)
        else:
            self._data_object = data_object.copy(deep=True)

        self.algorithm, self.k = algorithm, number_of_re
        self.target_replicates = self._data_object.target_replicates[self._data_object.target]
        self.vencodes, self.e_values = [], {}
        self._parent_path = os.path.join(str(Path(__file__).parents[2]), "VEnCodes")

        self.target_replicates_data = self._data_object.data[self.target_replicates]
        self.data = self._data_object.data.copy(deep=True)
        self._data_not_target = self._data_object.drop_target_ctp(inplace=False)

        if second_data_object:
            self.second_data_object = second_data_object.copy()
        else:
            self.second_data_object = None

        if self.algorithm == "heuristic":
            self._stop = stop
            self._vencodes_generator = self._heuristic_method_vencode_getter()
        elif self.algorithm == "sampling":
            self._n_samples = n_samples
            self._vencodes_generator = self._sampling_method_vencode_getter(using=using)

    def __eq__(self, other):
        if isinstance(other, Vencodes):
            args_list = [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a))]
            for arg in args_list:
                arg_self, arg_other = "self." + arg, "other." + arg
                if isinstance(eval(arg_self), pd.DataFrame):
                    try:
                        condition = eval(arg_self + ".equals(" + arg_other + ")")
                    except ValueError:
                        cols = eval(arg_self + ".columns.values.tolist()") == eval(arg_other
                                                                                   + ".columns.values.tolist()")
                        rows = eval(arg_self + ".index.values.tolist()") == eval(arg_other
                                                                                 + ".index.values.tolist()")
                        condition = cols and rows
                    except AttributeError as e:
                        print(e)
                        return False
                    if not condition:
                        return False
                    else:
                        continue
                elif inspect.isgenerator(eval(arg_self)):
                    # there is no way to compare generators without changing their state.
                    continue
                try:
                    if eval(arg_self + "==" + arg_other):
                        continue
                except ValueError:
                    return False
                else:
                    return False
            return True
        return False

    def next(self, amount=1):
        """
        Call this function to generate the next VEnCode. The VEnCode is appended to the variable `vencodes` and
        can also be returned as a variable.

        Parameters
        ----------
        amount : int
            Number of vencodes to retrieve.

        Returns
        -------
        list
            A list containing the desired amount of vencodes.
        """
        num = 0
        vencode_list = []
        while num < amount:
            duplicate = False
            try:
                vencode = next(self._vencodes_generator)
            except StopIteration:
                break
            if self.vencodes:
                for previous_ven in self.vencodes:
                    if set(previous_ven) == set(vencode):
                        duplicate = True
            if not duplicate:
                num += 1
            if not duplicate and vencode:
                self.vencodes.append(vencode)
                vencode_list.append(vencode)
            else:
                continue
        return vencode_list

    def determine_e_values(self, repetitions=100):
        """
        Call this function to generate `e` values for the current VEnCodes. `E` values will be stored in the variable
        called `e_values`. The method applied to calculate `e` values is a Monte-Carlo simulation.

        Parameters
        ----------
        repetitions : int
            Number of times each vencode is evaluated to get the average value.
        """

        if self.vencodes is None:
            print("No VEnCodes found yet. Try generating new VEnCodes first with .next()")
            return
        for vencode in self.vencodes:
            if isinstance(vencode[0], list):
                vencode_tuple = tuple([tuple(item) for item in vencode])
                if vencode_tuple in self.e_values.keys():
                    continue
                else:
                    e_value_raw, k = self._e_value_calculator_two_data_sets(vencode, repetitions)
            else:
                vencode_tuple = tuple(vencode)
                if vencode_tuple in self.e_values.keys():
                    continue
                else:
                    e_value_raw = self._e_value_calculator(vencode, repetitions)
                    k = None
            e_value = self._e_value_normalizer(e_value_raw, k=k)
            self.e_values[vencode_tuple] = e_value

    def export(self, *args, path=None, verbose=True):
        """
        Call this method to export vencode related values to CSV files.
        Put "vencodes" in the arguments to export each VEnCode to a CSV file, "e-values" to export the e-values,
        and "TPP" to export the tags per million expression of the REs that comprise the VEnCodes for the target
        celltype.
        You can put any amount of these arguments in the same function as long as they are supported.
        Use `path` to define a specific directory to store the file. (must be a complete path)

        Parameters
        ----------
        args
            "e-values", "vencodes", "TPP" or even all at once.
        path : str, None
            Path to write a file to store the VEnCode data.
        verbose : bool
            Either to allow the function to print messages to console (`True`), or not (`False`).
        """
        if path is None:
            path_ = self._parent_path
        else:
            path_ = path

        if "e-values" in args and "TPP" not in args:
            self._export_e_values(path=path_, verbose=verbose)
        elif "e-values" in args and "TPP" in args:
            self._export_e_values_tpp(path=path_, verbose=verbose)
            # TODO: export e_values with Tags per million included

        if "vencodes" in args:
            self._export_vencodes(path=path_, verbose=verbose)

    def get_vencode_data(self, method="return"):
        """
        Call this function to get the VEnCode data as a variable (``method="return"``),
        or printed in terminal (``method="print"``).

        Parameters
        ----------
        method : str
            How to retrieve the data.

        """
        vencodes = []
        for vencode in self.vencodes:
            if method in ("print", "both"):
                print(self.data.loc[vencode])
            elif method == "return":
                vencodes.append(self.data.loc[vencode])
        if method == "return":
            return vencodes

    def view_vencodes(self, method="print", interpolation="nearest", path=None, snapshot=None, verbose=True):
        """
        Call this function to get an heat map visualization of the vencodes.

        Parameters
        ----------
        method : str
            Method to view VEnCodes. "print" to get visualization on terminal. "write" to write to a file. "both" for
            both.
        interpolation : str
            Method for heat map interpolation.
        path : str, None
            Optional path for the file.
        snapshot : int, None
            Number of celltypes to show in heat map. `False` gets all but may hinder visualization.
        verbose : bool
            Either to allow the function to print messages to console (`True`), or not (`False`).
        """
        for vencode in self.vencodes:
            self._heatmap(vencode, method=method, interpolation=interpolation, path=path, snapshot=snapshot,
                          verbose=verbose)

    def next_heuristic2_vencode(self, second_data_object, amount=1):
        """
        Call this function to generate the next VEnCode, possibly hybrid enhancer-promoter VEnCode.
        The VEnCode is appended to the variable self.vencodes.

        Parameters
        ----------
        second_data_object : DataTpm
            If the current VEnCode object contains as source a set of promoter expression, supplying an enhancer DataTpm
            object here will allow retrieval of hybrid enhancer-promoter VEnCodes.
        amount : int
            Number of vencodes to retrieve.
        """

        # TODO: needs to get the minimum number of second promoter/enhancers as possible. rn is getting k second RE
        self.second_data_object = second_data_object.copy()
        self.second_data_object.drop_target_ctp(inplace=True)
        sparsest = self._data_not_target.head(n=self.k)
        mask = sparsest != 0
        cols = sparsest.columns[np.all(mask.values, axis=0)].tolist()
        cols_target = second_data_object.ctp_analyse_donors[second_data_object.target_ctp]
        data_problem_cols = second_data_object.data[cols + cols_target]
        second_data_object.data = data_problem_cols
        if self.algorithm == "heuristic":
            vencode_heuristic2 = Vencodes(second_data_object, algorithm="heuristic", number_of_re=self.k,
                                          stop=self._stop)
            vencode_heuristic2.next(amount=amount)
        else:
            raise AttributeError("Algorithm - {} - currently not supported".format(self.algorithm))
        if vencode_heuristic2.vencodes:
            for vencode_second in vencode_heuristic2.vencodes:
                vencode = [sparsest.index.values.tolist(), vencode_second]
                self.vencodes.append(vencode)

    def heuristic2_vencode(self):  # TODO: must implement this within _node_based_algorithm
        """
        Call this function to generate the next VEnCode, possibly hybrid enhancer-promoter VEnCode.
        The VEnCode is appended to the variable self.vencodes.
        """
        # TODO: needs to get the minimum number of second promoter/enhancers as possible. rn is getting k second RE
        sparsest = self._data_not_target.head(n=self.k)
        mask = sparsest != 0
        cols = sparsest.columns[np.all(mask.values, axis=0)].tolist()
        cols_target = self.second_data_object.ctp_analyse_donors[self.second_data_object.target_ctp]
        data_problem_cols = self.second_data_object.data[cols + cols_target]
        self.second_data_object.data = data_problem_cols
        if self.algorithm == "heuristic":
            vencode_heuristic2 = Vencodes(self.second_data_object, algorithm="heuristic", number_of_re=self.k,
                                          stop=self._stop)
            vencode_heuristic2.next()
        else:
            raise AttributeError("Algorithm - {} - currently not supported".format(self.algorithm))
        if vencode_heuristic2.vencodes:
            vencode = [sparsest.index.values.tolist(), vencode_heuristic2.vencodes]
            self.vencodes.append(vencode)

    @staticmethod
    def vencode_mc_simulation(data, reps=100):
        """
        Simulates turning 0s to 1s over a data set, asking each turn if the data still represents a VEnCode.
        Tests the VEnCode robustness to false negatives in the data.

        Parameters
        ----------
        data : pd.DataFrame
            Data frame of promoter expression per celltype without the celltype of interest.
        reps : int
            Number of simulations to run.

        Returns
        -------
        int
            The `e` value, that is, the average number of random changes done to the data until it breaks the VEnCode.
        """
        col_list = data.columns.values
        index_list = data.index.values
        simulator = 0
        local_counter_list = []
        while simulator < reps:
            vencode = True
            local_counter = 0
            data_mutable = data.copy()
            while vencode:
                col = random.choice(col_list)
                index = random.choice(index_list)
                if data_mutable.loc[index, col] == 0:
                    local_counter += 1
                    data_mutable.at[index, col] = 1
                    a = data_mutable[col].tolist()
                    try:
                        a.index(0)  # searches for at least one 0 in that column. If there's no 0, it's not a VEnCode.
                    except ValueError:
                        vencode = False
                        local_counter_list.append(local_counter)
                else:
                    pass
            simulator += 1
        global_counter = np.mean(local_counter_list, dtype=np.float64)
        return global_counter

    def _sampling_method_vencode_getter(self, threshold=0, skip_sparsest=False, using=None):
        """
        Function that searches for a VEnCode in data using the sampling method. Please note that it retrieves a
        DataFrame containing the entire sample. This is the reason why it only retrieves one VEnCode.

        Parameters
        ----------
        threshold : int
            Minimum expression threshold that counts to consider a promoter inactive.
        skip_sparsest : bool
            Allows user to skip first check - check if sparsest REs already constitute a VEnCode.

        Yields
        ------
        list
            The promoters that constitute a VEnCode.
        """
        if not skip_sparsest:
            # try first to see if sparsest REs aren't already a VEnCode:
            sparsest = self._data_not_target.head(n=self.k)
            if self._assess_vencode_one_zero_boolean(sparsest, threshold=threshold):
                yield sparsest.index.values.tolist()
        i = 0

        if using is not None:  # allows user to force some REs to be in the VEnCode
            use = self._data_not_target.loc[using]
            if isinstance(using, list):
                n = self.k - len(using)
            else:
                n = self.k - 1
        else:
            use = None
            n = self.k

        while i < self._n_samples:
            try:
                sample = self._data_not_target.sample(n=n)  # take a sample of n promoters
            except ValueError as e:  # Combinations number could be larger than number of RE available.
                print("Combinations number (k) is probably larger than the number of RE available. {}".format(
                    e.args))
                break
            if using is not None:
                try:
                    sample.loc[using] = use
                except KeyError:
                    sample = pd.concat([sample, use])
            if self._assess_vencode_one_zero_boolean(sample, threshold=threshold):  # assess if VEnCode
                yield sample.index.values.tolist()
                i = 0
            else:
                i += 1

    def _heuristic_method_vencode_getter(self):
        """
        Function that searches for a VEnCode in data using the heuristic method.
        """
        breaks = {}  # this next section creates a dictionary to update with how many times each node is cycled
        for item in range(1, self.k):
            breaks["breaker_" + str(item)] = 0
        generator = self._node_based_algorithm(breaks=breaks)
        while True:
            try:
                vencode_list = next(generator)
            except StopIteration:
                break
            if vencode_list:
                vencode_list = [item for sublist in vencode_list for item in sublist]
                for i in gen_util.combinations_from_nested_lists(vencode_list):
                    vencode = self._fill_vencode_list(list(i))
                    yield vencode  # We give the first vencode here
                    if len(i) == self.k:
                        continue
                    for prom_sparse in self._data_not_target.index.values:
                        if prom_sparse in vencode:
                            continue
                        for prom_filled in reversed(vencode):
                            if prom_filled in i:
                                continue
                            vencode_copy = vencode.copy()
                            vencode_copy.remove(prom_filled)
                            vencode_copy.append(prom_sparse)
                            yield vencode_copy
            else:
                break
        yield []

    def _node_based_algorithm(self, promoter=False, counter=1, skip=(), breaks=None, data=None):
        """
        Uses node-based approach to search for vencodes in data.

        Parameters
        ----------
        promoter : str, bool
            Previous promoter name(founder node if first time calling this function).
        counter : int
            Counter is equal to the depth of the current node.
        skip : tuple, list
            The promoters to skip when finding a VEnCode.
        breaks : dict, None
            Dictionary containing keys for the different levels of breaks (one per each combination
        number) and values corresponding to how many times each combination already cycled. dict type
        data : pd.DataFrame
            Data to search for VEnCodes. This method is recursive, and as it makes modifications to the initial
            data frame uses this parameter to feed the next loop.

        Returns
        -------
        list
            The VEnCode, in list type, if the algorithm found one.
        """

        def sort_sparseness(data_):
            """
            Sort data by sum of rows. Descending order of sparseness.

            Parameters
            ----------
            data_ : pd.DataFrame
                Data to sort.
            """
            data_["sum"] = data_.sum(axis=1)  # create a extra column with the sum of 1s for each row (promoter)
            data_.sort_values(["sum"], inplace=True)  # sort promoters based on the previous sum. Descending order.
            data_.drop(["sum"], axis=1, inplace=True)

        vencode_promoters_list = []
        if data is None:
            data_frame = self._data_not_target.copy()
        else:
            data_frame = data
        data_frame.drop(skip, axis=0, inplace=True,
                        errors="ignore")  # drop the promoters previously used to generate vencodes
        if promoter:
            cols = data_frame.loc[promoter] != 0  # create a mask where True marks the celltypes in which the previous
            # node is still expressed
            cols = data_frame.columns[cols]  # apply that mask, selecting the columns that are True
            data_frame = data_frame[cols].drop(promoter,
                                               axis=0)  # apply the selection and take the prom out of the data frame
            vencode_promoters_list.append(promoter)

        nodes = (data_frame == 0).all(
            axis=1)  # Check if any VEnCode - if any other promoter have 0 expression in all cells
        vencode_node_count = np.sum(nodes)  # if any True (VEnCode) the "True" becomes 1 and sum gives num VEnCodes
        if vencode_node_count > 0:
            vencode_list = data_frame[nodes].index.values.tolist()
            vencode_promoters_list.append(vencode_list)
            yield vencode_promoters_list  # found at least one VEnCode so it can return a successful answer

        else:  # if in previous node could not get a definite VEnCode, re-start search with next node
            if self.second_data_object:
                pass
            sort_sparseness(data_frame)
            promoters = data_frame.index.values  # get an array of all the promoters, to cycle
            counter = counter  # counter is defined with previous counter for recursive use of this function
            counter_thresholds = [i for i in range(2, (self.k + 1))]  # set maximum number for counter
            # loop the next area until number of nodes in combination exceeds num of desired proms in comb for VEnCode
            while counter < self.k:
                counter += 1  # updates the counter as it will enter the next node depth
                promoters_in_use = (prom for prom in promoters if prom not in skip)
                for prom in promoters_in_use:  # cycle the promoters
                    # region "early quit if loop is taking too long"
                    if breaks is not None and counter in counter_thresholds:
                        breaker_index = str(counter_thresholds.index(counter) + 1)
                        breaks["breaker_" + breaker_index] += 1
                        # Here, we only test x promoters per node level (self.stop):
                        if breaks["breaker_" + breaker_index] > self._stop:
                            breaks["breaker_" + breaker_index] = 0
                            yield []
                    # endregion "early quit if loop is taking too long"
                    check_if_ven = self._node_based_algorithm(promoter=prom, skip=skip, counter=counter, breaks=breaks,
                                                              data=data_frame)
                    try:
                        vencode_possible = next(check_if_ven)
                    except StopIteration:
                        vencode_possible = False
                        yield []
                    if vencode_possible:
                        vencode_promoters_list.append(vencode_possible)
                        yield vencode_promoters_list
                        vencode_promoters_list = []
            else:
                vencode_promoters_list = []
            yield vencode_promoters_list

    def _fill_vencode_list(self, vencode_list):
        """
        Given an incomplete list of x REs that make up a VEnCode, it fills the list up, up to y VEnCodes (
        y = RE combinations number), based on next sparse REs.

        Parameters
        ----------
        vencode_list : list of str
            A list containing the promoters necessary to establish a vencode.

        Returns
        -------
        list
            A list of y REs that comprise a VEnCode, where y = combinations number.
        """
        assert len(vencode_list) <= self.k, "vencode list len is bigger than wanted RE number"
        if len(vencode_list) == self.k:
            return vencode_list
        for prom in self._data_not_target.index.values:  # next we'll fill the vencode with the top sparse REs
            if prom in vencode_list:
                continue
            vencode_list.append(prom)
            if len(vencode_list) == self.k:
                break
        return vencode_list

    def _e_value_calculator(self, vencode, reps):
        """
        Prepares the data and feeds it to the function that performs the Monte Carlo simulation.

        Parameters
        ----------
        vencode : list of str
            One of the VEnCodes found.
        reps : int
            Number of times each vencode is evaluated to get the average value.

        Returns
        -------
        int
            `E` value, that is, the average number of random changes done to the data that breaks the vencode.
        """

        vencode_data = self._data_not_target.loc[vencode]
        e_value = self.vencode_mc_simulation(vencode_data, reps=reps)
        return e_value

    def _e_value_calculator_two_data_sets(self, vencode, reps):
        """
        Preps the data to be used in Monte Carlo simulation. Used for heuristic2 algorithm.

        Parameters
        ----------
        vencode : list of str
            One of the VEnCodes found.
        reps : int
            Number of times each vencode is evaluated to get the average value.

        Returns
        -------
            `E` value, that is, the average number of random changes done to the data that breaks the vencode.
        """

        vencode_first_data = self._data_not_target.loc[vencode[0]]
        vencode_second_data = self.second_data_object.data.loc[vencode[1]]
        vencode_data = pd.concat([vencode_first_data, vencode_second_data], axis=0)
        e_value = self.vencode_mc_simulation(vencode_data, reps=reps)
        return e_value, vencode_data.shape[0]

    def _heatmap(self, vencode, method="print", interpolation="nearest", path=None, snapshot=None, verbose=True):
        data = self.data.loc[vencode]
        labels = data.index.values
        if snapshot is not None:
            values = eval("data.values[:, -{}:]".format(snapshot))
        else:
            values = data.values
        pylab.imshow(values, interpolation=interpolation, cmap=plt.cm.Reds)
        pylab.yticks(range(values.shape[0]), labels)
        # Print or save to file:
        if not method == "print":
            if path is None:
                path = self._parent_path
            else:
                pass
            file_name = "{}_heat_map".format(self._data_object.target)
            file_path = d_f_handling.check_if_and_makefile(file_name, path=path, file_type=".png")
        else:
            file_path = None
        if method == "write":
            pylab.savefig(file_path, bbox_inches="tight")
            if verbose:
                print("Image stored in {}".format(file_path))
        elif method == "print":
            pylab.show()
        elif method == "both":
            pylab.savefig(file_path, bbox_inches="tight")
            if verbose:
                print("Image stored in {}".format(file_path))
            pylab.show()
        else:
            raise AttributeError("method argument is not recognized")

    def _e_value_normalizer(self, e_value_raw, k=None):
        """
        Normalizes the e-value to account for the variance in the number of celltypes and regulatory elements in the
        data sets.

        Parameters
        ----------
        e_value_raw : int
            Value to normalize

        Returns
        -------
            Normalized e-value.
        """
        if k is None:
            k = self.k

        coefs = {"a": -164054.1, "b": 0.9998811, "c": 0.000006088948, "d": 1.00051, "m": 0.9527, "e": -0.1131}
        e_value_expected = (coefs["m"] * k + coefs["e"]) * self._data_not_target.shape[1] ** (
                coefs["d"] + ((coefs["a"] - coefs["d"]) / (1 + (k / coefs["c"]) ** coefs["b"])))
        e_value_norm = (e_value_raw / e_value_expected) * 100
        if e_value_norm < 100:
            return e_value_norm
        else:
            return 100

    @staticmethod
    def _assess_vencode_one_zero_boolean(sample, threshold=0):
        """
        Returns True if sample represents a VEnCodes for a celltype not in "sample". It assumes VEnCodes when all
        other celltypes have at least one promoter not expressing. It's the quickest VEnCode assessing algorithm.
        """
        if threshold == 0:
            assess_if_vencode = np.any(sample == 0, axis=0)  # list of True if column has any 0
        elif threshold > 0:
            assess_if_vencode = np.any(sample <= threshold, axis=0)
        else:
            raise ValueError("Threshold for VEnCode assessment is not valid.")
        return all(assess_if_vencode)  # if all columns are True (contain at least one 0), then is VEn

    def _export_e_values(self, path=None, verbose=True):
        """
        Call this method to export `e` values to a .csv file.
        Use path to define a specific path for the file. (must be a complete path)

        Parameters
        ----------
        path : str
            Complete path to store the file.
        verbose : bool
            Either to allow the function to print messages to console (`True`), or not (`False`).
        """
        if not self.e_values:
            self.determine_e_values()
        if path is None:
            path = self._parent_path
        file_name = "{}_evalues".format(self._data_object.target)
        file_name = d_f_handling.str_replace_multi(
            file_name, {":": "-", "*": "-", "?": "-", "<": "-", ">": "-", "/": "-"})
        file_path = d_f_handling.check_if_and_makefile(file_name, path=path, file_type=".csv")
        d_f_handling.write_one_value_dict_to_csv(file_path, self.e_values)
        if verbose:
            print("File stored in: {}".format(file_path))

    def _export_e_values_tpp(self, path=None, verbose=True):
        pass

    def _export_vencodes(self, path=None, verbose=True):
        """
        Call this method to export VEnCodes to a .csv file.
        Use path to define a specific path for the file. (must be a complete path)

        Parameters
        ----------
        path : str
            Complete path to store the file.
        verbose : bool
            Either to allow the function to print messages to console (`True`), or not (`False`).
        """
        for vencode in self.vencodes:
            file_name = "{}_vencode".format(self._data_object.target)
            file_name = d_f_handling.str_replace_multi(
                file_name, {":": "-", "*": "-", "?": "-", "<": "-", ">": "-", "/": "-"})
            file_path = d_f_handling.check_if_and_makefile(file_name, path=path, file_type=".csv")
            self.data.loc[vencode].to_csv(file_path, sep=';')
            if verbose:
                print("File stored in {}".format(file_path))


class DataTpmFantom5Validated(DataTpmFantom5):
    """
    This class provides methods to develop a data set with chromosome coordinates intercepted
    with those of an external data set supplied in `validate_with`, which we call validated regulatory elements.

    How to use: After initializing, filter data with validated REs by calling the `select_validated` method.
    """

    def __init__(self, validate_with, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validate_with = validate_with

    def select_validated(self):
        """
        Main method to filter the REs in the data, leaving in the data only those that match the external data set.
        """
        df_range = self._regulatory_elements_range()
        self._interception(df_range, self.validate_with.data, self.data)

    def merge_external_cell_type(self, cell_type):
        df_range = self._regulatory_elements_range()
        self.data = self._interception(df_range, self.validate_with.data, self.data)
        validate_with = self._interception(self.validate_with.data, df_range, self.validate_with.data)
        if self.data.shape[0] == validate_with.shape[0]:
            validate_with.index = self.data.index
            self.data[cell_type] = validate_with["tpm"]
        else:
            self.data[cell_type] = pd.Series(data=[50] * len(self.data.index), index=self.data.index)

    def _interception(self, data1, data2, data_updated):
        mask = self._mask(data1, data2)
        data_updated = data_updated.loc[mask]
        return data_updated

    def _regulatory_elements_range(self):
        df_temp = pd.DataFrame()
        df_temp["Id"] = self.data.index
        df_temp[["Chromosome", "temp"]] = df_temp.Id.str.split(":", expand=True)
        df_temp[["Start", "End"]] = df_temp.temp.str.split("-", expand=True)
        df_temp = df_temp[["Chromosome", "Start", "End"]]
        pd_util.columns_to_numeric(df_temp, "Start", "End")
        df_temp["range"] = [[row.Start, row.End] for index, row in df_temp.iterrows()]
        return df_temp

    @staticmethod
    def _mask(df, df2):
        mask = []
        for index, row in df.iterrows():
            range1 = row.range
            data2_filter_chr = df2[df2["Chromosome"] == row.iloc[0]]
            range2_list = data2_filter_chr["range"].tolist()
            switch = False
            for range2 in range2_list:
                condition = gen_util.partial_subset_of_span(range1, range2)
                if condition:
                    mask.append(True)
                    switch = True
                    break
            if not switch:
                mask.append(False)
        return mask
