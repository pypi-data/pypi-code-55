# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Methods for AutoML remote runs."""
import logging

try:
    from azureml.train.automl.runtime._remote_script import setup_wrapper
    from azureml.train.automl.runtime._remote_script import driver_wrapper
    from azureml.train.automl.runtime._remote_script import model_exp_wrapper
except Exception:
    logging.warning("Encountered exception when importing one or more remote wrappers.")

try:
    # If azureml-train-automl-runtime package is not updated enough to have this wrapper, this import may fail.
    # Moving it to the end for specific logging.
    from azureml.train.automl.runtime._remote_script import featurization_wrapper
except Exception:
    logging.warning("Encountered exception when importing featurization wrapper.")
