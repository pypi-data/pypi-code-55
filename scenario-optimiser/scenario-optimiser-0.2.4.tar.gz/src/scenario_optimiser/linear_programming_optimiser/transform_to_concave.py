from copy import deepcopy
import numpy as np
from scipy.optimize import minimize, LinearConstraint


def transform_to_concave(scenarios, constraint_metric, optimise_metric):
    concave_scenarios = deepcopy(scenarios)
    concave_optimise_metric, mse_deviation = _calculate_concave_scenarios(
        scenarios[constraint_metric], scenarios[optimise_metric]
    )
    concave_scenarios[optimise_metric] = concave_optimise_metric

    return {
        "concave_scenarios": concave_scenarios,
        "mse_deviation": mse_deviation,
    }


def _calculate_concave_scenarios(constraint_metric_values, to_maximise_metric_values):
    n_rows, n_cols = constraint_metric_values.shape
    concave_values = np.zeros(to_maximise_metric_values.shape)
    mse_deviation = np.zeros((n_rows,))
    for row_idx in range(n_rows):
        result = _calculate_concave_scenario(
            constraint_metric_values[row_idx, :], to_maximise_metric_values[row_idx, :]
        )
        concave_values[row_idx, :] = _add_concave_values(
            n_cols, result["concave_values"]
        )
        mse_deviation[row_idx] = result["mse_deviation"]
    return concave_values, mse_deviation


def _calculate_concave_scenario(x_values, y_values):
    x_trimmed, y_trimmed = _trim(x_values, y_values)
    y_diff = np.array([0])
    if _too_few_bid_landscape_points(x_trimmed):
        return {"concave_values": y_values, "mse_deviation": y_diff}
    result = _compute_concave_points(x_trimmed, y_trimmed)
    concave_y_values = _get_untrimmed_values(x_values, x_trimmed, result)
    return {"concave_values": concave_y_values, "mse_deviation": round(result.fun, 2)}


def _trim(x_values, y_values):
    x_unique, unique_indices = np.unique(x_values, return_index=True)
    return x_unique, y_values[unique_indices]


def _too_few_bid_landscape_points(x_trimmed):
    return x_trimmed.shape[0] < 3


def _compute_concave_points(x, y):
    y_pred_0 = np.zeros(y.shape)
    return minimize(
        lambda y_pred: _objective(y_pred, y),
        y_pred_0,
        constraints=[
            _compute_increase_constraint(y_pred_0),
            _compute_concave_constraint(x),
        ],
    )


def _objective(y_pred, y):
    return np.mean(np.square(y_pred - y))


def _compute_concave_constraint(constraint_metric_values):
    a = constraint_metric_values.copy()
    n_columns = a.shape[0]
    n_rows = n_columns - 2
    new_array = np.zeros((n_rows, n_columns))

    for row_idx in range(n_rows):
        new_array[row_idx, row_idx] = -1 / (a[row_idx + 1] - a[row_idx])
        new_array[row_idx, row_idx + 1] = 1 / (a[row_idx + 1] - a[row_idx]) + 1 / (
            a[row_idx + 2] - a[row_idx + 1]
        )
        new_array[row_idx, row_idx + 2] = -1 / (a[row_idx + 2] - a[row_idx + 1])

    return LinearConstraint(new_array, [0] * n_rows, [np.inf] * n_rows)


def _compute_increase_constraint(x):
    n_columns = x.shape[0]
    n_rows = n_columns - 1
    new_array = np.zeros((n_rows, n_columns))

    for row_idx in range(n_rows):
        new_array[row_idx, row_idx] = -1
        new_array[row_idx, row_idx + 1] = 1

    return LinearConstraint(new_array, [0] * n_rows, [np.inf] * n_rows)


def _add_concave_values(n_cols, concave_values):
    n_values = concave_values.shape[0]
    last_value = concave_values[-1]
    if n_values < n_cols:
        extra_values = np.repeat(last_value, n_cols - n_values)
        return np.concatenate((concave_values, extra_values))
    return concave_values


def _get_untrimmed_values(x_values, x_trimmed, result):
    concave_values = []
    trimmed_concave_values = result.x
    for x_value in x_values:
        mask = x_trimmed == x_value
        concave_values.append(trimmed_concave_values[mask][0])
    return np.array(concave_values)
