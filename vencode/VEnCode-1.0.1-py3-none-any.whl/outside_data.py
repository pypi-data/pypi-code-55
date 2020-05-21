"""
outside_data.py: Module created to deal with the validation of VEnCodes for only specific celltypes. This module allows
the user to validate VEnCodes' activity using sources of that are not complete enough to determine VEnCode specificity.
"""

import os
import re
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from Bio import SeqIO

from VEnCode.utils import general_utils as gen_util, pandas_utils as pd_util


class OutsideData:
    """
    Base class for all data from outside sources.
    """

    def __init__(self, folder=None):
        if folder is None:
            folder = "Validation_files"
        self.data_path = os.path.join(str(Path(__file__).parents[2]), "Files", folder)
        self._data_source = None
        self.data = None

    @property
    def data_source(self):
        """
        File name of the data.

        Returns
        -------
        str
            File name of the data
        """
        return self._data_source

    @data_source.setter
    def data_source(self, value):
        if value.endswith((".broadPeak", ".BED", ".txt", ".FASTA", ".fasta", ".csv")):
            self._data_source = value
        else:
            if value == "DennySK2016":
                self._data_source = "GSE81255_all_merged.H14_H29_H52_H69_H82_H88_peaks.broadPeak"
            elif value == "InoueF2017":
                self._data_source = "supp_gr.212092.116_Supplemental_File_2_liverEnhancer_design.tsv"
            elif value == "BarakatTS2018":
                self._data_source = ["Barakat et al 2018 - Core and Extended Enhancers.csv",
                                     "Barakat et al 2018 - Merged Enhancers.csv"]
            elif value == "ChristensenCL2014":
                self._data_source = ["1-s2.0-S1535610814004231-mmc3_GLC16.csv",
                                     "1-s2.0-S1535610814004231-mmc3_H82.csv",
                                     "1-s2.0-S1535610814004231-mmc3_H69.csv"]
            elif value == "WangX2018":
                self._data_source = "41467_2018_7746_MOESM4_ESM.txt"
            elif value == "LiuY2017":
                self._data_source = "GSE82204_enhancer_overlap_dnase.txt"
            elif value.startswith("EnhancerAtlas-"):
                self._data_source = "{}.fasta".format(value.split("-", 1)[1])
            else:
                raise AttributeError("Source {} still not implemented".format(value))

    def join_data_sets(self, data_set):
        """
        Joins the data from this source with data from a different source. The result is a filtered data set with
        just the genomic coordinates that are overlapping in both data sets.

        Parameters
        ----------
        data_set : pd.DataFrame
            The data set to merge with.
        """
        union = {"Chromosome": [], "range": []}
        for index, row in self.data.iterrows():
            range1 = row.range
            data2_filter_chr = data_set.data[data_set.data["Chromosome"] == row.Chromosome]
            range2_list = data2_filter_chr["range"].tolist()
            for range2 in range2_list:
                condition = gen_util.partial_subset_of_span(range1, range2)
                if condition:
                    temp_chr, temp_rng = union["Chromosome"], union["range"]
                    temp_chr.append(row.Chromosome)
                    temp_rng.append(self._range_union(range1, range2))
                    union["Chromosome"] = temp_chr
                    union["range"] = temp_rng
                    break
        df = pd.DataFrame.from_dict(union)
        self.data = df

    @staticmethod
    def _range_union(range1, range2):
        values = [x for x in range1]
        values2 = [y for y in range2]
        values += values2
        range_union = [min(values), max(values)]
        return range_union

    def _open_csv_file(self, file_name, sep=";", header="infer", usecols=None, names=None):
        file_path = os.path.join(self.data_path, file_name)
        file_data = pd.read_csv(file_path, sep=sep, header=header, engine="python", usecols=usecols, names=names)
        return file_data

    def _merge_cell_type_files(self):
        enhancer_data_merged = None
        for source in self.data_source:
            enhancer_data = self._open_csv_file(source)
            if enhancer_data_merged is not None:
                enhancer_data_merged = pd.concat([enhancer_data_merged, enhancer_data])
            else:
                enhancer_data_merged = enhancer_data
        return enhancer_data_merged

    def _create_range(self):
        self.data["range"] = [[row.Start, row.End] for index, row in self.data.iterrows()]


