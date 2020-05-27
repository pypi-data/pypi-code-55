import numpy as np
import pandas as pd

INDEX_COLUMN = 'index_'


def data_frame_to_dict_of_arrays(data_frame, identifier, constraint):
    scenarios = dict()
    deduplicated = data_frame.groupby([identifier, constraint]).mean().reset_index()

    deduplicated[INDEX_COLUMN] = _calculate_index(deduplicated, identifier, constraint)
    metrics = _get_metrics(deduplicated, identifier)
    for metric in metrics:
        pivot = _pivot_data_frame_by_metric(deduplicated, metric, identifier)
        scenarios[metric] = np.array(pivot)

    scenarios[identifier] = np.array(
        _pivot_data_frame_by_metric(deduplicated, constraint, identifier).index)
    return scenarios


def _calculate_index(data_frame, identifier, constraint):
    data_frame = data_frame.sort_values(by=[identifier, constraint]).reindex()
    return data_frame.groupby(identifier).cumcount()


def _get_metrics(data_frame, identifier):
    metrics = _get_numerical_data_frame_columns(data_frame)
    return _get_metrics_not_identifier_or_index(metrics, identifier)


def _get_numerical_data_frame_columns(data_frame):
    return [
        col for col in data_frame.columns
        if data_frame[col].dtype in ('int64', 'float64')
    ]


def _get_metrics_not_identifier_or_index(metrics, identifier):
    return [metric for metric in metrics if metric not in (identifier, INDEX_COLUMN)]


def _pivot_data_frame_by_metric(data_frame, column, identifier):
    pivot = pd.pivot_table(data_frame, index=identifier, values=column,
                           columns=INDEX_COLUMN, aggfunc=np.sum)
    return pivot.fillna(method='ffill', axis=1)
