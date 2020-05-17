#  C O N S T R U C T I V I S T__ __
#   _____ ____   ____   /  |/  // /
#  / ___// __ \ / __ \ / /|_/ // /
# / /__ / /_/ // / / // /  / // /___
# \___/ \____//_/ /_//_/  /_//_____/
#  M A C H I N E   L E A R N I N G
#
#
# A Project by
# Thomas Schmid | UNIVERSITÄT LEIPZIG
# www.constructivist.ml
#
# Code Author: Dmitrij Denisenko
# Licence: MIT


"""Defines the pandas adapter.

"""


import re
import pandas as pd


def convert_df_to_block(dataframe):
    """Create PandasBlock from given dataframe.

    Args:
        dataframe (pandas.DataFrame)

    Returns:
        PandasBlock

    """
    return PandasBlock(dataframe)


def build_block_from_rows(rows):
    """Create PandasBlock from a list of pandas.Series.

    Args:
        rows (list): Rows as pandas.Series.

    Returns:
        PandasBlock

    """
    df = pd.concat(rows, sort=False)
    return PandasBlock(df)


def build_new_learnblock(values, columns, index, origin):
    """Build PandasBlock from given values, columns and index.

    Args:
        values (numpy.ndarray): Data that forms the dataframe.
        columns (list): Names of the columns as str.
        index (list): Index to use.
        origin (tuple): Indicator where this learnblock comes from.

    Returns:
        PandasBlock

    """
    data_frame = pd.DataFrame(data=values, columns=columns, index=index)
    block = PandasBlock(data_frame, origin=origin)
    return block