class BarakatTS2018Data(OutsideData):
    """
    Data from Barakat, et al., Cell Stem Cell, 2018.
    Parsed to use in VEnCode validation studies.

    How to use: data = internals.BarakatTS2018Data(**kwargs)
    kwargs can be empty, or used to get only part of the data, by using the kwarg: data="core" for example.
    data available are: core and extended enhancers, merged enhancers. Check Barakat, et al., Cell Stem Cell, 2018.
    """

    def __init__(self, source="BarakatTS2018", **kwargs):
        super().__init__()
        self.data_source = source

        try:
            source_partial = kwargs["data"]
            enhancer_file = next((s for s in self.data_source if source_partial.lower() in s.lower()), None)
            self.data = self._open_csv_file(enhancer_file)
        except KeyError:
            self.data = self._merge_cell_type_files()

        gen_util.clean_whitespaces(self.data, "Start", "End")
        pd_util.columns_to_numeric(self.data, "Start", "End")
        self._create_range()


class InoueF2017Data(OutsideData):
    """
        Data from Inoue F, et al., Genome Res., 2017.
        Parsed to use in VEnCode validation studies.

        How to use: data = internals.InoueF2017Data()
        """

    def __init__(self, source="InoueF2017"):
        super().__init__()
        self.data_source = source
        self.data = self._open_csv_file(self.data_source, sep="\t", header=None, names=["temp", "sequence"])
        self._data_cleaner()

    @staticmethod
    def search_between_brackets(string):
        """
        Gets all text between the first [] in a string.
        :param string: String to search for text.
        :return: All text between []
        """
        try:
            return re.search("(?<=\[)(.*)(?=\])", string).group(1)
        except AttributeError:
            pass

    def _genome_location_to_cols(self):
        self.data[["Chromosome", "temp"]] = self.data.temp.str.split(":", expand=True)
        self.data[["Start", "End"]] = self.data.temp.str.split("-", expand=True)
        self.data = self.data[["Chromosome", "Start", "End"]]

    def _genome_location_cleaner(self):
        self.data["temp"] = self.data["temp"].apply(self.search_between_brackets)
        self.data.drop_duplicates("temp", inplace=True)
        self.data.dropna(inplace=True)

    def _data_cleaner(self):
        self._genome_location_cleaner()
        self._genome_location_to_cols()
        pd_util.columns_to_numeric(self.data, "Start", "End")
        self._create_range()


class ChristensenCL2014Data(OutsideData):
    """
    Parses data from Christensen CL, et al., Cancer Cell, 2014, to use in VEnCode validation studies.

    How to use: data = internals.ChristensenCL2014Data(**kwargs)
    kwargs can be empty, or used to get only part of the data, by using the kwarg: data="H82" for example.
    data available are: GLC16, H82, and H69.
    """

    def __init__(self, source="ChristensenCL2014", **kwargs):
        super().__init__()
        self.data_source = source

        try:
            source_partial = kwargs["data"]
            enhancer_file = next((s for s in self.data_source if source_partial.lower() in s.lower()), None)
            self.data = self._open_csv_file(enhancer_file)
        except KeyError:
            self.data = self._merge_cell_type_files()

        self._data_cleaner()

    def _sort_data(self):
        self.data.sort_values(by=["Start"], inplace=True)

    def _data_cleaner(self):
        self._sort_data()
        self.data.rename({"Chrom": "Chromosome", "Stop": "End"}, axis='columns', inplace=True)
        self._create_range()


