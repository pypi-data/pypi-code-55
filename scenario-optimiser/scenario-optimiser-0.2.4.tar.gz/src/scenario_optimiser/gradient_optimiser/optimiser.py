from copy import deepcopy
import numpy as np
from .random_initialiser import randomly_initialise_values
from .calculations import interpolate_y_values, calculate_all_slopes


STEP_MULTIPLIER = {"up": 1, "down": -1}


def optimise_gradient(scenarios, settings):
    """
    Optimises scenarios using a gradient method.
    The optimisation starts with either randomly generated or entered constraint
    values that sum up to the total constraint value. From this point, the function
    looks at the possible revenue gains in each row of the scenarios with going one
    step up, and the possible loss by going one step down. If the most profitable step
    up gains more than the lowest loss of going a step down, this step is taken.
    If there's no step to take with more profit than loss, the step size will be
    decreased. This process continues until the minimum step size is reached.

    the function looks at the best step
    :param scenarios:
    dict with constraint metric x and optimisation metric y scenarios as numpy arrays
    :param settings:
    dict with 'max_iterations': default 50000,
    'initial_constraint_metric_values': default None,
    'min_step_size': default 0.000000005,
    'tolerance': 0.000000000001

    :return:
    dict with optimised constraint values and the total maximised value
    """

    max_iterations = settings.get("max_iterations")
    state = _initialise_state(scenarios, settings)

    for _ in range(max_iterations):
        state = _optimise_step(scenarios, state, settings)
        state["iteration"] += 1

        if _optimisation_complete(state, settings):
            break

    return state


def _initialise_state(scenarios, settings):
    state = dict()
    state["x_values"] = _get_or_calculate_initial_values(scenarios, settings)
    state["y_values"] = interpolate_y_values(scenarios, state.get("x_values"), settings)
    state["step_size"] = settings.get("step_size")
    state["y_total"] = state["y_values"].sum()
    state["iteration"] = 0
    state["slopes"] = calculate_all_slopes(scenarios, state, settings)
    return state


def _get_or_calculate_initial_values(scenarios, settings):
    if settings.get("initial_constraint_metric_values") is not None:
        return settings["initial_constraint_metric_values"]

    metric_scenarios = scenarios.get(settings.get("constraint_metric"))
    constraint_value = settings.get("constraint_value")
    return randomly_initialise_values(metric_scenarios, constraint_value)


def _optimise_step(scenarios, state, settings):
    slopes = state.get("slopes")
    new_state = deepcopy(state)

    if _possible_to_increase_y(slopes, settings):
        new_state = _re_allocate_and_calculate_new_state(scenarios, new_state, settings)

    if _y_total_did_not_increase(new_state, state, settings):
        new_state["step_size"] = _lower_step_size(state.get("step_size"))
        new_state["slopes"] = calculate_all_slopes(scenarios, new_state, settings)

    return new_state


def _possible_to_increase_y(slopes, settings):
    tolerance = settings["tolerance"]
    best_slopes = _get_best_slopes(slopes)
    return best_slopes["up"] > best_slopes["down"] + tolerance


def _get_best_slopes(slopes):
    return {"up": np.max(slopes["up"]), "down": np.min(slopes["down"])}


def _re_allocate_and_calculate_new_state(scenarios, new_state, settings):
    # Only re-calculate values from rows that have been changed
    new_state["x_values"], re_allocated = _re_allocate_constraint_metric(new_state)
    modified = _get_modified_values(scenarios, new_state, re_allocated)

    modified["y_values"] = _re_calculate_y_values(modified, settings)
    new_state["y_values"][re_allocated] = modified["y_values"]
    new_state["y_total"] = new_state["y_values"].sum()

    modified["slopes"] = _re_calculate_slopes(modified, new_state, settings)
    new_state["slopes"] = _fill_modified_slopes(new_state, modified, re_allocated)
    return new_state


def _re_allocate_constraint_metric(state):
    x_values = state.get("x_values")
    re_allocate = dict()
    for direction in ["up", "down"]:
        x_values, re_allocate[direction] = _re_allocate_direction(
            x_values, state, direction
        )
    re_allocation_mask = re_allocate["up"] | re_allocate["down"]
    return x_values, re_allocation_mask


def _re_allocate_direction(x_values, state, direction):
    step_size = state.get("step_size")
    re_allocate = _get_mask_of_best_step(state, direction)
    n_changes = np.sum(re_allocate)
    x_values[re_allocate] += STEP_MULTIPLIER[direction] * step_size / n_changes
    return x_values, re_allocate


def _get_mask_of_best_step(state, direction):
    best_slopes = _get_best_slopes(state.get("slopes"))
    return state.get("slopes")[direction] == best_slopes[direction].flatten()


def _get_modified_values(scenarios, new_state, re_allocated):
    modified = dict()
    modified["scenarios"] = {
        key: array[re_allocated] for key, array in scenarios.items()
    }
    modified["x_values"] = new_state["x_values"][re_allocated]
    return modified


def _re_calculate_y_values(modified, settings):
    return interpolate_y_values(
        modified.get("scenarios"), modified.get("x_values"), settings
    )


def _re_calculate_slopes(modified, state, settings):
    modified_state = {'step_size': state.get('step_size'),
                      'x_values': modified.get('x_values'),
                      'y_values': modified.get('y_values')}
    new_slopes = calculate_all_slopes(modified['scenarios'], modified_state, settings)
    return new_slopes


def _fill_modified_slopes(new_state, modified, re_allocated):
    for direction in ['up', 'down']:
        new_state['slopes'][direction][re_allocated] = modified['slopes'][direction]
    return new_state['slopes']


def _y_total_did_not_increase(new_state, old_state, settings):
    tolerance = settings["tolerance"]
    return not new_state.get("y_total") > old_state.get("y_total") + tolerance


def _lower_step_size(step):
    return step / 2


def _optimisation_complete(state, settings):
    return state.get("step_size") < settings.get("min_step_size")