class PandasBlock:
    """Responsible for encapsulating pandas.DataFrame.

    Args:
        dataframe (pandas.DataFrame): Contains the data.
        relationship (tuple):
            If not None, contains the learnblock relationship.
        subject (tuple): If not None, contains the learnblock subject.
        origin (tuple):
            If not None, contains the origin of the learnblock.
            Plain integers indicate that this learnblock is from a raw
            block. Aim values indicate that this learnlock was build
            form the labels from two models.

    """
    LAST_THREE_COLUMNS = 3
    TIME = "T"
    SUBJECT = "Sigma"
    PURPOSE = "Z"

    def __init__(self, dataframe, relationship=None, subject=None, origin=None):
        self.df = dataframe
        self._origin = origin
        self.relationship = relationship
        self.subject = subject
        # TODO (dmt): Check if you really need n_cluster.
        self.n_cluster = None

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = value

    def __str__(self):
        return ("origin: <{}> subject: <{}> "
                "n_cluster: <{}> relationship: <{}>".format(self.origin,
                                                            self.subject,
                                                            self.n_cluster,
                                                            self.relationship))

    def __len__(self):
        return self.n_rows()

    def __getitem__(self, item):
        end = self.n_columns(effective=True)
        return self.df.iloc[item][:end]

    def shape(self):
        """Shape of the dataframe.

        Returns:
            tuple:
                Integers indicating row and column number.

        """
        return self.df.shape

    def row_as_df_via_index(self, index):
        """Get pandas.Series via given Index.

        Args:
            index (int): Row index.

        Returns:
            pandas.Series

        """
        return self.df.loc[[index]]

    def n_rows(self):
        """Number of rows.

        Returns:
           int

        """
        return self.df.shape[0]

    def n_columns(self, effective=False):
        """Number of columns.

        Args:
            effective (bool): Indicator if T, Sigma and Z should be taken
                into account.

        Returns:
            int:
                Number of columns.

        """
        if effective:
            return max(0, self.df.shape[1] - self.LAST_THREE_COLUMNS)
        else:
            return self.df.shape[1]

    def columns(self, effective=False):
        """Get the names of the columns.

        Args:
            effective (bool): Indicator if T, Sigma, Z should be taken into
                account.

        Returns:
            list:
                Names of columns.

        """
        if not effective:
            return list(self.df.columns)
        else:
            features = list(self.df.columns)
            features.remove(self.TIME)
            features.remove(self.PURPOSE)
            features.remove(self.SUBJECT)
            return features

    def memory_usage(self):
        """Memory usage of the dataframe.

        Returns:
            int

        """
        return self.df.memory_usage().sum()

    def min_timestamp(self):
        """Smallest time value within T feature.

        Returns:
            int

        """
        return min(self.df["T"])

    def max_timestamp(self):
        """Biggest time value withtin T feature.

        Returns:
            int

        """
        return max(self.df["T"])

    def indices(self):
        """Get the indices of pandas.DataFrame.

        Returns:
            list:
                Indices as integers.

        """
        return list(self.df.index)

    def reindex(self, indices):
        """Change the indices of dataframe to new indices.

        Args:
            indices (list): New indices.

        """
        assert len(indices) == self.df.shape[0]
        self.df.index = indices

    def has_nan(self):
        """Check if the dataframe has any NaN.

        Returns:
            bool
                True, if there is at least one NaN.

        """
        return bool(self.df.isna().any().any())

    def drop_rows(self, row):
        """Remove given row from the dataframe.

        Args:
            row (pandas.Series): Row to remove.

        """
        self.df.drop(row, inplace=True)

    def rename_columns(self, names):
        """Rename dataframe columns to the given names.

        Args:
            names (list): Names as strings.

        """
        names.extend(["T", "Sigma", "Z"])
        self.df.columns = names

    def rename_column(self, old_name, new_name):
        """Rename a single column.

        Args:
            old_name (str): Column to rename.
            new_name (str): New name.

        """
        self.df = self.df.rename(columns={old_name: new_name})

    def drop_columns(self, columns, by_index=False):
        """Remove columns from dataframe.

        Args:
            columns (list): String names or integer indices.
            by_index (bool): Indicates if columns should be interpreted as
                integers or strings.

        """
        if not by_index:
            self.df = self.df.drop(columns=columns)
        else:
            assert all([isinstance(column, int) for column in columns])
            names = [self.df.columns[index] for index in columns]
            self.df = self.df.drop(columns=names)

    def labeled(self):
        """Check if the block is alreay labeled.

        Returns:
            bool:
                True, if labeled.

        """
        values_empty = self.df["Z"].iloc[0].strip('""') == ''
        values_unique = self.df["Z"].nunique() == 1
        if values_empty and values_unique:
            return False

        elif not values_empty and values_unique:
            return True

        else:
            return False

    def reorder_columns(self, columns):
        """Reorder columns accoring the given order.

        Args:
            columns (list): Column names as strings.

        """
        self.df = self.df[columns]

    def as_numpy_array(self, effective=True):
        """Get the dataframe as numpy ndarray.

        Args:
            effective (bool): Indicator if columns T, Sigma, Z should be taken
                into account.

        Returns:
            pandas.ndarray

        """
        return self.df[self.columns(effective=effective)].values

    def set_column(self, name, values):
        """Assign column values to given values.

        If the given column does not exist, it will be created.

        Args:
            name (str): Column name.
            values (list): Column values.

        """
        if isinstance(values, list):
            assert len(values) == self.n_rows()
        self.df[name] = values

    def new_block_from(self, fundament, time_column=False, index=False):
        """Construct PandasBlock from either given time stamps or given
        index.

        Args:
            fundament (list): Timestamps or indices as intergers.
            time_column (bool): Indicates if fundament should be interpreted
                as a list of timestamps.
            index (bool): Indicates if fundament should be interpreted as
                as list of indices.

        Returns:
              PandasBlock.

        """
        if index:
            assert all([isinstance(index, int) for index in fundament])
            return PandasBlock(
                self.df.loc[fundament],
                self.relationship,
                self.subject,
                origin=self.origin)

        if time_column:
            assert all([isinstance(timestamp, int) for timestamp in fundament])
            return PandasBlock(
                self.df.loc[self.df["T"].isin(fundament)],
                self.relationship,
                self.subject,
                origin=self.origin)

    def get_column(self, name):
        """Get column values for the given column.

        Args:
            name (str): Column name.

        Returns:
            list

        """
        return self.df[name].to_list()

    def get_row(self, index):
        """Get row via index.

        Args:
            index (int): Row index.

        Returns:
            list

        """
        return self.df.iloc[index].to_list()

    def sort_after(self, column, ascending=True):
        """Sort column.

        Args:
            column (str): Column name.
            ascending (bool): Indicates sorting order.

        """
        self.df.sort_values(by=[column], ascending=ascending, inplace=True)

    def get_duplicated_pairs(self, column_a, column_b):
        """Find duplicated rows in the given columns.

        Args:
            column_a (str): Column name as str.
            column_b (str): Column name as str.

        Yield:
            tuple:
                Duplicated rows.

        """
        bool_series = self.df.duplicated(subset=[column_a, column_b])
        duplicates = self.df[bool_series]
        for i, j in zip(duplicates[column_a], duplicates[column_b]):
            yield i, j

    def construct_from_two_pairs(self, **kwargs):
        """Build PandasBlock from given T, Z or Sigma value.

        Args:
            **kwargs: Contains T, Z and Sigma value.

        Returns:
            PandasBlock

        """
        t, z, sigma = kwargs.get("T"), kwargs.get("Z"), kwargs.get("Sigma")

        if t is not None and z is not None:
            df = self.df.loc[(self.df["T"] == t) & (self.df["Z"] == z)]
        elif t is not None and sigma is not None:
            df = self.df.loc[(self.df["T"] == t) & (self.df["Sigma"] == sigma)]
        else:
            df = self.df.loc[(self.df["Z"] == z) & (self.df["Sigma"] == sigma)]

        return PandasBlock(df, self.relationship, origin=self.origin)

    def get_overlapping_on_timestamps(self, block):
        """Construct a new PandasBlock from overlapping timestamps.

        Args:
            block (PandasBlock): Block.

        Returns:
              PandasBlock

        """
        if len(block) < len(self):
            biggest = block
            block = self
        else:
            biggest = self
            block = block

        join = biggest.df.join(block.df.set_index("T"),
                               on="T",
                               lsuffix="_other",
                               how="inner")

        if any(join.duplicated(["T"])):
            join.drop_duplicates(subset="T", keep="first", inplace=True)
            # empty_df = pd.DataFrame()

        return PandasBlock(join, origin=self.origin, subject=self.subject)

    def same_features_fusion(self, block):
        """Build a new PandasBlock based on the feature intersection of
        two PandasBlocks.

        Args:
            block (PandasBlock): Learnblock.

        Returns:
            PandasBlock

        """
        df = pd.concat([self.df, block.df], sort=False, join="inner")
        origin = tuple(set(self.origin+block.origin))
        return PandasBlock(df, subject=self.subject, origin=origin)

    def constructed_from_models(self):
        """Check if this PandasBlock from build based on
        PragmaticMachineLearningModel.

        Returns:
            bool:
                True, if this block was build based on
                PragmaticMachineLearningModel.

        """
        regex = "[A-Z]\.\d+\.\d+"
        return any([re.match(regex, str(o)) for o in self.origin])
