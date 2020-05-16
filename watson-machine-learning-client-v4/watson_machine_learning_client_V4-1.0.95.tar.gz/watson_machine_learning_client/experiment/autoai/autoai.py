import logging
import sys
from typing import List, Union

from watson_machine_learning_client.workspace import WorkSpace
from watson_machine_learning_client.experiment.autoai.engines import WMLEngine
from watson_machine_learning_client.experiment.autoai.optimizers import LocalAutoPipelines, RemoteAutoPipelines
from watson_machine_learning_client.experiment.autoai.runs import AutoPipelinesRuns
from watson_machine_learning_client.experiment.base_experiment.base_experiment import BaseExperiment
from watson_machine_learning_client.utils.autoai.errors import LocalInstanceButRemoteParameter
from watson_machine_learning_client.utils.autoai.enums import (
    TShirtSize, ClassificationAlgorithms, RegressionAlgorithms, PredictionType, Metrics, DataConnectionTypes,
    PipelineTypes)
from watson_machine_learning_client.utils.autoai.utils import is_ipython, check_dependencies_versions

__all__ = [
    "AutoAI"
]
# note: disable logging if we are in Jupyter Notebook (lale logs appear in wrong cell)
if is_ipython:
    logging.disable(sys.maxsize)

# note: checking installed versions of scikit, xgboost and lightgbm
check_dependencies_versions()


