import logging
import numpy as np
from scipy.optimize import linprog
from .intercepts_slopes import calculate_intercepts_and_slopes, scenarios_concave

from .errors import ScenariosNotConcaveError


log = logging.getLogger(__name__)


def optimise_scenarios_with_linear_programming(scenarios, settings):
    """
    x = vector of constraint metric values and objective metric values
    Objective: minimize c transposed * x
    Subject to: Ax <= b and x between x_min and x_max
    """

    intercepts, slopes = calculate_intercepts_and_slopes(
        scenarios, settings["constraint_metric"], settings["maximise_metric"]
    )

    if not scenarios_concave(slopes).all():
        raise ScenariosNotConcaveError("Scenarios are not concave")

    log.debug("Scenarios are concave, proceeding with linear programming solution")

    rows, cols = slopes.shape
    c = _get_linear_objective_coefficients(rows)
    A_ub = _calculate_inequality_matrix(slopes, rows, cols)
    b_ub = _calculate_inequality_vector(scenarios, settings, intercepts, rows, cols)
    A_eq = _get_equality_constraint_params(rows)
    b_eq = settings.get("constraint_value")
    result = linprog(c, A_ub, b_ub, A_eq, b_eq)
    return {
        "message": result["message"],
        "maximised_result": -result["fun"],
        "success": result["success"],
        "constraint_metric_values": result["x"][:rows],
        "iterations": result["nit"],
    }


def _get_linear_objective_coefficients(rows):
    return np.concatenate((np.zeros((rows,)), -np.ones((rows,))), axis=0)


def _calculate_inequality_matrix(slopes, rows, cols):
    identity_matrix = np.identity(rows)
    left_upper = np.concatenate((identity_matrix, -identity_matrix), axis=0)
    right_upper = np.zeros((2 * rows, rows))
    left_bottom, right_bottom = _calculate_inequality_parameters(slopes, rows, cols)
    upper = np.concatenate((left_upper, right_upper), axis=1)
    lower = np.concatenate((left_bottom, right_bottom), axis=1)
    return np.concatenate((upper, lower), axis=0)


def _calculate_inequality_parameters(slopes, rows, cols):
    scenarios_slope_params = np.zeros((rows * cols, rows))
    scenarios_intercept_params = np.zeros((rows * cols, rows))
    for r in np.arange(0, rows):
        for c in np.arange(0, cols):
            row = r * cols + c
            scenarios_slope_params[row, r] = -slopes[r, c]
            scenarios_intercept_params[row, r] = 1
    return scenarios_slope_params, scenarios_intercept_params


def _calculate_inequality_vector(scenarios, settings, intercepts, rows, cols):
    x_min, x_max = _calculate_min_and_max_values_constraint_metric(scenarios, settings)
    top = np.concatenate((x_max, -x_min), axis=0)
    intercepts_vector = np.zeros((rows * cols, 1))
    for k in np.arange(0, rows):
        for j in np.arange(0, cols):
            row = k * cols + j
            intercepts_vector[row] = intercepts[k, j]
    return np.concatenate((top, intercepts_vector), axis=0)


def _calculate_min_and_max_values_constraint_metric(scenarios, settings):
    constraint_metric = settings.get("constraint_metric")
    return (
        np.min(scenarios.get(constraint_metric), axis=1, keepdims=True),
        np.max(scenarios.get(constraint_metric), axis=1, keepdims=True),
    )


def _get_equality_constraint_params(rows):
    return np.concatenate((np.ones((1, rows)), np.zeros((1, rows))), axis=1)


def _get_constraint_value(settings):
    return np.array([settings.get("constraint_value")])
