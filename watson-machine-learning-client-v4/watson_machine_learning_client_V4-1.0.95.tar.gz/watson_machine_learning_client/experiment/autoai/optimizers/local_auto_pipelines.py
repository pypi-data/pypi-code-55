import os
import traceback
import uuid
from contextlib import redirect_stdout
from inspect import signature
from time import gmtime, strftime
from typing import Union, List, Tuple, TYPE_CHECKING
from warnings import filterwarnings

from numpy import ndarray
from pandas import DataFrame
from pandas import Series

from watson_machine_learning_client.utils.autoai.local_training_message_handler import LocalTrainingMessageHandler
from watson_machine_learning_client.utils.autoai.utils import try_import_lale
from watson_machine_learning_client.utils.autoai.errors import FitNeeded
from watson_machine_learning_client.utils.autoai.enums import (
    PredictionType, Directions, MetricsToDirections, PipelineTypes)
from .base_auto_pipelines import BaseAutoPipelines

if TYPE_CHECKING:
    from watson_machine_learning_client.utils.autoai.enums import (
        Metrics, ClassificationAlgorithms, RegressionAlgorithms)
    from sklearn.pipeline import Pipeline

__all__ = [
    "LocalAutoPipelines"
]
DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class LocalAutoPipelines(BaseAutoPipelines):
    """
    LocalAutoPipelines class for pipeline operation automation.

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

    max_num_daub_ensembles: int, optional
        Maximum number (top-K ranked by DAUB model selection) of the selected algorithm, or estimator types,
        for example LGBMClassifierEstimator, XGBoostClassifierEstimator, or LogisticRegressionEstimator
        to use in pipeline composition.  The default is 1, where only the highest ranked by model
        selection algorithm type is used.

    train_sample_rows_test_size: float, optional
        Training data sampling percentage

    daub_include_only_estimators: List[Union['ClassificationAlgorithms', 'RegressionAlgorithms']], optional
        List of estimators to include in computation process.
    """

    def __init__(self,
                 name: str,
                 prediction_type: 'PredictionType',
                 prediction_column: str,
                 scoring: 'Metrics',
                 desc: str = None,
                 test_size: float = 0.1,
                 max_num_daub_ensembles: int = 1,
                 train_sample_rows_test_size: float = 1.,
                 daub_include_only_estimators: List[Union['ClassificationAlgorithms', 'RegressionAlgorithms']] = None):

        import logging
        # Disable printing to suppress warnings from ai4ml
        with redirect_stdout(open(os.devnull, "w")):
            try:
                from ai4ml.joint_optimizers.prep_daub_cog_opt import PrepDaubCogOptEstimator
                from ai4ml.utils.ai4ml_status import StatusMessageHandler

            except ModuleNotFoundError:
                raise ModuleNotFoundError("To be able to use a Local Optimizer version, you need to have "
                                          "a full ai4ml installed locally.")

        # note: ai4ml uses a default root handler, we need to recreate it to be able to log into the file
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        logging.basicConfig(filename='local_auto_pipelines.log',
                            filemode='w',
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            datefmt=DATE_FORMAT,
                            level=logging.DEBUG)
        # -- end note

        self.params = {
            'name': name,
            'desc': desc if desc else '',
            'prediction_type': prediction_type,
            'prediction_column': prediction_column,
            'scoring': scoring,
            'test_size': test_size,
            'max_num_daub_ensembles': int(max_num_daub_ensembles),
            'train_sample_rows_test_size': train_sample_rows_test_size,
            'daub_include_only_estimators': daub_include_only_estimators
        }
        self.best_pipeline = None
        self._pdcoe = None
        self._computed_pipelines_details = None
        self.logger = logging.getLogger()

    def get_params(self) -> dict:
        """
        Get configuration parameters of AutoPipelines.

        Returns
        -------
        Dictionary with AutoPipelines parameters.

        Example
        -------
        >>> from watson_machine_learning_client.experiment import AutoAI
        >>> experiment = AutoAI()
        >>> local_optimizer = experiment.optimizer()
        >>>
        >>> local_optimizer.get_params()
            {
                'name': 'test name',
                'desc': 'test description',
                'prediction_type': 'classification',
                'prediction_column': 'y',
                'scoring': 'roc_auc',
                'test_size': 0.1,
                'max_num_daub_ensembles': 1,
                'train_sample_rows_test_size': 0.8,
                'daub_include_only_estimators': ["ExtraTreesClassifierEstimator",
                                                "GradientBoostingClassifierEstimator",
                                                "LGBMClassifierEstimator",
                                                "LogisticRegressionEstimator",
                                                "RandomForestClassifierEstimator",
                                                "XGBClassifierEstimator"]
            }
        """
        return self.params

    def fit(self, X: 'DataFrame', y: 'Series') -> 'Pipeline':
        """
        Run a training process of AutoAI locally.

        Parameters
        ----------
        X: pandas.DataFrame, required
            Training dataset.

        y: pandas.Series, required
            Target values.

        Returns
        -------
        Pipeline model (best found)

        Example
        -------
        >>> from watson_machine_learning_client.experiment import AutoAI
        >>> experiment = AutoAI()
        >>> local_optimizer = experiment.optimizer()
        >>>
        >>> fitted_best_model = local_optimizer.fit(X=test_data_x, y=test_data_y)
        """
        if not isinstance(X, DataFrame) or not isinstance(y, Series):
            raise TypeError("\"X\" should be of type pandas.DataFrame and \"y\" should be of type pandas.Series.")

        self._pdcoe = self._train(train_x=X, train_y=y)
        self.best_pipeline = self._pdcoe.best_pipeline
        self._computed_pipelines_details = self._pdcoe.status_msg_handler.status_dict['ml_metrics']['global_output']

        return self._pdcoe.best_pipeline

    def get_holdout_data(self) -> Tuple['DataFrame', 'ndarray']:
        """
        Provide holdout part of the training dataset (X and y) to the user.

        Returns
        -------
        X: DataFrame , y: ndarray

        Example
        -------
        >>> from watson_machine_learning_client.experiment import AutoAI
        >>> experiment = AutoAI()
        >>> local_optimizer = experiment.optimizer()
        >>>
        >>> holdout_data = local_optimizer.get_holdout_data()
        """
        if self._pdcoe is None:
            raise FitNeeded(reason="To list computed pipelines parameters, "
                                   "first schedule a fit job by using a fit() method.")

        columns = self._pdcoe.column_headers_list_Xholdout

        return DataFrame(self._pdcoe.X_holdout, columns=columns), self._pdcoe.y_holdout

    def summary(self) -> 'DataFrame':
        """
        Prints AutoPipelineOptimizer Pipelines details (autoai trained pipelines).

        Returns
        -------
        Pandas DataFrame with computed pipelines and ML metrics.

        Example
        -------
        >>> from watson_machine_learning_client.experiment import AutoAI
        >>> experiment = AutoAI()
        >>> local_optimizer = experiment.optimizer()
        >>>
        >>> local_optimizer.summary()
                           training_normalized_gini_coefficient  ...  training_f1
            Pipeline Name                                        ...
            Pipeline_3                                 0.359173  ...     0.449197
            Pipeline_4                                 0.359173  ...     0.449197
            Pipeline_1                                 0.358124  ...     0.449057
            Pipeline_2                                 0.358124  ...     0.449057
        """
        score_names = [f"training_{name}" for name in
                       self._computed_pipelines_details['Pipeline0']['Score']['training']['scores'].keys()]
        columns = (['Pipeline Name', 'Number of enhancements'] + score_names)
        values = []

        for name, pipeline in self._computed_pipelines_details.items():
            pipeline_name = f"Pipeline_{name[-1]}"
            num_enhancements = len(pipeline['CompositionSteps']) - 5
            scores = [score for score in pipeline['Score']['training']['scores'].values()]
            values.append([pipeline_name, num_enhancements] + scores)

        pipelines = DataFrame(data=values, columns=columns)
        pipelines.drop_duplicates(subset="Pipeline Name", keep='first', inplace=True)
        pipelines.set_index('Pipeline Name', inplace=True)

        if (MetricsToDirections[self._pdcoe.scorer_for_ranking.upper()].value ==
                Directions.ASCENDING):
            return pipelines.sort_values(by=[f"training_{self._pdcoe.scorer_for_ranking}"], ascending=False).rename({
                f"training_{self._pdcoe.scorer_for_ranking}": f"training_{self._pdcoe.scorer_for_ranking}_(optimized)"},
                axis='columns')

        else:
            return pipelines.sort_values(by=[f"training_{self._pdcoe.scorer_for_ranking}"]).rename({
                f"training_{self._pdcoe.scorer_for_ranking}": f"training_{self._pdcoe.scorer_for_ranking}_(optimized)"},
                axis='columns')

    def get_pipeline_details(self, pipeline_name: str = None) -> dict:
        """
        Fetch specific pipeline details, eg. steps etc.

        Parameters
        ----------
        pipeline_name: str, optional
            Pipeline name eg. Pipeline_1, if not specified, best pipeline parameters will be fetched

        Returns
        -------
        Dictionary with pipeline parameters.

        Example
        -------
        >>> from watson_machine_learning_client.experiment import AutoAI
        >>> experiment = AutoAI()
        >>> local_optimizer = experiment.optimizer()
        >>>
        >>> pipeline_details = local_optimizer.get_pipeline_details(pipeline_name="Pipeline_1")
        """
        if self._pdcoe is None:
            raise FitNeeded(reason="To list computed pipelines parameters, "
                                   "first schedule a fit job by using a fit() method.")

        if pipeline_name is None:
            pipeline_name = self.summary().index[0]

        pipeline_name = pipeline_name.replace('_', '')

        pipeline_parameters = {
            "composition_steps": self._computed_pipelines_details[pipeline_name]['CompositionSteps'].values(),
            "pipeline_nodes": [node['op'] for node in
                               self._computed_pipelines_details[pipeline_name]['Params']['pipeline']['nodes'].values()],
        }

        return pipeline_parameters

    def get_pipeline(self,
                     pipeline_name: str,
                     astype: 'PipelineTypes' = PipelineTypes.LALE) -> Union['Pipeline', 'TrainablePipeline']:
        """
        Get specified computed pipeline.

        Parameters
        ----------
        pipeline_name: str, optional
            Pipeline name, if you want to see the pipelines names, please use summary() method.
            If this parameter is None, the best pipeline will be fetched.

        astype: PipelineTypes, optional
            Type of returned pipeline model. If not specified, lale type is chosen.

        Returns
        -------
        Scikit-Learn pipeline or Lale TrainablePipeline.

        See also
        --------
        LocalAutoPipelines.summary()

        Example
        -------
        >>> from watson_machine_learning_client.experiment import AutoAI
        >>> experiment = AutoAI()
        >>> local_optimizer = experiment.optimizer()
        >>>
        >>> pipeline_1 = local_optimizer.get_pipeline(pipeline_name='Pipeline_1')
        >>> pipeline_2 = local_optimizer.get_pipeline(pipeline_name='Pipeline_1', astype=PipelineTypes.LALE)
        >>> pipeline_3 = local_optimizer.get_pipeline(pipeline_name='Pipeline_1', astype=PipelineTypes.SKLEARN)
        >>> type(pipeline_3)
            <class 'sklearn.pipeline.Pipeline'>

        """

        if self._pdcoe is None:
            raise FitNeeded(reason="To get computed pipeline, "
                                   "first schedule a fit job by using a fit() method.")

        pipeline_name = pipeline_name.replace('_', '')

        pipeline_model = self._computed_pipelines_details[pipeline_name]['Model']

        if astype == PipelineTypes.SKLEARN:
            return pipeline_model

        elif astype == PipelineTypes.LALE:
            try_import_lale()
            from lale.helpers import import_from_sklearn_pipeline
            return import_from_sklearn_pipeline(pipeline_model)

        else:
            raise ValueError('Incorrect value of \'astype\'. '
                             'Should be either PipelineTypes.SKLEARN or PipelineTypes.LALE')

    def predict(self, X: Union['DataFrame', 'ndarray']) -> 'ndarray':
        """
        Predict method called on top of the best computed pipeline.

        Parameters
        ----------
        X: numpy.ndarray or pandas.DataFrame, required
            Test data for prediction.

        Returns
        -------
        Numpy ndarray with model predictions.

        Example
        -------
        >>> from watson_machine_learning_client.experiment import AutoAI
        >>> experiment = AutoAI()
        >>> local_optimizer = experiment.optimizer()
        >>>
        >>> predictions = local_optimizer.predict(X=test_data)
        """
        if isinstance(X, DataFrame) or isinstance(X, ndarray):
            if self.best_pipeline:
                return self.best_pipeline.predict(X if isinstance(X, ndarray) else X.values)
            else:
                raise FitNeeded("To list computed pipelines parameters, "
                                "first schedule a fit job by using a fit() method.")
        else:
            raise TypeError("X should be either of type pandas.DataFrame or numpy.ndarray")

    # TODO: expose more parameters to the user
    def _train(self, train_x: 'DataFrame', train_y: 'Series') -> 'PrepDaubCogOptEstimator':
        """
        Prepare and run PDCOE optimizer/estimator.

        Parameters
        ----------
        train_x: pandas.DataFrame, required
            Training dataset.

        train_y: pandas.Series, required
            Target values.

        Returns
        -------
        PrepDaubCogOptEstimator
        """
        # Disable printing to suppress warnings from ai4ml
        with redirect_stdout(open(os.devnull, "w")):
            from ai4ml.joint_optimizers.prep_daub_cog_opt import PrepDaubCogOptEstimator
            from ai4ml.utils.ai4ml_status import StatusMessageHandler

        filterwarnings("ignore")
        message_handler_with_progress_bar = LocalTrainingMessageHandler()
        train_id = str(uuid.uuid4())

        self.logger.debug(f"train_id: {train_id} --- Preparing started at: {strftime(DATE_FORMAT, gmtime())}")

        pdcoe_signature = signature(PrepDaubCogOptEstimator)

        # note: prepare estimator parameters
        estimator_parameters = {
            'learning_type': (PredictionType.REGRESSION if self.params['prediction_type'] == PredictionType.REGRESSION
                              else PredictionType.CLASSIFICATION),
            'run_cognito_flag': True,
            'show_status_flag': True,
            'status_msg_handler': StatusMessageHandler(
                job_id=train_id, handle_func=message_handler_with_progress_bar.on_training_message),
            'compute_feature_importances_flag': self.params.get('compute_feature_importances_flag', True),
            # TODO: expose this parameter to the user
            'compute_feature_importances_options': ['pipeline'],
            'compute_pipeline_notebooks_flag': False,
            'max_num_daub_ensembles': self.params['max_num_daub_ensembles']
        }

        if pdcoe_signature.parameters.get('target_label_name') is not None:
            estimator_parameters['target_label_name'] = self.params['prediction_column']

        if 'CPU' in os.environ:
            try:
                self.logger.debug(f"train_id: {train_id} --- Using {os.environ.get('CPU', 1)} CPUs")
                # TODO: expose this parameter to the user
                estimator_parameters['cpus_available'] = int(self.params.get('cpus_available',
                                                                             os.environ.get('CPU', 1)))
            except Exception as e:
                self.logger.error(f"Fail setting CPUs ({e}) {traceback.format_exc()}")
        # --- end note

        pdcoe = PrepDaubCogOptEstimator(**estimator_parameters)
        self.logger.debug(f"{train_id} --- Training started at: {strftime(DATE_FORMAT, gmtime())}")

        # Disable printing to suppress warnings from ai4ml
        with redirect_stdout(open(os.devnull, "w")):
            pdcoe.fit(train_x, train_y.values)

        if message_handler_with_progress_bar.progress_bar is not None:
            message_handler_with_progress_bar.progress_bar.last_update()
            message_handler_with_progress_bar.progress_bar.close()

        else:
            message_handler_with_progress_bar.progress_bar_2.last_update()
            message_handler_with_progress_bar.progress_bar_2.close()
            message_handler_with_progress_bar.progress_bar_1.last_update()
            message_handler_with_progress_bar.progress_bar_1.close()

        self.logger.debug(f"{train_id} --- End training at: {strftime(DATE_FORMAT, gmtime())}")
        return pdcoe
