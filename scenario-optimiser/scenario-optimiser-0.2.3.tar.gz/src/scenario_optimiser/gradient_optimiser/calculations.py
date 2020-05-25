import numpy as np


def interpolate_y_values(scenarios, x_values, settings):
    interpolator = settings.get("interpolator")
    return interpolator(scenarios).get(
        from_metric=settings.get("constraint_metric"),
        metric_values=x_values.reshape(-1, 1),
        to_metric=settings.get("maximise_metric"),
    )


def calculate_all_slopes(scenarios, state, settings):
    step_size = state.get("step_size")
    step_direction = {"down": -step_size, "up": step_size}
    marginal_revenues = dict()
    for direction, step_ in step_direction.items():
        marginal_revenues[direction] = calculate_slopes(
            scenarios, step_, state, settings
        )
    return marginal_revenues


def calculate_slopes(scenarios, step, state, settings):
    x_scenarios = scenarios.get(settings.get("constraint_metric"))
    x_values = state.get("x_values")
    y_values = state.get("y_values")
    x_new = _add_step_to_x_values(x_values, step)
    x_new_bounded = _replace_x_values_outside_scenarios_with_zero(x_new, x_scenarios)
    y_new = interpolate_y_values(scenarios, x_new_bounded, settings)
    slopes = (y_new - y_values) / step
    return _correct_slopes_when_bounded(x_new_bounded, slopes, step)


def _add_step_to_x_values(x_values, step):
    return x_values + step


def _replace_x_values_outside_scenarios_with_zero(x_values, x_scenarios):
    x_bounded = x_values.copy()
    min_bound_condition = x_values < x_scenarios[:, 0]
    max_bound_condition = x_values > x_scenarios[:, -1]
    x_bounded[min_bound_condition | max_bound_condition] = 0
    return x_bounded


def _correct_slopes_when_bounded(x_bounded, slopes, step):
    step_direction = "up" if step > 0 else "down"
    correct_values = {"up": 0, "down": np.inf}
    bounded_values = x_bounded == 0
    slopes[bounded_values] = correct_values[step_direction]
    return slopes
