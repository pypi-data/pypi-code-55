import pandas as pd
from scenario_optimiser.linear_interpolator.interpolate_linear import LinearInterpolator


def interpolate_all_metrics(scenarios, constraint_metric, identifier_metric,
                            constraint_values):
    if constraint_values is None:
        return None

    metrics = _get_metrics(scenarios, identifier_metric)
    data_frame = pd.DataFrame(
        columns=[identifier_metric], data=scenarios.get(identifier_metric))

    for metric in metrics:
        metric_interpolations = linear_interpolate(
            scenarios, constraint_metric, metric, constraint_values)
        data_frame[metric] = metric_interpolations.flatten()

    return data_frame


def _get_metrics(scenarios, identifier_metric):
    return [key for key in scenarios.keys() if key != identifier_metric]


def linear_interpolate(scenarios, x, y, x_new):
    x_new = x_new.reshape(-1, 1)
    interpolator = LinearInterpolator(scenarios)
    output = interpolator.get(x, x_new, y)
    return output.reshape(-1, 1)
