"""
test_internals.py: File containing a set of unittest.TestCase runnable tests for the classes and functions
in the internals.py file.
"""

import os
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

file_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(file_dir)

from VEnCode import internals
from VEnCode import common_variables as cv
from VEnCode.utils import dir_and_file_handling as dh


# First come the tests for the data set container, DataTpm:
class DataTpmTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Sets-up class variables to be used in the tests.
        """
        cls.celltype_analyse = "celltypetarget"
        cls.replicate_suffix = "_donor"
        cls.data1 = cv.expression_data1
        cls.data2 = cv.expression_data2


class FilenameHandler(DataTpmTest):
    @classmethod
    def setUpClass(cls):
        """ Sets-up class variables to be used in the tests. """
        super().setUpClass()
        cls.path = os.path.join(str(Path(__file__).parents[1]), "Files")

    def test_filename(self):
        data_tpm = internals.DataTpm(file=self.data1, files_path="test", nrows=4)
        data_tpm.load_data()
        self.assertEqual(os.path.isfile(data_tpm._file_path), True)

    def test_files_path(self):
        data_tpm_path_div = internals.DataTpm(file=self.data1, files_path=self.path)
        data_tpm_path_div.load_data()
        self.assertEqual(os.path.isfile(data_tpm_path_div._file_path), True)

    def test_file_full(self):
        data_tpm_path_full = internals.DataTpm(file=os.path.join(self.path, self.data1), files_path=None)
        data_tpm_path_full.load_data()
        self.assertEqual(os.path.isfile(data_tpm_path_full._file_path), True)

    def test_data_frame_input(self):
        df = pd.DataFrame(data=[[0, 1, 0], [1, 1, 0]], index=["first", "second"], columns=["A", "B", "C"])
        data_tpm = internals.DataTpm(file=df, files_path=None)
        data_tpm.load_data()
        self.assertEqual(data_tpm._file_path, None)


class DataTest(DataTpmTest):
    @classmethod
    def setUpClass(cls):
        """ Sets-up class variables to be used in the tests. """
        super().setUpClass()
        cls.data_tpm = internals.DataTpm(file=cls.data1, files_path="test", sep=";")
        cls.data_tpm.load_data()
        cls.data_tpm_4row = internals.DataTpm(file=cls.data1, files_path="test", sep=";", nrows=4)
        cls.data_tpm_4row.load_data()

    def test_open(self):
        self.assertEqual(isinstance(self.data_tpm.data, pd.DataFrame), True)

    def test_rows(self):
        self.assertEqual(69, self.data_tpm.shape[0])

    def test_nrows(self):
        self.assertEqual(4, self.data_tpm_4row.shape[0])

    def test_cols(self):
        self.assertEqual(28, self.data_tpm.shape[1])

    def test_row_names(self):
        expected = ["chr10:100027943..100027958,-", "chr10:100174900..100174956,-",
                    "chr12:109548967..109549024,+", "chr12:109554241..109554255,+"]
        self.assertEqual(expected, self.data_tpm_4row.data.index.values.tolist())

    def test_col_names(self):
        expected = ["celltypetarget_donor1", "celltypetarget_donor2", "celltypetarget_donor3"]
        self.assertCountEqual(expected, self.data_tpm.data.columns[:3])


class FromDataFrameTest(DataTpmTest):
    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        df = pd.DataFrame(data=[[0, 1, 0], [1, 1, 0]], index=["first", "second"], columns=["A", "B", "C"])
        self.data_tpm = internals.DataTpm(file=df)
        self.data_tpm.load_data()

    def test_open(self):
        self.assertEqual(isinstance(self.data_tpm.data, pd.DataFrame), True)

    def test_rows(self):
        self.assertEqual(2, self.data_tpm.shape[0])

    def test_cols(self):
        self.assertEqual(3, self.data_tpm.shape[1])

    def test_row_names(self):
        expected = ["first", "second"]
        self.assertEqual(expected, self.data_tpm.data.index.values.tolist())

    def test_col_names(self):
        expected = ["A", "B", "C"]
        self.assertCountEqual(expected, self.data_tpm.data.columns)


class MakeCelltypeSpecificTest(DataTpmTest):
    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.target_dict = {self.celltype_analyse: {'celltypetarget_donor1', 'celltypetarget_donor2',
                                                    'celltypetarget_donor3'}}
        self.data_tpm = internals.DataTpm(file=self.data1, files_path="test", sep=";")
        self.data_tpm.load_data()

    def test_target_replicates(self):
        self.data_tpm.make_data_celltype_specific(self.celltype_analyse, replicates=True)
        expected = {'celltypetarget_donor1', 'celltypetarget_donor2', 'celltypetarget_donor3'}
        self.assertEqual(expected, set(self.data_tpm.target_replicates["celltypetarget"]))

    def test_target(self):
        self.data_tpm.make_data_celltype_specific(self.celltype_analyse, replicates=True)
        expected = 'celltypetarget'
        self.assertEqual(expected, self.data_tpm.target)

    def test_target_replicates_dict(self):
        self.data_tpm.make_data_celltype_specific(self.target_dict, replicates=True)
        expected = {'celltypetarget_donor1', 'celltypetarget_donor2', 'celltypetarget_donor3'}
        self.assertEqual(expected, set(self.data_tpm.target_replicates["celltypetarget"]))

    def test_target_dict(self):
        self.data_tpm.make_data_celltype_specific(self.target_dict, replicates=True)
        expected = 'celltypetarget'
        self.assertEqual(expected, self.data_tpm.target)


class MakeCelltypeSpecificFromDfTest(DataTpmTest):
    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        df = pd.DataFrame(data=[[0, 1, 0], [1, 1, 0]], index=["first", "second"], columns=["A", "A_1", "C"])
        self.data_tpm = internals.DataTpm(file=df)
        self.data_tpm.load_data()
        self.data_tpm.make_data_celltype_specific("A", replicates=True)

    def test_target_replicates(self):
        expected = {"A", "A_1"}
        self.assertEqual(expected, set(self.data_tpm.target_replicates["A"]))

    def test_target(self):
        expected = "A"
        self.assertEqual(expected, self.data_tpm.target)


class ReplicatesFalseTest(DataTpmTest):
    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.data_tpm = internals.DataTpm(file=self.data1, files_path="test", sep=";")
        self.data_tpm.load_data()
        self.data_tpm.make_data_celltype_specific(self.celltype_analyse, replicates=False)

    def test_target_replicates(self):
        expected = 'celltypetarget'
        self.assertEqual(expected, self.data_tpm.target_replicates["celltypetarget"])

    def test_target(self):
        expected = 'celltypetarget'
        self.assertEqual(expected, self.data_tpm.target)


class MergeReplicatesTest(DataTpmTest):
    COLUMN_NAMES = ['celltypetarget', 'celltype2', 'celltype3', 'celltype4', 'celltype5', 'celltype6',
                    'celltype7', 'celltype8', 'celltype9', 'celltype10', 'celltype11', 'celltype12']


class ReplicateSuffixTest(MergeReplicatesTest):
    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.data_tpm = internals.DataTpm(file=self.data1, files_path="test", sep=";")
        self.data_tpm.load_data()

    def test_shape(self):
        self.data_tpm.merge_replicates(replicate_suffix=self.replicate_suffix)
        expected = (69, 12)
        self.assertEqual(expected, self.data_tpm.shape)

    def test_average(self):
        expected = np.mean(self.data_tpm.data.iloc[0, 0:3].values)
        self.data_tpm.merge_replicates(replicate_suffix=self.replicate_suffix)
        self.assertAlmostEqual(expected, self.data_tpm.data.iloc[0, 0])

    def test_column_names(self):
        self.data_tpm.merge_replicates(replicate_suffix=self.replicate_suffix)
        self.assertCountEqual(self.COLUMN_NAMES, self.data_tpm.data.columns)


class CelltypeListTest(MergeReplicatesTest):
    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.data_tpm = internals.DataTpm(file=self.data1, files_path="test", sep=";")
        self.data_tpm.load_data()
        self.celltype_list = ['celltypetarget', 'celltype2', 'celltype3', 'celltype4', 'celltype5', 'celltype6',
                              'celltype7', 'celltype8', 'celltype9', 'celltype10', 'celltype11', 'celltype12']

    def test_shape(self):
        self.data_tpm.merge_replicates(celltype_list=self.celltype_list)
        expected = (69, 12)
        self.assertEqual(expected, self.data_tpm.shape)

    def test_average(self):
        expected = np.mean(self.data_tpm.data.iloc[0, 0:3].values)
        self.data_tpm.merge_replicates(celltype_list=self.celltype_list)
        self.assertAlmostEqual(expected, self.data_tpm.data.iloc[0, 0])

    def test_column_names(self):
        self.data_tpm.merge_replicates(celltype_list=self.celltype_list)
        self.assertCountEqual(self.COLUMN_NAMES, self.data_tpm.data.columns)


class ReplicateDictTest(MergeReplicatesTest):
    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.data_tpm = internals.DataTpm(file=self.data1, files_path="test", sep=";")
        self.data_tpm.load_data()
        self.replicate_dict = {
            'celltypetarget': ['celltypetarget_donor1', 'celltypetarget_donor2', 'celltypetarget_donor3'],
            'celltype2': ['celltype2_donor1', 'celltype2_donor2'],
            'celltype3': ['celltype3_donor1'],
            'celltype4': ['celltype4_donor1', 'celltype4_donor2', 'celltype4_donor3'],
            'celltype5': ['celltype5_donor1', 'celltype5_donor2'],
            'celltype6': ['celltype6_donor1', 'celltype6_donor2'],
            'celltype7': ['celltype7_donor1'],
            'celltype8': ['celltype8_donor1', 'celltype8_donor2', 'celltype8_donor3'],
            'celltype9': ['celltype9_donor1', 'celltype9_donor2', 'celltype9_donor3', 'celltype9_donor4',
                          'celltype9_donor5'],
            'celltype10': ['celltype10_donor1', 'celltype10_donor2'],
            'celltype11': ['celltype11_donor1', 'celltype11_donor2'],
            'celltype12': ['celltype12_donor1', 'celltype12_donor2']
        }

    def test_shape(self):
        self.data_tpm.merge_replicates(replicate_dict=self.replicate_dict)
        expected = (69, 12)
        self.assertEqual(expected, self.data_tpm.shape)

    def test_average(self):
        expected = np.mean(self.data_tpm.data.iloc[0, 0:3].values)
        self.data_tpm.merge_replicates(replicate_dict=self.replicate_dict)
        self.assertAlmostEqual(expected, self.data_tpm.data.iloc[0, 0])

    def test_column_names(self):
        self.data_tpm.merge_replicates(replicate_dict=self.replicate_dict)
        self.assertCountEqual(self.COLUMN_NAMES, self.data_tpm.data.columns)


class NotIncludeTest(MergeReplicatesTest):
    NOT_INCLUDE = {"celltypetarget": ["donor1"], "celltype9": ["donor3", "5"]}

    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.data_tpm = internals.DataTpm(file=self.data1, files_path="test", sep=";")
        self.data_tpm.load_data()

    def test_shape(self):
        self.data_tpm.merge_replicates(replicate_suffix=self.replicate_suffix, not_include=self.NOT_INCLUDE)
        expected = (69, 12)
        self.assertEqual(expected, self.data_tpm.shape)

    def test_average_target(self):
        expected = np.mean(self.data_tpm.data.iloc[0, 1:3].values)
        self.data_tpm.merge_replicates(replicate_suffix=self.replicate_suffix, not_include=self.NOT_INCLUDE)
        self.assertAlmostEqual(expected, self.data_tpm.data.iloc[0, 0])

    def test_average_9(self):
        ctp_9 = self.data_tpm.data.iloc[1, 17:21].values
        ctp_9 = np.delete(ctp_9, [2, 4])
        expected = np.mean(ctp_9)
        self.data_tpm.merge_replicates(replicate_suffix=self.replicate_suffix, not_include=self.NOT_INCLUDE)
        self.assertAlmostEqual(expected, self.data_tpm.data.iloc[1, 8])

    def test_column_names(self):
        self.data_tpm.merge_replicates(replicate_suffix=self.replicate_suffix, not_include=self.NOT_INCLUDE)
        self.assertCountEqual(self.COLUMN_NAMES, self.data_tpm.data.columns)


class ExcludeTargetTest(MergeReplicatesTest):
    COLUMN_NAMES = ['celltypetarget_donor1', 'celltypetarget_donor2', 'celltypetarget_donor3', 'celltype2', 'celltype3',
                    'celltype4', 'celltype5', 'celltype6', 'celltype7', 'celltype8', 'celltype9', 'celltype10',
                    'celltype11', 'celltype12']

    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.data_tpm = internals.DataTpm(file=self.data1, files_path="test", sep=";")
        self.data_tpm.load_data()
        self.data_tpm.make_data_celltype_specific(self.celltype_analyse)

    def test_shape(self):
        self.data_tpm.merge_replicates(replicate_suffix=self.replicate_suffix, exclude_target=True)
        expected = (69, 14)
        self.assertEqual(expected, self.data_tpm.shape)

    def test_average(self):
        before = np.mean(self.data_tpm.data.iloc[0, 0:3].values)
        self.data_tpm.merge_replicates(replicate_suffix=self.replicate_suffix, exclude_target=True)
        after = np.mean(
            self.data_tpm.data[
                ['celltypetarget_donor1', 'celltypetarget_donor2', 'celltypetarget_donor3']].iloc[0].values)
        self.assertAlmostEqual(before, after)

    def test_column_names(self):
        self.data_tpm.merge_replicates(replicate_suffix=self.replicate_suffix, exclude_target=True)
        self.assertCountEqual(self.COLUMN_NAMES, self.data_tpm.data.columns)


class CopyTest(DataTpmTest):
    @classmethod
    def setUpClass(cls):
        """ Sets-up class variables to be used in the tests. """
        super().setUpClass()
        cls.data_tpm = internals.DataTpm(file=cls.data1, files_path="test", sep=";")
        cls.data_tpm.load_data()
        cls.data_tpm.make_data_celltype_specific(cls.celltype_analyse)

    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.data_tpm2 = self.data_tpm.copy(deep=False)
        self.data_tpm3 = self.data_tpm.copy(deep=True)

    def test_shallow_creation(self):
        self.assertEqual(self.data_tpm, self.data_tpm2)

    def test_shallow_equal_data(self):
        condition = self.data_tpm.data.equals(self.data_tpm2.data)
        self.assertTrue(condition)

    def test_deep_creation(self):
        self.assertEqual(self.data_tpm, self.data_tpm3)

    def test_deep_equal_data(self):
        condition = self.data_tpm.data.equals(self.data_tpm3.data)
        self.assertTrue(condition)

    def test_change_arg_shallow(self):
        self.data_tpm2.target = "test"
        self.assertNotEqual(self.data_tpm, self.data_tpm2)

    def test_change_arg_deep(self):
        self.data_tpm3.target = "test"
        self.assertNotEqual(self.data_tpm, self.data_tpm3)

    def test_change_data_shallow(self):
        self.data_tpm2.data.iloc[1, 1] = "test"
        self.assertEqual(self.data_tpm, self.data_tpm2)

    def test_change_data_deep(self):
        self.data_tpm3.data.iloc[1, 1] = "test"
        self.assertNotEqual(self.data_tpm, self.data_tpm3)


class EqualTest(DataTpmTest):
    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.data_tpm = internals.DataTpm(file=self.data1, files_path="test", sep=";")
        self.data_tpm.load_data()
        self.data_tpm.make_data_celltype_specific(self.celltype_analyse)

    def test_unequal_arg(self):
        data_tpm2 = self.data_tpm.copy(deep=True)
        data_tpm2.target = "test"
        condition = self.data_tpm == data_tpm2
        self.assertFalse(condition)

    def test_unequal_data(self):
        data_tpm3 = self.data_tpm.copy(deep=True)
        data_tpm3.data.iloc[0, 0] = 3
        condition = self.data_tpm == data_tpm3
        self.assertFalse(condition)

    def test_equal_data(self):
        data_tpm4 = self.data_tpm.copy(deep=True)
        condition = self.data_tpm == data_tpm4
        self.assertTrue(condition)


class SortColumnsTest(DataTpmTest):
    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.data_tpm = internals.DataTpm(file=self.data1, files_path="test", sep=";")
        self.data_tpm.load_data()
        self.data_tpm.make_data_celltype_specific(self.celltype_analyse)
        self.data_tpm.merge_replicates(replicate_suffix=self.replicate_suffix)
        self.cols = self.data_tpm.data.columns.tolist()

    def test_sort_alphabetically(self):
        self.data_tpm.sort_columns()
        cols = self.data_tpm.data.columns.tolist()
        for i in (self.cols, sorted(self.cols, key=str.lower)):
            condition = (i == cols)
            with self.subTest(i=i):
                if i == self.cols:
                    self.assertFalse(condition)
                else:
                    self.assertTrue(condition)

    def test_values_remain(self):
        before = self.data_tpm.data[self.celltype_analyse].values.tolist()
        self.data_tpm.sort_columns()
        after = self.data_tpm.data[self.celltype_analyse].values.tolist()
        self.assertEqual(before, after)

    def test_sort_to_first(self):
        celltype = "celltype5"
        before = self.data_tpm.data.columns.tolist().index(celltype)
        self.data_tpm.sort_columns(col_to_shift=celltype, pos_to_move=0)
        after = self.data_tpm.data.columns.tolist().index(celltype)
        condition = (before != after) and (after == 0)
        self.assertTrue(condition)


class FilterByTargetTest(DataTpmTest):
    def setUp(self):
        """ Sets-up class variables to be used in the tests. """
        self.data_tpm = internals.DataTpm(file=self.data1, files_path="test", sep=";")
        self.data_tpm.load_data()
        self.data_tpm.make_data_celltype_specific(self.celltype_analyse)

    def test_above_threshold(self, threshold=1):
        _temp = self.data_tpm.data[self.data_tpm.target_replicates[self.celltype_analyse]].values.tolist()
        expected = [i for i in _temp if (all(f >= threshold for f in i))]
        self.data_tpm.filter_by_target_celltype_activity(threshold=threshold, binarize=False)
        to_test = self.data_tpm.data[self.data_tpm.target_replicates[self.celltype_analyse]].values.tolist()
        self.assertCountEqual(expected, to_test)

    def test_replicates(self, threshold=2):
        _temp = self.data_tpm.data[self.data_tpm.target_replicates[self.celltype_analyse][:2]].values.tolist()
        expected = [i for i in _temp if (all(f >= threshold for f in i))]
        replicates = ["celltypetarget_donor1", "celltypetarget_donor2"]
        self.data_tpm.filter_by_target_celltype_activity(threshold=threshold, binarize=False, replicates=replicates)
        to_test = self.data_tpm.data[self.data_tpm.target_replicates[self.celltype_analyse][:2]].values.tolist()
        self.assertCountEqual(expected, to_test)

    def test_binarize(self, threshold=1):
        self.data_tpm.filter_by_target_celltype_activity(threshold=threshold, binarize=True)
        values = np.unique(self.data_tpm.data[self.data_tpm.target_replicates[self.celltype_analyse]].values)
        self.assertCountEqual([1], values)

    def test_merged_data(self, threshold=1):
        self.data_tpm.merge_replicates(replicate_suffix=self.replicate_suffix)
        _temp = self.data_tpm.data[self.celltype_analyse].values.tolist()
        expected = [i for i in _temp if i >= threshold]
        self.data_tpm.filter_by_target_celltype_activity(threshold=threshold, binarize=False)
        to_test = self.data_tpm.data[self.data_tpm.target_replicates[self.celltype_analyse]].values.tolist()
        self.assertCountEqual(expected, to_test)


class DefineNonTargetCelltypesInactivityTest(DataTpmTest):
    @classmethod
    def setUpClass(cls):
        """ Sets-up class variables to be used in the tests. """
        super().setUpClass()
        cls.data_tpm = internals.DataTpm(file=cls.data1, files_path="test", sep=";")
        cls.data_tpm.load_data()
        cls.data_tpm.make_data_celltype_specific(cls.celltype_analyse)

    def test_if_int_promoters(self):
        self.data_tpm.merge_replicates(replicate_suffix=self.replicate_suffix, exclude_target=False)
        self.data_tpm.define_non_target_celltypes_inactivity(threshold=0.3)
        self.assertFalse([True for item in self.data_tpm.data[
            self.data_tpm.data.columns[1:]].dtypes if item != np.int64])

    def test_no_bigger_than_one(self):
        self.data_tpm.merge_replicates(replicate_suffix=self.replicate_suffix, exclude_target=False)
        self.data_tpm.define_non_target_celltypes_inactivity(threshold=0.3)
        non_target_data = self.data_tpm.data[self.data_tpm.data.columns[1:]]
        result = pd.eval("non_target_data.values > 1")
        self.assertFalse(np.any(result))

    def test_non_merged_data(self):
        self.data_tpm.define_non_target_celltypes_inactivity(threshold=0.3)
        non_target_data = self.data_tpm.data[self.data_tpm.data.columns[3:]]
        result = pd.eval("non_target_data.values > 1")
        self.assertFalse(np.any(result))


class FilterBySparsenessTest(DataTpmTest):
    @classmethod
    def setUpClass(cls):
        """ Sets-up class variables to be used in the tests. """
        super().setUpClass()
        cls.data_tpm = internals.DataTpm(file=cls.data1, files_path="test", sep=";")
        cls.data_tpm.load_data()
        cls.data_tpm.make_data_celltype_specific(cls.celltype_analyse)
        cls.data_tpm.merge_replicates(replicate_suffix=cls.replicate_suffix, exclude_target=False)


class FilterBySparsenessMainTest(FilterBySparsenessTest):
    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.data_tpm.filter_by_reg_element_sparseness(threshold=50, min_re=10, exclude_target=True)

    def test_ctp_still_in_df(self):
        condition = all([x for x in self.data_tpm.target_replicates[
            self.celltype_analyse] if x in self.data_tpm.data.columns.tolist()])
        self.assertTrue(condition)

    def test_number_cols(self):
        self.assertEqual(28, self.data_tpm.data.shape[0])

    def test_percentile_col_not_in_df(self):
        column = "Percentile_col"
        condition = column in self.data_tpm.data.columns.tolist()
        self.assertFalse(condition)


class MinReTest(FilterBySparsenessTest):
    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.data_tpm.filter_by_reg_element_sparseness(threshold=50, min_re=40, exclude_target=True)

    def test_ctp_still_in_df(self):
        condition = all([x for x in self.data_tpm.target_replicates[
            self.celltype_analyse] if x in self.data_tpm.data.columns.tolist()])
        self.assertTrue(condition)

    def test_number_cols(self):
        self.assertEqual(40, self.data_tpm.data.shape[0])

    def test_percentile_col_not_in_df(self):
        column = "Percentile_col"
        condition = column in self.data_tpm.data.columns.tolist()
        self.assertFalse(condition)


class NotExcludeTargetTest(FilterBySparsenessTest):
    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.data_tpm.filter_by_reg_element_sparseness(threshold=50, min_re=10, exclude_target=False)

    def test_ctp_still_in_df(self):
        condition = all([x for x in self.data_tpm.target_replicates[
            self.celltype_analyse] if x in self.data_tpm.data.columns.tolist()])
        self.assertTrue(condition)

    def test_number_cols(self):
        self.assertEqual(22, self.data_tpm.data.shape[0])

    def test_percentile_col_not_in_df(self):
        column = "Percentile_col"
        condition = column in self.data_tpm.data.columns.tolist()
        self.assertFalse(condition)


class SortSparsenessTest(DataTpmTest):
    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.data_tpm = internals.DataTpm(file=self.data1, files_path="test", sep=";")
        self.data_tpm.load_data()
        self.data_tpm.make_data_celltype_specific(self.celltype_analyse)
        self.data_tpm.merge_replicates(replicate_suffix=self.replicate_suffix, exclude_target=False)

    def test_sort_exclude_target(self):
        self.data_tpm.sort_sparseness(exclude_target=True)
        self.data_tpm.data["Sum"] = self.data_tpm.data.drop(self.celltype_analyse, axis=1).sum(axis=1)
        counter = 0
        previous_row = None
        for row_sum in self.data_tpm.data["Sum"].values:
            if previous_row is None or row_sum >= previous_row:
                counter += 1
                previous_row = row_sum
        self.assertEqual(counter, 69)

    def test_sort_not_exclude_target(self):
        self.data_tpm.sort_sparseness(exclude_target=False)
        self.data_tpm.data["Sum"] = self.data_tpm.data.sum(axis=1)
        counter = 0
        previous_row = None
        for row_sum in self.data_tpm.data["Sum"].values:
            if previous_row is None or row_sum >= previous_row:
                counter += 1
                previous_row = row_sum
        self.assertEqual(counter, 69)


class RemoveCelltypeTest(DataTpmTest):
    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.data_tpm = internals.DataTpm(file=self.data1, files_path="test", sep=";")
        self.data_tpm.load_data()
        self.data_tpm.make_data_celltype_specific(self.celltype_analyse)

    def test_remove_celltype(self):
        self.data_tpm.remove_celltype("celltype2_donor2")
        self.assertNotIn("celltype2_donor2", self.data_tpm.data.columns)

    def test_remove_list_celltypes(self):
        self.data_tpm.remove_celltype(["celltype2_donor1", "celltype2_donor2"])
        with self.assertRaises(KeyError):
            test = self.data_tpm.data[["celltype2_donor1", "celltype2_donor2"]]

    def test_incorrect_celltype(self):
        self.data_tpm.remove_celltype("cellype2_dr2")
        condition = not self.data_tpm.data["celltype2_donor2"].empty
        self.assertTrue(condition)


class RemoveElementTest(DataTpmTest):
    def setUp(self):
        """ Sets-up  variables to be used in the tests. """
        self.data_tpm = internals.DataTpm(file=self.data1, files_path="test", sep=";")
        self.data_tpm.load_data()
        self.data_tpm.make_data_celltype_specific(self.celltype_analyse)
        self.elements = ['chr10:100027943..100027958,-', 'chr10:100174900..100174956,-']

    def test_remove_elements(self):
        self.data_tpm.remove_element(self.elements)
        with self.assertRaises(KeyError):
            test = self.data_tpm.data.loc[self.elements]

    def test_incorrect_elements(self):
        self.data_tpm.remove_celltype("test incorrect RE")
        condition = not self.data_tpm.data.loc[self.elements].empty
        self.assertTrue(condition)


class AddCelltypeTest(DataTpmTest):
    @classmethod
    def setUpClass(cls):
        """ Sets-up class variables to be used in the tests. """
        super().setUpClass()
        # main data
        cls.data_tpm = internals.DataTpm(file=cls.data1, files_path="test", sep=";")
        cls.data_tpm.load_data()
        # copy for use in tests
        cls.data_tpm_added = cls.data_tpm.copy(deep=True)
        # adding a celltype
        cls.data_tpm_added.add_celltype(celltypes=["celltype13_donor1", "celltype13_donor2"],
                                        data_from=cls.data2, files_path="test", sep=";")

    def test_adding(self):
        expected = ["celltype13_donor1", "celltype13_donor2"]
        for i in expected:
            with self.subTest(i=i):
                self.assertIn(i, self.data_tpm_added.data.columns)

    def test_celltype_only_added(self):
        expected_difference = ["celltype13_donor1", "celltype13_donor2"]
        difference = set(self.data_tpm_added.data.columns.values) - set(self.data_tpm.data.columns.values)
        self.assertCountEqual(expected_difference, difference)

    def test_any_nan(self):
        self.assertFalse(self.data_tpm_added.data.isnull().values.any())

    def test_adding_back_primary(self):
        data_tpm_rescue = self.data_tpm.copy(deep=True)
        # adding a celltype after having removed from the data set
        data_tpm_rescue.remove_celltype("celltype3_donor1")
        data_tpm_rescue.add_celltype(celltypes="celltype3_donor1", data_from=self.data_tpm)
        self.data_tpm.sort_columns()
        data_tpm_rescue.sort_columns()
        self.assertEqual(self.data_tpm, data_tpm_rescue)


class DropTargetTest(DataTpmTest):
    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.data_tpm = internals.DataTpm(file=self.data1, files_path="test", sep=";")
        self.data_tpm.load_data()
        self.data_tpm.make_data_celltype_specific(self.celltype_analyse)

    def test_drop(self):
        data_test = self.data_tpm.drop_target_ctp(inplace=False)
        difference = set(self.data_tpm.data.columns.values) - set(data_test.columns.values)
        self.assertCountEqual(self.data_tpm.target_replicates[self.data_tpm.target], difference)

    def test_merged_drop(self):
        self.data_tpm.merge_replicates(replicate_suffix=self.replicate_suffix, exclude_target=False)
        data_test = self.data_tpm.drop_target_ctp(inplace=False)
        difference = set(self.data_tpm.data.columns.values) - set(data_test.columns.values)
        self.assertCountEqual({self.celltype_analyse}, difference)

    def test_inplace_drop(self):
        self.data_tpm.merge_replicates(replicate_suffix=self.replicate_suffix, exclude_target=False)
        self.data_tpm.drop_target_ctp(inplace=True)
        self.assertNotIn(self.celltype_analyse, self.data_tpm.data.columns)


class BinarizeDataTest(DataTpmTest):
    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.data_tpm = internals.DataTpm(file=self.data1, files_path="test", sep=";")
        self.data_tpm.load_data()
        self.data_tpm.binarize_data(threshold=0)

    def test_binarize_data(self):
        values = np.unique(self.data_tpm.data.values)
        self.assertCountEqual([0, 1], values)


class ToCsvTest(DataTpmTest):
    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.data_tpm = internals.DataTpm(file=self.data1, files_path="test", sep=";")
        self.data_tpm.load_data()
        self.data_tpm.binarize_data(threshold=0)

    def test_to_csv(self):
        self.data_tpm.to_csv("test.csv")
        data_exported = pd.read_csv("test.csv", index_col=0, engine="python")
        condition = data_exported.equals(self.data_tpm.data)
        self.assertTrue(condition)
        os.remove("test.csv")


# Here we start testing the FANTOM5 CAGE-seq specific methods:
class DataTpmFantom5Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """ Sets-up class variables to be used in the tests. """
        cls.celltypes_total = ["Hepatocyte", "Adipocyte - breast"]
        cls.celltype_analyse = "Adipocyte - breast"


class FilenameHandlerFantom5Test(DataTpmFantom5Test):

    def test_filename(self):
        file_type = cv.test_promoter_file_name
        database = internals.DataTpmFantom5(file=file_type, nrows=4)
        self.assertEqual(os.path.isfile(database._file_path), True)

    def test_parsed(self):
        file_type = "parsed"
        database = internals.DataTpmFantom5(file=file_type, nrows=4)
        database.make_data_celltype_specific(self.celltype_analyse)
        self.assertEqual(os.path.isfile(database._file_path), True)


class RawDataFantom5Test(DataTpmFantom5Test):
    @classmethod
    def setUpClass(cls):
        """ Sets-up class variables to be used in the tests. """
        super().setUpClass()
        cls.database_promoters = internals.DataTpmFantom5(file=cv.test_promoter_file_name, nrows=4, keep_raw=True)
        cls.database_enhancers = internals.DataTpmFantom5(file=cv.test_enhancer_file_name, nrows=4, keep_raw=True,
                                                          data_type="enhancers")

    def test_open(self):
        self.assertEqual(isinstance(self.database_promoters.raw_data, pd.DataFrame), True)

    def test_open_enhancers(self):
        self.assertEqual(isinstance(self.database_enhancers.raw_data, pd.DataFrame), True)

    def test_nrows(self):
        self.assertEqual(self.database_promoters.raw_data.shape[0], 4)

    def test_nrows_enhancers(self):
        self.assertEqual(self.database_enhancers.raw_data.shape[0], 4)

    def test_ncols(self):
        self.assertEqual(self.database_promoters.raw_data.shape[1], 1829)

    def test_ncols_enhancers(self):
        self.assertEqual(self.database_enhancers.raw_data.shape[1], 1827)

    def test_row_names(self):
        expected = ["chr10:100013403..100013414,-", "chr10:100027943..100027958,-",
                    "chr10:100076685..100076699,+", "chr10:100150910..100150935,-"]
        self.assertEqual(self.database_promoters.raw_data.index.values.tolist(), expected)

    def test_row_names_enhancers(self):
        expected = ['chr1:839741-840250', 'chr1:840753-841210', 'chr1:845485-845678', 'chr1:855764-856157']
        self.assertEqual(self.database_enhancers.raw_data.index.values.tolist(), expected)

    def test_col_names_enhancers(self):
        """ Tests if all column tags were converted to proper celltype names"""
        for column_name in self.database_enhancers.raw_data.columns:
            self.assertIn(column_name, self.database_enhancers.names_db["celltypes"].values)


class DataNotParsedFantom5Test(DataTpmFantom5Test):
    @classmethod
    def setUpClass(cls):
        """ Sets-up class variables to be used in the tests. """
        super().setUpClass()
        cls.database_promoters = internals.DataTpmFantom5(file=cv.test_promoter_file_name, nrows=4)
        cls.database_enhancers = internals.DataTpmFantom5(file=cv.test_enhancer_file_name, nrows=4,
                                                          data_type="enhancers")

    def test_primary_cells_ncols_promoters(self):
        self.assertEqual(self.database_promoters.data.shape[1], 537)

    def test_primary_cells_ncols_enhancers(self):
        self.assertEqual(self.database_enhancers.data.shape[1], 537)


class DataParsedFantom5Test(DataTpmFantom5Test):
    @classmethod
    def setUpClass(cls):
        """ Sets-up class variables to be used in the tests. """
        super().setUpClass()
        file_type = "parsed"
        cls.database_promoters = internals.DataTpmFantom5(file=file_type, nrows=4)
        cls.database_promoters.make_data_celltype_specific(cls.celltype_analyse)
        cls.database_enhancers = internals.DataTpmFantom5(file=file_type, nrows=4, data_type="enhancers")
        cls.database_enhancers.make_data_celltype_specific(cls.celltype_analyse)

    def test_primary_cells_ncols_promoters(self):
        self.assertEqual(self.database_promoters.data.shape[1], 155)

    def test_primary_cells_ncols_enhancers(self):
        self.assertEqual(self.database_enhancers.data.shape[1], 155)


class MakeCelltypeSpecificFantom5Test(DataTpmFantom5Test):
    @classmethod
    def setUpClass(cls):
        """ Sets-up class variables to be used in the tests. """
        super().setUpClass()
        cls.database_promoters = internals.DataTpmFantom5(file=cv.test_promoter_file_name, nrows=4)
        cls.database_promoters.make_data_celltype_specific(cls.celltype_analyse)
        cls.database_enhancers = internals.DataTpmFantom5(file=cv.test_enhancer_file_name, nrows=4,
                                                          data_type="enhancers")
        cls.database_enhancers.make_data_celltype_specific(cls.celltype_analyse)

    def test_donors_promoters(self):
        expected = {'Adipocyte - breast, donor1', 'Adipocyte - breast, donor2'}
        self.assertEqual(expected, set(self.database_promoters.target_replicates["Adipocyte - breast"]))

    def test_donors_enhancers(self):
        expected = {'Adipocyte - breast, donor1', 'Adipocyte - breast, donor2'}
        self.assertEqual(expected, set(self.database_enhancers.target_replicates["Adipocyte - breast"]))


class MakeCelltypeSpecificParsedFantom5Test(DataTpmFantom5Test):
    @classmethod
    def setUpClass(cls):
        """ Sets-up class variables to be used in the tests. """
        super().setUpClass()
        file_type = "parsed"
        cls.database_promoters = internals.DataTpmFantom5(file=file_type, nrows=4)
        cls.database_promoters.make_data_celltype_specific(cls.celltype_analyse)
        cls.database_enhancers = internals.DataTpmFantom5(file=file_type, nrows=4, data_type="enhancers")
        cls.database_enhancers.make_data_celltype_specific(cls.celltype_analyse)

    def test_donors_promoters(self):
        expected = {'tpm.Adipocyte%20-%20breast%2c%20donor1.CNhs11051.11376-118A8',
                    'tpm.Adipocyte%20-%20breast%2c%20donor2.CNhs11969.11327-117E4'}
        self.assertEqual(expected, set(self.database_promoters.target_replicates["Adipocyte - breast"]))

    def test_donors_enhancers(self):
        expected = {'Adipocyte - breast, donor1', 'Adipocyte - breast, donor2'}
        self.assertEqual(expected, set(self.database_enhancers.target_replicates["Adipocyte - breast"]))


class MergeDonorsPrimaryFantom5Test(DataTpmFantom5Test):
    @classmethod
    def setUpClass(cls):
        """ Sets-up class variables to be used in the tests. """
        super().setUpClass()
        cls.database_promoters = internals.DataTpmFantom5(file=cv.test_promoter_file_name, nrows=4)
        cls.database_promoters.make_data_celltype_specific(cls.celltype_analyse)
        cls.database_promoters.merge_donors_primary()
        cls.database_enhancers = internals.DataTpmFantom5(file=cv.test_enhancer_file_name, nrows=4,
                                                          data_type="enhancers")
        cls.database_enhancers.make_data_celltype_specific(cls.celltype_analyse)
        cls.database_enhancers.merge_donors_primary()

    def test_merged_promoters_cols(self):
        self.assertEqual(self.database_promoters.data.shape[1], 155)

    def test_merged_enhancers_cols(self):
        self.assertEqual(self.database_enhancers.data.shape[1], 155)

    def test_col_names_equal(self):
        data_promoters = set(self.database_promoters.data.columns.tolist())
        data_enhancers = set(self.database_enhancers.data.columns.tolist())
        self.assertEqual(data_promoters, data_enhancers)


class FilterByTargetFantom5Test(DataTpmFantom5Test):
    @classmethod
    def setUpClass(cls):
        """ Sets-up class variables to be used in the tests. """
        super().setUpClass()
        cls.database_promoters = internals.DataTpmFantom5(file=cv.test_promoter_file_name, nrows=10)
        cls.database_promoters.make_data_celltype_specific(cls.celltype_analyse)
        cls.database_promoters.merge_donors_primary()
        cls.database_enhancers = internals.DataTpmFantom5(file=cv.test_enhancer_file_name, nrows=10,
                                                          data_type="enhancers")
        cls.database_enhancers.make_data_celltype_specific(cls.celltype_analyse)
        cls.database_enhancers.merge_donors_primary()

    def test_above_threshold_promoters(self, threshold=1):
        _temp = self.database_promoters.data[self.database_promoters.target_replicates[self.celltype_analyse]] \
            .values.tolist()
        expected = [i for i in _temp if (all(f >= threshold for f in i))]
        self.database_promoters.filter_by_target_celltype_activity(threshold=threshold, binarize=False)
        to_test = self.database_promoters.data[self.database_promoters.target_replicates[self.celltype_analyse]] \
            .values.tolist()
        self.assertEqual(expected, to_test)

    def test_above_threshold_enhancers(self, threshold=0.15):
        _temp = self.database_enhancers.data[self.database_enhancers.target_replicates[self.celltype_analyse]] \
            .values.tolist()
        expected = [i for i in _temp if (all(f >= threshold for f in i))]
        self.database_enhancers.filter_by_target_celltype_activity(threshold=threshold, binarize=False)
        to_test = self.database_enhancers.data[self.database_enhancers.target_replicates[self.celltype_analyse]] \
            .values.tolist()
        self.assertEqual(expected, to_test)


class DefineNonTargetCelltypesInactivityFantom5Test(DataTpmFantom5Test):
    @classmethod
    def setUpClass(cls):
        """ Sets-up class variables to be used in the tests. """
        super().setUpClass()
        cls.database_promoters = internals.DataTpmFantom5(file=cv.test_promoter_file_name, nrows=10)
        cls.database_promoters.make_data_celltype_specific(cls.celltype_analyse)
        cls.database_promoters.merge_donors_primary()
        cls.database_promoters.filter_by_target_celltype_activity(threshold=1)
        cls.database_promoters.define_non_target_celltypes_inactivity(threshold=0.3)
        cls.database_enhancers = internals.DataTpmFantom5(file=cv.test_enhancer_file_name, nrows=10,
                                                          data_type="enhancers")
        cls.database_enhancers.make_data_celltype_specific(cls.celltype_analyse)
        cls.database_enhancers.merge_donors_primary()
        cls.database_enhancers.filter_by_target_celltype_activity(threshold=0.15)
        cls.database_enhancers.define_non_target_celltypes_inactivity(threshold=0)

    def test_if_int_promoters(self):
        self.assertFalse([True for item in self.database_promoters.data.dtypes if item != np.int64])

    def test_if_int_enhancers(self):
        self.assertFalse([True for item in self.database_enhancers.data.dtypes if item != np.int64])

    def test_no_bigger_than_one_promoters(self):
        result = pd.eval("self.database_promoters.data.values > 1")
        self.assertFalse(np.any(result))

    def test_no_bigger_than_one_enhancers(self):
        result = pd.eval("self.database_enhancers.data.values > 1")
        self.assertFalse(np.any(result))


class FilterBySparsenessFantom5Test(DataTpmFantom5Test):
    @classmethod
    def setUpClass(cls):
        """ Sets-up class variables to be used in the tests. """
        super().setUpClass()
        cls.database_promoters = internals.DataTpmFantom5(file=cv.test_promoter_file_name, nrows=10)
        cls.database_promoters.make_data_celltype_specific(cls.celltype_analyse)
        cls.database_promoters.merge_donors_primary()
        cls.database_promoters.filter_by_reg_element_sparseness(threshold=50)
        cls.database_enhancers = internals.DataTpmFantom5(file=cv.test_enhancer_file_name, nrows=100,
                                                          data_type="enhancers")
        cls.database_enhancers.make_data_celltype_specific(cls.celltype_analyse)
        cls.database_enhancers.merge_donors_primary()
        cls.database_enhancers.filter_by_reg_element_sparseness(threshold=50)

    def test_ctp_still_in_df_promoters(self):
        condition = all([x for x in self.database_promoters.target_replicates[
            self.celltype_analyse] if x in self.database_promoters.data.columns.tolist()])
        self.assertTrue(condition)

    def test_ctp_still_in_df_enhancers(self):
        condition = all([x for x in self.database_enhancers.target_replicates[
            self.celltype_analyse] if x in self.database_enhancers.data.columns.tolist()])
        self.assertTrue(condition)

    def test_number_cols_promoters(self):
        self.assertEqual(10, self.database_promoters.data.shape[0])

    def test_number_cols_enhancers(self):
        self.assertEqual(87, self.database_enhancers.data.shape[0])

    def test_percentile_col_not_in_df(self):
        column = "Percentile_col"
        condition = column in self.database_promoters.data.columns.tolist()
        self.assertFalse(condition)


class SortSparsenessFantom5Test(DataTpmFantom5Test):
    @classmethod
    def setUpClass(cls):
        """ Sets-up class variables to be used in the tests. """
        super().setUpClass()
        cls.database_promoters = internals.DataTpmFantom5(file=cv.test_promoter_file_name, nrows=20)
        cls.database_promoters.make_data_celltype_specific(cls.celltype_analyse)
        cls.database_promoters.merge_donors_primary()
        cls.database_promoters.filter_by_target_celltype_activity(threshold=1)
        cls.database_promoters.define_non_target_celltypes_inactivity(threshold=0)
        cls.database_promoters.sort_sparseness()
        cls.database_enhancers = internals.DataTpmFantom5(file=cv.test_enhancer_file_name, nrows=50,
                                                          data_type="enhancers")
        cls.database_enhancers.make_data_celltype_specific(cls.celltype_analyse)
        cls.database_enhancers.merge_donors_primary()
        cls.database_enhancers.filter_by_target_celltype_activity(threshold=0.15)
        cls.database_enhancers.define_non_target_celltypes_inactivity(threshold=0)
        cls.database_enhancers.sort_sparseness()

    def test_sort_promoters(self):
        self.database_promoters.data["Sum"] = self.database_promoters.data.sum(axis=1)
        counter = 0
        previous_row = None
        for row_sum in self.database_promoters.data["Sum"].values:
            if previous_row is None or row_sum >= previous_row:
                counter += 1
                previous_row = row_sum
        self.assertEqual(counter, 3)

    def test_sort_enhancers(self):
        self.database_enhancers.data["Sum"] = self.database_enhancers.data.sum(axis=1)
        counter = 0
        previous_row = None
        for row_sum in self.database_enhancers.data["Sum"].values:
            if previous_row is None or row_sum >= previous_row:
                counter += 1
                previous_row = row_sum
        self.assertEqual(counter, 5)


class RemoveCelltypeFantom5Test(DataTpmFantom5Test):
    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.cage_primary = internals.DataTpmFantom5(file="parsed", nrows=4)
        self.cage_primary.make_data_celltype_specific(self.celltype_analyse)

    def test_remove_hepatocyte(self):
        self.cage_primary.remove_celltype("Hepatocyte")
        with self.assertRaises(KeyError):
            test = self.cage_primary.data["Hepatocyte"]

    def test_incorrect_celltype(self):
        self.cage_primary.remove_celltype("Hipatocytes")
        condition = not self.cage_primary.data["Hepatocyte"].empty
        self.assertTrue(condition)


class RemoveElementFantom5Test(DataTpmFantom5Test):
    def setUp(self):
        """ Sets-up  variables to be used in the tests. """
        self.cage_primary = internals.DataTpmFantom5(file="parsed", nrows=4)
        self.cage_primary.make_data_celltype_specific(self.celltype_analyse)
        self.elements = ['chr10:100027943..100027958,-', 'chr10:100174900..100174956,-']

    def test_remove_elements(self):
        self.cage_primary.remove_element(self.elements)
        with self.assertRaises(KeyError):
            test = self.cage_primary.data.loc[self.elements]

    def test_incorrect_elements(self):
        self.cage_primary.remove_celltype("test incorrect RE")
        condition = not self.cage_primary.data.loc[self.elements].empty
        self.assertTrue(condition)


class AddCelltypeFantom5Test(DataTpmFantom5Test):
    @classmethod
    def setUpClass(cls):
        """ Sets-up class variables to be used in the tests. """
        super().setUpClass()
        # main data
        cls.cage_primary = internals.DataTpmFantom5(file=cv.test_promoter_file_name, nrows=20)
        # copies for all different tests
        cls.cage_cancer = cls.cage_primary.copy(deep=True)
        cls.cage_primary_rescue = cls.cage_primary.copy(deep=True)
        # adding a cancer celltype
        cls.cage_cancer.add_celltype(celltypes="small cell lung carcinoma cell line",
                                     data_from=cv.test_promoter_file_name,
                                     sample_types="cell lines", data_type="promoters")
        # adding a primary celltype after having removed from the data set
        cls.cage_primary_rescue.remove_celltype("Keratocytes", merged=False)
        cls.cage_primary_rescue.add_celltype(celltypes="Keratocytes", data_from=cv.test_promoter_file_name,
                                             sample_types="primary cells", data_type="promoters")

    def test_merging(self):
        expected = ['small cell lung carcinoma cell line:LK-2', 'small cell lung carcinoma cell line:WA-hT',
                    'small cell lung carcinoma cell line:DMS 144', 'small cell lung carcinoma cell line:NCI-H82']
        for i in expected:
            with self.subTest(i=i):
                self.assertIn(i, self.cage_cancer.data.columns)

    def test_celltype_only_added(self):
        expected_difference = ['small cell lung carcinoma cell line:LK-2', 'small cell lung carcinoma cell line:WA-hT',
                               'small cell lung carcinoma cell line:DMS 144',
                               'small cell lung carcinoma cell line:NCI-H82']
        difference = set(self.cage_cancer.data.columns.values) - set(self.cage_primary.data.columns.values)
        self.assertCountEqual(expected_difference, difference)

    def test_any_nan(self):
        self.assertFalse(self.cage_cancer.data.isnull().values.any())

    def test_adding_back_primary(self):
        self.cage_primary.sort_columns()
        self.cage_primary_rescue.sort_columns()
        self.assertEqual(self.cage_primary, self.cage_primary_rescue)


class EqualFantom5Test(DataTpmFantom5Test):
    @classmethod
    def setUpClass(cls):
        """ Sets-up class variables to be used in the tests. """
        super().setUpClass()
        file_type = "parsed"
        cls.data = internals.DataTpmFantom5(file=file_type, nrows=4)
        cls.data.make_data_celltype_specific(cls.celltype_analyse)
        cls.data2 = cls.data.copy(deep=True)
        cls.data2.sample_type = "test"
        cls.data3 = cls.data.copy(deep=True)
        cls.data3.data.iloc[0, 0] = 3
        cls.data4 = cls.data.copy(deep=True)

    def test_unequal_arg(self):
        condition = self.data == self.data2
        self.assertFalse(condition)

    def test_unequal_data(self):
        condition = self.data == self.data3
        self.assertFalse(condition)

    def test_equal_data(self):
        condition = self.data == self.data4
        self.assertTrue(condition)


class CopyFantom5Test(DataTpmFantom5Test):
    @classmethod
    def setUpClass(cls):
        """ Sets-up class variables to be used in the tests. """
        super().setUpClass()
        file_type = "parsed"
        cls.data = internals.DataTpmFantom5(file=file_type, nrows=4)
        cls.data.make_data_celltype_specific(cls.celltype_analyse)

    def setUp(self):
        self.data2 = self.data.copy(deep=False)
        self.data3 = self.data.copy(deep=True)

    def test_shallow_creation(self):
        self.assertEqual(self.data, self.data2)

    def test_shallow_equal_data(self):
        condition = self.data.data.equals(self.data2.data)
        self.assertTrue(condition)

    def test_deep_creation(self):
        self.assertEqual(self.data, self.data3)

    def test_deep_equal_data(self):
        condition = self.data.data.equals(self.data3.data)
        self.assertTrue(condition)

    def test_change_arg_shallow(self):
        self.data2.target = "test"
        self.assertNotEqual(self.data, self.data2)

    def test_change_arg_deep(self):
        self.data3.target = "test"
        self.assertNotEqual(self.data, self.data3)

    def test_change_data_shallow(self):
        self.data2.data.iloc[1, 1] = "test"
        self.assertEqual(self.data, self.data2)

    def test_change_data_deep(self):
        self.data3.data.iloc[1, 1] = "test"
        self.assertNotEqual(self.data, self.data3)


class SortColumnsFantom5Test(DataTpmFantom5Test):
    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        file_type = "parsed"
        self.cage_tpm = internals.DataTpmFantom5(file=file_type, nrows=4)
        self.cage_tpm.make_data_celltype_specific(self.celltype_analyse)
        self.cols = self.cage_tpm.data.columns.tolist()

    def test_sort_alphabetically(self):
        self.cage_tpm.sort_columns()
        cols = self.cage_tpm.data.columns.tolist()
        for i in (self.cols, sorted(self.cols, key=str.lower)):
            condition = (i == cols)
            with self.subTest(i=i):
                if i == self.cols:
                    self.assertFalse(condition)
                else:
                    self.assertTrue(condition)

    def test_values_remain(self):
        before = self.cage_tpm.data["Urothelial cells"].values.tolist()
        self.cage_tpm.sort_columns()
        after = self.cage_tpm.data["Urothelial cells"].values.tolist()
        self.assertEqual(before, after)

    def test_sort_to_first(self):
        celltype = "Urothelial cells"
        before = self.cage_tpm.data.columns.tolist().index(celltype)
        self.cage_tpm.sort_columns(col_to_shift=celltype, pos_to_move=0)
        after = self.cage_tpm.data.columns.tolist().index(celltype)
        condition = (before != after) and (after == 0)
        self.assertTrue(condition)


# Next we have the tests for the VEnCodes Class:
class VencodeData(unittest.TestCase):
    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.celltype_analyse = "celltypetarget"
        self.data1 = cv.expression_data1
        self.data_tpm = internals.DataTpm(file=self.data1, files_path="test", sep=";")
        self.data_tpm.load_data()

    def test_data_not_celltype_specific(self):
        vencodes = internals.Vencodes(self.data_tpm, algorithm="heuristic", target=self.celltype_analyse)
        condition = vencodes.data.equals(self.data_tpm.data)
        self.assertTrue(condition)

    def test_data_prepared(self):
        self.data_tpm.make_data_celltype_specific(self.celltype_analyse)
        vencodes = internals.Vencodes(self.data_tpm, algorithm="heuristic")
        condition = vencodes.data.equals(self.data_tpm.data)
        self.assertTrue(condition)

    def test_both_methods_equals(self):
        vencodes1 = internals.Vencodes(self.data_tpm, algorithm="heuristic", target=self.celltype_analyse)
        self.data_tpm.make_data_celltype_specific(self.celltype_analyse)
        vencodes2 = internals.Vencodes(self.data_tpm, algorithm="heuristic")
        condition = vencodes1 == vencodes2
        self.assertTrue(condition)


class VencodeFromDataFrame(unittest.TestCase):
    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.df = pd.DataFrame(data=[[0, 1, 0], [1, 1, 0]], index=["first", "second"], columns=["A", "B", "C"])
        self.vencodes = internals.Vencodes(self.df, algorithm="heuristic", target="A")

    def test_data_from_data_frame(self):
        condition = self.df.equals(self.vencodes._data_object.data)
        self.assertTrue(condition)

    def test_equal(self):
        test = internals.Vencodes(self.df, algorithm="heuristic", target="A")
        condition = self.vencodes == test
        self.assertTrue(condition)


class VencodeEquality(unittest.TestCase):
    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.df = pd.DataFrame(data=[[0, 1, 0], [1, 1, 0]], index=["first", "second"], columns=["A", "B", "C"])
        self.vencodes = internals.Vencodes(self.df, algorithm="heuristic", target="A")

    def test_unequal_arg(self):
        vencodes2 = internals.Vencodes(self.df, algorithm="heuristic", target="A")
        vencodes2.algorithm = "test"
        condition = self.vencodes == vencodes2
        self.assertFalse(condition)

    def test_unequal_data(self):
        vencodes3 = internals.Vencodes(self.df, algorithm="heuristic", target="A")
        vencodes3.data.iloc[0, 0] = 3
        condition = self.vencodes == vencodes3
        self.assertFalse(condition)

    def test_equal_data(self):
        vencodes4 = internals.Vencodes(self.df, algorithm="heuristic", target="A")
        condition = self.vencodes == vencodes4
        self.assertTrue(condition)


class VencodesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """ Sets-up class variables to be used in the tests. """
        cls.celltype_analyse = "celltypetarget"
        cls.data1 = cv.expression_data1
        cls.data_tpm = internals.DataTpm(file=cls.data1, files_path="test", sep=";")
        cls.data_tpm.load_data()


class VencodesHeuristicTest(VencodesTest):
    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.vencodes = internals.Vencodes(self.data_tpm, algorithm="heuristic", target=self.celltype_analyse)

    def test_first_vencode(self):
        self.vencodes.next(amount=1)
        expected = ['chr12:109554241..109554255,+', 'chr10:100027943..100027958,-', 'chr10:100174900..100174956,-',
                    'chr12:109548967..109549024,+']
        self.assertCountEqual(expected, self.vencodes.vencodes[0])

    def test_second_vencode(self):
        self.vencodes.next(amount=1)
        vencode = self.vencodes.next(amount=1)
        expected = ['chr12:109554241..109554255,+', 'chr10:100027943..100027958,-', 'chr10:100174900..100174956,-',
                    'chr12:109568972..109568988,+']
        for i in (self.vencodes.vencodes[1], vencode[0]):
            with self.subTest(i=i):
                self.assertCountEqual(expected, i)

    def test_if_correct_vencodes(self):
        self.vencodes.next(amount=4)
        for vencode_data in self.vencodes.get_vencode_data(method="return"):
            vencode_data.drop(self.vencodes.target_replicates, axis=1, inplace=True)
            with self.subTest(i=vencode_data.index.values.tolist()):
                condition = self.vencodes._assess_vencode_one_zero_boolean(vencode_data)
                self.assertTrue(condition)

    def test_e_values_created(self):
        self.vencodes.next(amount=3)
        self.vencodes.determine_e_values()
        maximum, minimum = 100, 0
        for i in self.vencodes.e_values.values():
            with self.subTest(i=i):
                self.assertTrue(maximum >= i >= minimum, msg="{} is not between {} and {}".format(i, minimum, maximum))


class VencodeSamplingTest(VencodesTest):
    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.vencodes = internals.Vencodes(self.data_tpm, algorithm="sampling", target=self.celltype_analyse)

    def test_vencode(self):
        self.vencodes.next(amount=1)
        expected = ['chr12:109554241..109554255,+', 'chr10:100027943..100027958,-', 'chr10:100174900..100174956,-',
                    'chr12:109548967..109549024,+']
        self.assertCountEqual(expected, self.vencodes.vencodes[0])

    def test_second_vencode(self):
        self.vencodes.next(amount=1)
        self.vencodes.next(amount=1)  # by calling two times, this test is also testing that aspect of the generator
        expected = 4
        self.assertEqual(expected, len(self.vencodes.vencodes[1]))

    def test_if_correct_vencodes(self):
        self.vencodes.next(amount=5)
        for vencode_data in self.vencodes.get_vencode_data(method="return"):
            vencode_data.drop(self.vencodes.target_replicates, axis=1, inplace=True)
            with self.subTest(i=vencode_data.index.values.tolist()):
                condition = self.vencodes._assess_vencode_one_zero_boolean(vencode_data)
                self.assertTrue(condition)


class VencodesHepatocyteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """ Sets-up class variables to be used in the tests. """
        cls.celltype_analyse = "Hepatocyte"
        cls.data = internals.DataTpmFantom5(file="parsed", nrows=None)
        cls.data.make_data_celltype_specific(cls.celltype_analyse)


class HepatocyteHeuristicTest(VencodesHepatocyteTest):
    @classmethod
    def setUpClass(cls):
        """ Sets-up class variables to be used in the tests. """
        super().setUpClass()
        cls.data.filter_by_target_celltype_activity(threshold=1)
        cls.data.define_non_target_celltypes_inactivity(threshold=0)
        cls.data.sort_sparseness()

    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.vencodes = internals.Vencodes(self.data, algorithm="heuristic", number_of_re=4)

    def test_first_vencode(self):
        self.vencodes.next(amount=1)
        expected = ['chr15:85427903..85427915,+', 'chr16:72094548..72094561,-', 'chr14:94914994..94915003,-',
                    'chr12:57828590..57828604,+']
        self.assertCountEqual(expected, self.vencodes.vencodes[0])

    def test_second_vencode(self):
        self.vencodes.next(amount=1)
        vencode = self.vencodes.next(amount=1)
        expected = ['chr15:85427903..85427915,+', 'chr16:72094548..72094561,-', 'chr14:94914994..94915003,-',
                    'chr11:61297083..61297101,-']
        for i in (self.vencodes.vencodes[1], vencode[0]):
            with self.subTest(i=i):
                self.assertCountEqual(expected, i)

    def test_if_correct_vencodes(self):
        self.vencodes.next(amount=3)
        for vencode_data in self.vencodes.get_vencode_data(method="return"):
            vencode_data.drop(self.vencodes.target_replicates, axis=1, inplace=True)
            with self.subTest(i=vencode_data.index.values.tolist()):
                condition = self.vencodes._assess_vencode_one_zero_boolean(vencode_data)
                self.assertTrue(condition)

    def test_e_values_created(self):
        self.vencodes.next(amount=2)
        self.vencodes.determine_e_values()
        maximum = 100
        minimum = 0
        for i in self.vencodes.e_values.values():
            with self.subTest(i=i):
                self.assertTrue(maximum >= i >= minimum, msg="{} is not between {} and {}".format(i, minimum, maximum))


class HepatocyteSamplingTest(VencodesHepatocyteTest):
    @classmethod
    def setUpClass(cls):
        """ Sets-up class variables to be used in the tests. """
        super().setUpClass()
        cls.data.filter_by_target_celltype_activity(threshold=1)
        cls.data.define_non_target_celltypes_inactivity(threshold=0)
        cls.data.sort_sparseness()

    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.vencodes = internals.Vencodes(self.data, algorithm="sampling", number_of_re=4, n_samples=10000)

    def test_vencode(self):
        self.vencodes.next(amount=1)
        expected = ['chr15:85427903..85427915,+', 'chr16:72094548..72094561,-', 'chr14:94914994..94915003,-',
                    'chr12:57828590..57828604,+']
        self.assertCountEqual(expected, self.vencodes.vencodes[0])

    def test_second_vencode(self):
        self.vencodes.next(amount=1)
        self.vencodes.next(amount=1)
        expected = 4
        self.assertEqual(expected, len(self.vencodes.vencodes[1]))

    def test_if_correct_vencodes(self):
        self.vencodes.next(amount=3)
        for vencode_data in self.vencodes.get_vencode_data(method="return"):
            vencode_data.drop(self.vencodes.target_replicates, axis=1, inplace=True)
            with self.subTest(i=vencode_data.index.values.tolist()):
                condition = self.vencodes._assess_vencode_one_zero_boolean(vencode_data)
                self.assertTrue(condition)


class VencodesAdipocyteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """ Sets-up class variables to be used in the tests. """
        cls.celltype_analyse = "Adipocyte - breast"
        cls.data = internals.DataTpmFantom5(file="parsed", nrows=None)
        cls.data.make_data_celltype_specific(cls.celltype_analyse)
        cls.data.filter_by_target_celltype_activity(threshold=1)
        cls.data.define_non_target_celltypes_inactivity(threshold=0)
        cls.data.sort_sparseness()

    def setUp(self):
        """ Sets-up  variables to be used in the tests. """
        self.vencodes = internals.Vencodes(self.data, algorithm="heuristic", number_of_re=4)

    def test_first_vencode(self):
        vencode = self.vencodes.next(amount=1)
        expected = ["chr5:42175384..42175396,-", "chr6:72596184..72596196,+", "chr6:11532480..11532521,+",
                    "chr12:109568972..109568988,+"]
        for i in (self.vencodes.vencodes[0], vencode[0]):
            with self.subTest(i=i):
                self.assertCountEqual(expected, i)

    def test_second_vencode(self):
        self.vencodes.next(amount=1)
        vencode = self.vencodes.next(amount=1)
        expected = ["chr5:42175384..42175396,-", "chr6:72596184..72596196,+", "chr12:109568972..109568988,+",
                    "chr7:112614228..112614232,+"]
        for i in (self.vencodes.vencodes[1], vencode[0]):
            with self.subTest(i=i):
                self.assertCountEqual(expected, i)

    def test_if_correct_vencodes(self):
        self.vencodes.next(amount=3)
        for vencode_data in self.vencodes.get_vencode_data(method="return"):
            vencode_data.drop(self.vencodes.target_replicates, axis=1, inplace=True)
            with self.subTest(i=vencode_data.index.values.tolist()):
                condition = self.vencodes._assess_vencode_one_zero_boolean(vencode_data)
                self.assertTrue(condition)

    def test_e_values_created(self):
        self.vencodes.next(amount=2)
        self.vencodes.determine_e_values()
        maximum = 100
        minimum = 0
        for i in self.vencodes.e_values.values():
            with self.subTest(i=i):
                self.assertTrue(maximum >= i >= minimum)


class VencodesKeratocytesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """ Sets-up class variables to be used in the tests. """
        cls.celltype_analyse = "Keratocytes"
        cls.data = internals.DataTpmFantom5(file="parsed", nrows=None)
        cls.data.make_data_celltype_specific(cls.celltype_analyse)
        cls.data.filter_by_target_celltype_activity(threshold=1)
        cls.data.define_non_target_celltypes_inactivity(threshold=0)
        cls.data.sort_sparseness()

    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.vencodes = internals.Vencodes(self.data, algorithm="heuristic", number_of_re=4)

    def test_first_vencode(self):
        vencode = self.vencodes.next(amount=1)
        expected = ['chr4:111536708..111536738,-', 'chr5:79331164..79331177,+', 'chr15:41786065..41786081,+',
                    'chr17:56081185..56081244,-']
        for i in (self.vencodes.vencodes[0], vencode[0]):
            with self.subTest(i=i):
                self.assertCountEqual(expected, i)

    def test_second_vencode(self):
        self.vencodes.next(amount=1)
        vencode = self.vencodes.next(amount=1)
        expected = ['chr4:111536708..111536738,-', 'chr5:79331164..79331177,+', 'chr15:41786065..41786081,+',
                    'chr7:6501803..6501823,-']
        for i in (self.vencodes.vencodes[1], vencode[0]):
            with self.subTest(i=i):
                self.assertCountEqual(expected, i)

    def test_vencode_different_node(self):
        vencodes = self.vencodes.next(amount=2)
        self.assertTrue(len(vencodes) == 2)

    def test_if_correct_vencodes(self):
        self.vencodes.next(amount=3)
        for vencode_data in self.vencodes.get_vencode_data(method="return"):
            vencode_data.drop(self.vencodes.target_replicates, axis=1, inplace=True)
            with self.subTest(i=vencode_data.index.values.tolist()):
                condition = self.vencodes._assess_vencode_one_zero_boolean(vencode_data)
                self.assertTrue(condition)

    def test_e_values_created(self):
        self.vencodes.next(amount=2)
        self.vencodes.determine_e_values()
        maximum = 100
        minimum = 0
        for i in self.vencodes.e_values.values():
            with self.subTest(i=i):
                self.assertTrue(maximum >= i >= minimum)


class VencodesBronchialEpTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """ Sets-up class variables to be used in the tests. """
        cls.celltype_analyse = "Bronchial Epithelial Cell"
        cls.data = internals.DataTpmFantom5(file="parsed", nrows=None)
        cls.data.make_data_celltype_specific(cls.celltype_analyse)
        cls.data.filter_by_target_celltype_activity(threshold=1)
        cls.data.define_non_target_celltypes_inactivity(threshold=0)
        cls.data.sort_sparseness()

    def setUp(self):
        """ Sets-up variables to be used in the tests. """
        self.vencodes = internals.Vencodes(self.data, algorithm="heuristic", number_of_re=4)

    def test_first_vencode(self):
        self.vencodes.next(amount=1)
        self.assertFalse(self.vencodes.vencodes)


class VencodesOtherMethodsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """ Sets-up variables to be used in the tests. """
        cls.data = internals.DataTpmFantom5(file="parsed", sample_types="primary cells", data_type="promoters",
                                            nrows=20000)
        cls.data.make_data_celltype_specific("Hepatocyte")
        cls.data.filter_by_target_celltype_activity(threshold=1)
        cls.data.filter_by_reg_element_sparseness(threshold=0)
        cls.data.define_non_target_celltypes_inactivity(threshold=0)
        cls.data.sort_sparseness()
        cls.vencodes = internals.Vencodes(cls.data, algorithm="heuristic", number_of_re=4, stop=3)
        cls.vencodes.next(amount=2)

    def test_view_vencodes(self):
        self.vencodes.view_vencodes(method="write", snapshot=30, verbose=False)
        folder_path = self.vencodes._parent_path
        file_path_1 = os.path.join(folder_path, "Hepatocyte_heat_map.png")
        file_path_2 = os.path.join(folder_path, "Hepatocyte_heat_map-1.png")
        for i in (file_path_1, file_path_2):
            with self.subTest(i=i):
                self.assertTrue(os.path.exists(i))
                dh.remove_file(i)

    def test_get_vencodes_return(self):
        vencodes = self.vencodes.get_vencode_data(method="return")
        expected = (pd.DataFrame, (4, 156))
        for vencode_data in vencodes:
            properties = (type(vencode_data), vencode_data.shape)
            with self.subTest(i=vencode_data):
                self.assertEqual(properties, expected)

    def test_vencode_mc_simulation(self):
        vencodes = self.vencodes.get_vencode_data(method="return")
        e_value = self.vencodes.vencode_mc_simulation(vencodes[1], reps=1000)
        self.assertLessEqual(0, e_value)

    def test_export_vencodes(self):
        self.vencodes.export("vencodes", verbose=False)
        folder_path = self.vencodes._parent_path
        file_path_1 = os.path.join(folder_path, "Hepatocyte_vencode.csv")
        file_path_2 = os.path.join(folder_path, "Hepatocyte_vencode-1.csv")
        for i in (file_path_1, file_path_2):
            with self.subTest(i=i):
                self.assertTrue(os.path.exists(i))
                dh.remove_file(i)

    def test_export_e_values(self):
        self.vencodes.export("e-values", verbose=False)
        folder_path = self.vencodes._parent_path
        file_path = os.path.join(folder_path, "Hepatocyte_evalues.csv")
        self.assertTrue(os.path.exists(file_path))
        dh.remove_file(file_path)

    def test_export_ven_and_e(self):
        self.vencodes.export("vencodes", "e-values", verbose=False)
        folder_path = self.vencodes._parent_path
        file_path_1 = os.path.join(folder_path, "Hepatocyte_vencode.csv")
        file_path_2 = os.path.join(folder_path, "Hepatocyte_vencode-1.csv")
        file_path_e = os.path.join(folder_path, "Hepatocyte_evalues.csv")
        for i in (file_path_1, file_path_2, file_path_e):
            with self.subTest(i=i):
                self.assertTrue(os.path.exists(i))
                dh.remove_file(i)


if __name__ == "__main__":
    unittest.main(verbosity=2)
