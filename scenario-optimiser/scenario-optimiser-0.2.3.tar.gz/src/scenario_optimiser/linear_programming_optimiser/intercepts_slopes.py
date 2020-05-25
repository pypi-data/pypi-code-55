import numpy as np

MIN_TOLERANCE = 0.0000000001


def calculate_intercepts_and_slopes(scenarios, constraint_metric, maximise_metric):
    values = _get_scenario_points_and_deltas(
        scenarios, constraint_metric, maximise_metric
    )
    slopes = _calculate_slopes(values)
    intercepts = _calculate_intercepts(values, slopes)
    return intercepts, slopes


def _get_scenario_points_and_deltas(scenarios, constraint_metric, maximise_metric):
    values = {}
    name_dict = {constraint_metric: "x", maximise_metric: "y"}
    for metric in [constraint_metric, maximise_metric]:
        name = name_dict[metric]
        values[name + "_low"] = scenarios.get(metric)
        values[name + "_high"] = _shift_array_to_right(values[name + "_low"])
        values[name + "_delta"] = values[name + "_high"] - values[name + "_low"]
    return values


def _shift_array_to_right(array):
    next_array = array[:, 1:]
    added_col = array[:, -1].reshape(-1, 1)
    return np.concatenate((next_array, added_col), axis=1)


def _calculate_slopes(values):
    delta_x = values["x_delta"]
    delta_x_zero = delta_x == 0
    delta_x[delta_x_zero] = 0.01
    slopes = values["y_delta"] / delta_x
    slopes[delta_x_zero] = 0.0
    return slopes


def _calculate_intercepts(values, slopes):
    return values["y_low"] - slopes * values["x_low"]


def scenarios_concave(slopes):
    """slope[y, x] should always be higher than or equal to slope[y, x+1]"""
    next_slopes = _shift_array_to_right(slopes)
    concave = np.array(slopes >= next_slopes - MIN_TOLERANCE)
    # pylint: disable=unsubscriptable-object
    true_column = np.ones((concave.shape[0], 1), dtype=bool)
    return np.concatenate((true_column, concave[:, :-1]), axis=1)