class AutoAI(BaseExperiment):
    """
    AutoAI class for pipeline models optimization automation.

    Parameters
    ----------
    wml_credentials: dictionary, required
        Credentials to Watson Machine Learning instance.

    project_id: str, optional
        ID of the Watson Studio project.

    space_id: str, optional
        ID of the Watson Studio Space.

    Example
    -------
    >>> from watson_machine_learning_client.experiment import AutoAI
    >>> # Remote version of AutoAI
    >>> experiment = AutoAI(
    >>>        wml_credentials={
    >>>              "apikey": "...",
    >>>              "iam_apikey_description": "...",
    >>>              "iam_apikey_name": "...",
    >>>              "iam_role_crn": "...",
    >>>              "iam_serviceid_crn": "...",
    >>>              "instance_id": "...",
    >>>              "url": "https://us-south.ml.cloud.ibm.com"
    >>>            },
    >>>         project_id="...",
    >>>         space_id="...")
    >>>
    >>> # Local version of AutoAI
    >>> experiment = AutoAI()
    """
    # note: initialization of AutoAI enums as class properties
    ClassificationAlgorithms = ClassificationAlgorithms
    RegressionAlgorithms = RegressionAlgorithms
    TShirtSize = TShirtSize
    PredictionType = PredictionType
    Metrics = Metrics
    DataConnectionTypes = DataConnectionTypes
    PipelineTypes = PipelineTypes

    def __init__(self, wml_credentials: Union[dict, 'WorkSpace'] = None, project_id: str = None, space_id: str = None) -> None:

        # note: as workspace is not clear enough to understand, there is a possibility to use pure
        # wml credentials with project and space IDs, but in addition we
        # leave a possibility to use a previous WorkSpace implementation, it could be passed as a first argument
        if wml_credentials is None:
            self._workspace = None

        else:
            if isinstance(wml_credentials, WorkSpace):
                self._workspace = wml_credentials
            else:
                self._workspace = WorkSpace(wml_credentials=wml_credentials.copy(),
                                            project_id=project_id,
                                            space_id=space_id)

            self.project_id = self._workspace.project_id
            self.space_id = self._workspace.space_id
            self.runs = AutoPipelinesRuns(engine=WMLEngine(self._workspace.wml_client))
            self.runs._workspace = self._workspace
        # --- end note

    def runs(self, *, filter: str) -> 'AutoPipelinesRuns':
        """Get the historical runs but with WML Pipeline name filter.

        Parameters
        ----------
        filter: str, required
            WML Pipeline name to filter the historical runs.

        Returns
        -------
        AutoPipelinesRuns

        Example
        -------
        >>> from watson_machine_learning_client.experiment import AutoAI
        >>> experiment = AutoAI(...)
        >>>
        >>> experiment.runs(filter='Test').list()
        """
        return AutoPipelinesRuns(engine=WMLEngine(self._workspace.wml_client), filter=filter)

    def optimizer(self,
                  name: str,
                  *,
                  prediction_type: 'PredictionType',
                  prediction_column: str,
                  scoring: 'Metrics',
                  desc: str = None,
                  test_size: float = 0.1,
                  max_number_of_estimators: int = 1,
                  train_sample_rows_test_size: float = None,
                  daub_include_only_estimators: List[Union['ClassificationAlgorithms', 'RegressionAlgorithms']] = None,
                  **kwargs) -> Union['RemoteAutoPipelines', 'LocalAutoPipelines']:
        """
        Initialize an AutoAi optimizer.

        Parameters
        ----------
        name: str, required
            Name for the AutoPipelines

        prediction_type: PredictionType, required
            Type of the prediction.

        prediction_column: str, required
            name of the target/label column

        scoring: Metrics, required
            Type of the metric to optimize with.

        desc: str, optional
            Description

        test_size: float, optional
            Percentage of the entire dataset to leave as a holdout. Default 0.1

        max_number_of_estimators: int, optional
            Maximum number (top-K ranked by DAUB model selection) of the selected algorithm, or estimator types,
            for example LGBMClassifierEstimator, XGBoostClassifierEstimator, or LogisticRegressionEstimator
            to use in pipeline composition.  The default is 1, where only the highest ranked by model
            selection algorithm type is used. (min 1, max 4)

        train_sample_rows_test_size: float, optional
            Training data sampling percentage

        daub_include_only_estimators: List[Union['ClassificationAlgorithms', 'RegressionAlgorithms']], optional
            List of estimators to include in computation process.
            See: AutoAI.ClassificationAlgorithms or AutoAI.RegressionAlgorithms

        t_shirt_size: TShirtSize, optional
            The size of the remote AutoAI POD instance (computing resources). Only applicable to a remote scenario.
            See: AutoAI.TShirtSize

        Returns
        -------
        RemoteAutoPipelines or LocalAutoPipelines, depends on how you initialize the AutoAI object.

        Example
        -------
        >>> from watson_machine_learning_client.experiment import AutoAI
        >>> experiment = AutoAI(...)
        >>>
        >>> optimizer = experiment.optimizer(
        >>>        name="name of the optimizer.",
        >>>        prediction_type=AutoAI.PredictionType.CLASSIFICATION,
        >>>        prediction_column="y",
        >>>        scoring=AutoAI.Metrics.ROC_AUC_SCORE,
        >>>        desc="Some description.",
        >>>        test_size=0.1,
        >>>        max_num_daub_ensembles=1,
        >>>        train_sample_rows_test_size=1,
        >>>        daub_include_only_estimators=[AutoAI.ClassificationAlgorithms.LGBM, AutoAI.ClassificationAlgorithms.XGB],
        >>>        t_shirt_size=AutoAI.TShirtSize.L
        >>>    )
        >>>
        >>> optimizer = experiment.optimizer(
        >>>        name="name of the optimizer.",
        >>>        prediction_type=AutoAI.PredictionType.CLASSIFICATION,
        >>>        prediction_column="y",
        >>>        scoring=AutoAI.Metrics.ROC_AUC_SCORE,
        >>>        desc="Some description.",
        >>>    )
        """
        if self._workspace is None and kwargs.get('t_shirt_size'):
            raise LocalInstanceButRemoteParameter(
                "t_shirt_size",
                reason="During LocalOptimizer initialization, \"t_shirt_size\" parameter was provided. "
                       "\"t_shirt_size\" parameter is only applicable to the RemoteOptimizer instance."
            )
        elif self._workspace is None:
            return LocalAutoPipelines(
                name=name,
                prediction_type=prediction_type,
                prediction_column=prediction_column,
                scoring=scoring,
                desc=desc,
                test_size=test_size,
                max_num_daub_ensembles=max_number_of_estimators,
                train_sample_rows_test_size=train_sample_rows_test_size,
                daub_include_only_estimators=daub_include_only_estimators)

        else:
            optimizer = RemoteAutoPipelines(
                name=name,
                prediction_type=prediction_type,
                prediction_column=prediction_column,
                scoring=scoring,
                desc=desc,
                test_size=test_size,
                max_num_daub_ensembles=max_number_of_estimators,
                t_shirt_size=kwargs.get('t_shirt_size', TShirtSize.M),
                train_sample_rows_test_size=train_sample_rows_test_size,
                daub_include_only_estimators=daub_include_only_estimators,
                engine=WMLEngine(self._workspace.wml_client),
                notebooks=kwargs.get('notebooks', False),
                autoai_pod_version=kwargs.get('autoai_pod_version', '0.1.425')
            )
            optimizer._workspace = self._workspace
            return optimizer
