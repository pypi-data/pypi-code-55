#!/usr/bin/env python
"""
Name: Rio Atmadja
Date: 23 May 2020
"""
import numpy as np
from typing import List
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from botocore.exceptions import MissingParametersError
from typing import Dict
from numpy import ndarray
from sklearn.model_selection import train_test_split
import pandas as pd

def get_random_features(feature_names: List[str]) -> List[str]:
    """
    This function will return random feature mtarix
    :param feature_names: given a list that contains the feature names
    :return: a list of feature matrix attributes
    """
    if not feature_names:
        raise ValueError("ERROR: feature names cannot be empty")

    lower_bound: int = np.random.randint(0, round(len(feature_names) + 1 / 2))
    upper_bound: int = np.random.randint(lower_bound, len(feature_names) + 1)
    return feature_names[lower_bound:upper_bound]

def get_best_features(df: DataFrame, *attrib) -> DataFrame:
    """
    This function will return the best features matrix
    :param df: given the dataframe
    :attrib: given a tuple of feature attributes
    :return: a dataframe
    """
    if df.empty:
        raise Warning("Must run clf.get_auto_accuracy first.")

    accuracy, sensitivity, specificity = attrib

    return df[(df['accuracy'] > accuracy) & (df['sensitivity'] > sensitivity) & (df['specificity'] > specificity)]


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
            results.append(pd.factorize(data))

    return Series(results)

def save_columns(df: DataFrame) -> List[str]:
    """
    Helper function to save the
    :param df: given a data frame
    :return: a list that contains column names
    """
    return df.columns.tolist()


def get_possible_combinations(feature_names: List[str], iteration: int = int(np.random.randint(10, 50, size=1))) -> List[List]:
    """
    Helper function to remove duplicates feature matrix
    :feature_names: given the feature matrix
    :iteration: an optional parameter with a default iteration of 10 to 50 iterations
    :return: a list of list of feature matricies
    """
    if iteration <= 1:
        raise ValueError("ERROR: iteration must be greater than 1")

    if not feature_names:
        raise MissingParametersError(object_name="Required parameters", missing="feature_names")

    combinations: List[str] = sorted(set([','.join(get_random_features(feature_names=feature_names)) for n_features in range(iteration)]))

    return list(map(lambda row: row.split(','), filter(lambda row: len(row) > 1, map(lambda row: row, combinations))))

def train_test(feature_matrix: DataFrame, response_vector: Series, random_state: int = np.random.randint(100, 150)) -> Dict:
    """
    Helper function to create to split given feature matrix and response vectors into training and testing data
    :feature_matrix: given the feature matrix of mxn dimensions
    :response_vector: given a scalar vector
    :random_state: an optional param with random state from 100 to 150
    :return: a dictionary that contains testing and training data attributes
    """

    if not get_dimensions(feature_matrix) and not get_dimensions(response_vector):
        raise ValueError(
            f"ERROR Mismatch Dimensions Feature Matrix: {feature_matrix.shape} must equals Response Vector: {response_vector.shape}")

    X_train, X_test, y_train, y_test = train_test_split(feature_matrix, response_vector,
                                                        random_state=random_state)

    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test

    }

def get_dimensions(vector) -> tuple:
    """
    Helper function to check the dimension of the given vectors and return the mxn dimension
    :vector: given mxn vector
    :return: a tuple of mxn object
    """
    if not type(vector) in [Series, DataFrame, ndarray]:
        raise TypeError("Error: Must be type of ndarray, Series, DataFrame")

    return vector.shape


def as_character(df: DataFrame, col_names: List[str]) -> DataFrame:
    """
    Helper function to convert dataframe of mxn into vector of characrters
    :param df: given an mxn data frame
    :param col_names: given column names to be converted
    :return: a set of mxn chars of data frame
    """
    if not col_names:
        raise MissingParametersError(object_name="Required parameters", missing="col_names")

    return df[col_names].apply(lambda col: pd.factorize(col)[0], axis=0 )