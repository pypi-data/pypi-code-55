#!/usr/bin/env python
"""
Name: Rio Atmadja
Date: 23 May 2020
"""
import numpy as np
from typing import List
from pandas.core.frame import DataFrame
from pandas.core.series import Series

def get_random_features(feature_enginering: bool, feature_names: List[str]) -> List[str]:
    """
    This function will return random feature mtarix
    :param feature_enginering: given a boolean flag of the feature_engineering
    :param feature_names: given a list that contains the feature names
    :return: a list of feature matrix attributes
    """
    if not feature_enginering:
        raise Warning("Must set future_engineering to True")

    if not feature_names:
        raise ValueError("ERROR: feature names cannot be empty")

    lower_bound: int = np.random.randint(0, round(len(feature_names) + 1 / 2))
    upper_bound: int = np.random.randint(lower_bound, len(feature_names) + 1)
    return feature_names[lower_bound:upper_bound]

def get_best_features(feature_engineering: bool, df: DataFrame) -> DataFrame:
    """
    This function will return the best features matrix
    :param feature_enginering: given a boolean flag of the feature_engineering
    :param df: given the dataframe
    :return: a dataframe
    """
    if not feature_engineering:
        raise Warning("Must set feature_engineering to True")

    if df.empty:
        raise Warning("Must run clf.get_auto_accuracy first.")

    return df[(df['accuracy'] > 0.5) & (df['sensitivity'] > 0.5) & (df['specificity'] > 0.5)]


def auto_numeric_map(row: Series, col_names: List[str]) -> Series:
    """
    Convert string numeric into numbers
    :row: given a series of elements
    :col_names: given the colum names to be converted
    :return : numeric representation
    """
    row_data: List = row[col_names].tolist()
    results: List = []

    for data in row_data:
        if str(data).isdigit():
            results.append(int(data))

        elif len(str(row).split('.')) == 2 and str(row).split('.')[0].isdigit() and str(row).split('.')[-1].isdigit():
            results.append(float(data))

        else:
            results.append(data)

    return Series(results)

def save_columns(df: DataFrame) -> List[str]:
    """
    Helper function to save the
    :param df: given a data frame
    :return: a list that contains column names
    """
    return df.columns.tolist()