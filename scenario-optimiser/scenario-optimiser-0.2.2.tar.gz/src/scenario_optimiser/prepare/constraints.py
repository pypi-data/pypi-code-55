import numpy as np


def calculate_constraint_values_and_bounds(constraint_scenarios, constraint_value):
    metric_scenarios = constraint_scenarios

    constraint = dict()
    constraint['value'] = constraint_value
    constraint['bounds'] = _get_total_bounds(metric_scenarios)
    constraint['status'] = _get_constraint_value_status(constraint)
    constraint['bounded_values'] = _get_bounded_values(constraint,
                                                       metric_scenarios)
    constraint['message'] = _get_message(constraint)
    return constraint


def _get_total_bounds(array):
    min_max_array = _get_row_bounds(array)
    return np.sum(min_max_array, axis=0)


def _get_row_bounds(metric_array):
    array = np.array(metric_array)
    lowest_values = array[:, 0].reshape(-1, 1)
    highest_values = array[:, -1].reshape(-1, 1)
    return np.concatenate((lowest_values, highest_values), axis=1)


def _get_constraint_value_status(constraint):
    if constraint['value'] > constraint['bounds'][1]:
        return 'too high'
    if constraint['value'] < constraint['bounds'][0]:
        return 'too low'
    return 'ok'


def _get_bounded_values(constraint, scenarios):
    if constraint['status'] == 'ok':
        return None

    idx = 0 if constraint['status'] == 'too low' else -1
    return _get_row_bounds(scenarios)[:, idx]


def _get_message(constraint):
    if constraint['status'] == 'ok':
        message = ""
    else:
        message = 'Constraint value {} is {} (should be between {})'.format(
            constraint['value'], constraint['status'], constraint['bounds'])
    return message