class BroadPeak(OutsideData):
    """
    Parses data from BroadPeak files to use in VEnCode validation studies.

    How to use: data = internals.BroadPeak(source)
    source can be any source described in baseclass, or a filename ending in .broadPeak
    """

    def __init__(self, source=False):
        super().__init__()
        self.data_source = source
        names = ["Chromosome", "Start", "End", "Name", "Score", "Strand", "SignalValue",
                 "pValue", "qValue"]
        use_cols = range(0, len(names))
        self.data = self._open_csv_file(self.data_source, sep="\t", header=None, usecols=use_cols,
                                        names=names)
        self._data_cleaner()

    def _data_cleaner(self):
        self.data = self.data[["Chromosome", "Start", "End", "Score"]]
        self._create_range()


class Bed(OutsideData):
    """
    Parses data from BED files to use in VEnCode validation studies.

    How to use: data = internals.Bed(source)
    source can be any source described in baseclass, or a filename ending in .BED
    """

    def __init__(self, source=False):
        super().__init__()
        if source:
            self.data_source = source
        names = ["Chromosome", "Start", "End"]
        use_cols = range(0, len(names))
        self.data = self._open_csv_file(self.data_source, sep="\t", header=None, usecols=use_cols,
                                        names=names)

        self._data_cleaner()

    def _data_cleaner(self):
        self.data = self.data[["Chromosome", "Start", "End"]]
        self._create_range()


class Fasta(OutsideData):
    """
    Parses data from FASTA files to use in VEnCode validation studies.

    How to use: data = internals.Fasta(source)
    source can be any source described in baseclass, or a filename ending in .Fasta, .Fa, .txt, etc.
    """

    def __init__(self, source=False):
        super().__init__()
        if source:
            self.data_source = source
        file_path = os.path.join(self.data_path, self.data_source)
        fasta_sequences = SeqIO.parse(open(file_path), 'fasta')
        self._data_cleaner(fasta_sequences)

    def _data_cleaner(self, sequences):
        array = None
        for fasta in sequences:
            name = fasta.id
            name = name.split(':')
            chromosome, locations = name[0], name[1].split("-")
            start, end = locations[0], locations[1]
            end = re.match(r"[0-9]+", end).group()
            info = [[chromosome, start, end]]
            try:
                array = np.append(array, info, axis=0)
            except ValueError:
                array = np.array(info)
        columns = ["Chromosome", "Start", "End"]
        self.data = pd.DataFrame(array, columns=columns)
        pd_util.columns_to_numeric(self.data, "Start", "End")
        self._create_range()


class Csv(OutsideData):
    """
        Parses data from CSV files to use in VEnCode validation studies.

        How to use: data = internals.Csv(source)
        source can be any source described in baseclass, or a filename ending in .csv.
        """

    def __init__(self, source=False, positions=(0, 0, 0, 1), splits=(":", "-")):
        super().__init__(folder="Single Cell analysis")
        if source:
            self.data_source = source
        self.data = self._open_csv_file(self.data_source, sep=";")
        self._data_cleaner(positions, splits)
        pd_util.columns_to_numeric(self.data, "Start", "End")
        self._create_range()

    def _data_cleaner(self, positions, splits):
        data_final = pd.DataFrame()
        columns = ["Chromosome", "Start", "End", "tpm"]
        split_count = 0
        for item, count in Counter(positions).items():
            if count > 1:
                data_to_split = self.data.iloc[:, item]
                for i in range(count - 1):
                    data_temp = data_to_split.str.split(splits[split_count], n=1, expand=True)
                    if columns[split_count] not in data_final.columns:
                        data_final[columns[split_count]] = data_temp[0]
                    if count == i + 2:
                        data_final[columns[split_count + 1]] = data_temp[1]
                    else:
                        data_final[columns[split_count + 1]] = data_temp[1].str.split(splits[split_count + 1], n=1,
                                                                                      expand=True)[0]
                    split_count += 1
            else:
                position = positions.index(item)
                data_final[columns[position]] = self.data.iloc[:, item]
        self.data = data_final