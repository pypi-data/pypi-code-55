import numpy as np

TOLERANCE = 0.0001


def randomly_initialise_values(scenarios, target_total_value):
    """
    Randomly selects values between the minimum and maximum values of scenarios
    with the total sum of values matching the target value
    """

    min_values = scenarios[:, 0]
    max_values = scenarios[:, -1]

    values = _get_random_values(min_values, max_values)
    modifier = _calculate_modifier(values, target_total_value)

    while abs(modifier - 1) > TOLERANCE:
        values = _adjust_values(values, modifier)
        values = _ensure_values_stay_within_limits(values, min_values, max_values)
        modifier = _calculate_modifier(values, target_total_value)
    return values


def _get_random_values(min_values, max_values):
    return np.random.uniform(min_values, max_values)


def _calculate_modifier(values, target_total_value):
    return target_total_value / np.sum(values)


def _adjust_values(old_values, modifier):
    return old_values * modifier


def _ensure_values_stay_within_limits(
        values, min_values, max_values):
    max_bounded_values = np.minimum(values, max_values)
    return np.maximum(max_bounded_values, min_values)
