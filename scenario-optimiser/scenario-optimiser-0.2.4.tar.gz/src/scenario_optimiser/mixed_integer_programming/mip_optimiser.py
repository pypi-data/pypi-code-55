from collections import namedtuple
import numpy as np
from mip import Model, xsum, maximize, BINARY, CONTINUOUS, LinExpr

from scenario_optimiser.mixed_integer_programming.piecewise_linear import (
    PiecewiseLinearFunction,
)


def optimise_scenarios_with_mip(scenarios, settings):
    constraint_metric = settings.get("constraint_metric")
    optimise_metric = settings.get("maximise_metric")
    constraint_value = settings.get("constraint_value")
    plfs = _to_piecewise_linear_funcs(scenarios, constraint_metric, optimise_metric)
    plfs = list(plfs)
    optimum = maximize_sum(plfs, constraint_value)
    return _summarize_optimized_result(optimum)


def _to_piecewise_linear_funcs(scenarios, constraint_metric, optimise_metric):
    constraint_metric_values = scenarios.get(constraint_metric)
    optimise_metric_values = scenarios.get(optimise_metric)
    n_rows = constraint_metric_values.shape[0]
    for row_idx in range(n_rows):
        row = (constraint_metric_values[row_idx, :], optimise_metric_values[row_idx, :])
        constraint_values, optimise_values = _get_unique_values(row)
        yield PiecewiseLinearFunction(constraint_values, optimise_values)


def _get_unique_values(row):
    """The algorithm goes much faster if we remove any duplicate values in the
    bid landscapes (needed to have the same number of columns per identifier to
    support the gradient method)"""
    unique_constraint_values = np.unique(row[0])
    if len(unique_constraint_values) < 2:
        return row[0][:2], row[1][:2]
    indices = [int(np.where(value == unique_constraint_values)[0]) for value in row[0]]
    unique_indices = list(set(indices))
    unique_maximise_values = row[1][unique_indices]
    return unique_constraint_values, unique_maximise_values


def _summarize_optimized_result(optimum):
    opt_total_result = sum([line.revenue for line in optimum])
    opt_constraint_metric_values = np.array([line.cost for line in optimum])
    return {
        "message": "optimisation completed successfully",
        "maximised_result": opt_total_result,
        "success": True,
        "constraint_metric_values": opt_constraint_metric_values,
        "iterations": 1,
    }


Line = namedtuple("Line", ["cost", "revenue", "plf"])


def maximize_sum(plfs, max_costs, print_logs=False):
    # pylint: disable=too-many-locals
    m = Model("bid-landscapes")
    m.solver.set_verbose(1 if print_logs else 0)
    costs = LinExpr()
    objective = LinExpr()
    xs = []
    ws = []
    for (_, plf) in enumerate(plfs):
        k = len(plf)
        w = [m.add_var(var_type=CONTINUOUS) for _ in range(0, k)]
        x = [m.add_var(var_type=BINARY) for _ in range(0, k - 1)]
        xs.append(x)
        ws.append(w)

        m += xsum(w[i] for i in range(0, k)) == 1
        for i in range(0, k):
            m += w[i] >= 0

        m += w[0] <= x[0]
        for i in range(1, k - 1):
            m += w[i] <= x[i - 1] + x[i]
        m += w[k - 1] <= x[k - 2]
        m += xsum(x[k] for k in range(0, k - 1)) == 1

        for i in range(0, k):
            costs.add_term(w[i] * plf.a[i])
            objective.add_term(w[i] * plf.b[i])

    m += costs <= max_costs
    m.objective = maximize(objective)
    m.optimize()

    optimum = []
    for (i, plf) in enumerate(plfs):
        k = len(plf)
        u_i = sum(ws[i][j].x * plf.a[j] for j in range(0, k))
        v_i = sum(ws[i][j].x * plf.b[j] for j in range(0, k))
        optimum.append(Line(cost=u_i, revenue=v_i, plf=plf))
    return optimum
