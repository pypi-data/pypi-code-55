# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utility methods for data transformation."""
from typing import List, Union, Any, Optional, cast

import logging
from sklearn_pandas import DataFrameMapper

from azureml.core import Run
from azureml.automl.core.constants import FeaturizationRunConstants
from azureml.automl.core.shared import logging_utilities
from .featurization import DataTransformer
from .featurization import data_transformer_utils
from .featurization import TransformerAndMapper
from azureml.automl.runtime._engineered_feature_names import _GenerateEngineeredFeatureNames
from azureml.automl.runtime.shared.types import DataInputType
from azureml.automl.runtime.shared.pickler import DefaultPickler


logger = logging.getLogger(__name__)
_PICKLER = DefaultPickler()


def _upload_pickle(obj: Any, run_obj: Run, file_name: str) -> None:
    """
    Helper function for uploading object to storage with specified file name.

    :param obj: The object to be uploaded.
    :param run_obj: The run through which we upload the file.
    :param file_name: The name of the file to be created in storage.
    :return: None
    """
    _PICKLER.dump(obj, file_name)
    run_obj.upload_file(file_name, file_name)


def _download_pickle(file_name: str) -> Any:
    """
    Helper function for downloading file from storage.

    :param file_name: The name of the file to be downloaded.
    :return: The downloaded, unpickled object.
    """
    return _PICKLER.load(file_name)


def load_and_update_from_sweeping(data_transformer: DataTransformer,
                                  df: DataInputType) -> None:
    """
    Function called in the featurization run for updating the newly-instantiated data transformer
    with values from the setup iteration's data transformer that are necessary for full featurization.

    :param data_transformer: The data transformer to update.
    :param df: The input data used for recreating the column types mapping.
    :return: None.
    """

    run = Run.get_context()
    property_dict = run.get_properties()

    with logging_utilities.log_activity(logger=logger, activity_name="FeatureConfigDownload"):
        try:
            feature_config = _download_pickle(property_dict.get(FeaturizationRunConstants.CONFIG_PROP,
                                                                FeaturizationRunConstants.CONFIG_PATH))
        except Exception as e:
            logging_utilities.log_traceback(
                exception=e,
                logger=logger,
                override_error_msg="Error when retrieving feature config from local node storage.")
            raise e

    if data_transformer._is_onnx_compatible:
        data_transformer.mapper = feature_config
    else:
        data_transformer.transformer_and_mapper_list = feature_config

    with logging_utilities.log_activity(logger=logger, activity_name="EngineeredFeatureNamesDownload"):
        try:
            data_transformer._engineered_feature_names_class = \
                _download_pickle(property_dict.get(FeaturizationRunConstants.NAMES_PROP,
                                                   FeaturizationRunConstants.NAMES_PATH))
        except Exception as e:
            logging_utilities.log_traceback(
                exception=e,
                logger=logger,
                override_error_msg="Error when retrieving feature names from local node storage.")
            raise e

    if data_transformer._columns_types_mapping is None:
        data_transformer._columns_types_mapping = data_transformer_utils.get_pandas_columns_types_mapping(df)

    data_transformer._feature_sweeped = True


def save_feature_config(feature_config: Union[List[TransformerAndMapper], DataFrameMapper]) -> None:
    """
    Logic for saving the transformer_and_mapper_list or mapper from the setup run's data transformer.

    :param feature_config: The feature config to be downloaded and used in the featurization run.
    :return: None.
    """
    run = Run.get_context()
    with logging_utilities.log_activity(logger=logger, activity_name="FeatureConfigUpload"):
        _upload_pickle(feature_config, run, FeaturizationRunConstants.CONFIG_PATH)


def save_engineered_feature_names(engineered_feature_names: _GenerateEngineeredFeatureNames) -> None:
    """
    Logic for saving the engineered feature names from the setup run's data transformer.

    :param engineered_feature_names: The feature names to be downloaded and used in the featurization run.
    :return: None.
    """
    run = Run.get_context()
    with logging_utilities.log_activity(logger=logger, activity_name="EngineeredFeatureNamesDownload"):
        _upload_pickle(engineered_feature_names, run, FeaturizationRunConstants.NAMES_PATH)
