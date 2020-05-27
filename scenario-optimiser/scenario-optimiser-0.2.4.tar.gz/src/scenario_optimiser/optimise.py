import logging

from .prepare.constraints import calculate_constraint_values_and_bounds
from .linear_programming_optimiser import optimise_scenarios_with_linear_programming
from .linear_programming_optimiser import errors
from .linear_interpolator.interpolate_scenarios import \
    (linear_interpolate, interpolate_all_metrics)
from .gradient_optimiser.optimise_gradient import optimise_scenarios_with_gradient_method
from .mixed_integer_programming.mip_optimiser import optimise_scenarios_with_mip


log = logging.getLogger(__name__)


def optimise_scenarios(scenarios, settings, method=None):
    """
    Optimisation function that - if method is not specifically entered - first tries
    to use a linear programming solution. If the constraint vs maximise metrics is
    not a concave function (so no diminishing returns), a gradient method will
    be used to find an optimal solution.

    The function will return the results, which includes a data frame with the
    interpolated values of all provided metrics

    :param scenarios
    Dictionary of numpy arrays containing estimates of metrics in different scenarios

    :param settings
    Dictionary at least containing the key values for the constraint_metric,
    maximise_metric and identifier so they can be selected from the scenarios
    and the constraint value

    :param method
    Indicate whether to use linear programming or gradient method to optimize

    :return: result
    Dictionary with the result of the optimisation: a message, total optimised value,
    success status, constraint metric values and a data frame containing the
    metric values per identifier as a result of the optimization
    """

    _validate_inputs_settings(scenarios, settings, method)
    constraint_metric_name = settings.get('constraint_metric')
    constraint_value = settings.get('constraint_value')

    constraint = calculate_constraint_values_and_bounds(
        scenarios.get(constraint_metric_name), constraint_value)

    if constraint.get('status') == 'ok':
        optimised = _run_optimiser(scenarios, settings, method)

    else:
        optimised = _get_bounded_results(scenarios, settings, constraint)

    optimised['data_frame'] = _interpolate_results(scenarios, settings,
                                                   optimised)
    optimised['method'] = method

    return optimised


def _validate_inputs_settings(scenarios, settings, method):
    methods = (None, 'linear', 'gradient', 'mip')

    if method not in methods:
        raise KeyError('Method %s is not supported' % method)

    if not isinstance(scenarios, dict):
        raise TypeError(
            'Scenarios should be provided as a dictionary with numpy arrays')

    if not isinstance(settings, dict):
        raise TypeError('Settings should be provided as a dictionary')

    mandatory_settings = [
        'constraint_metric', 'constraint_value', 'maximise_metric',
        'identifier'
    ]
    missing_settings = [
        sett for sett in mandatory_settings if sett not in settings.keys()
    ]

    if missing_settings:
        raise KeyError('Missing following settings: %s' % missing_settings)

    mandatory_scenarios_keys = [
        settings[key] for key in mandatory_settings
        if key != 'constraint_value'
    ]
    scenario_keys = list(scenarios.keys())

    missing_keys = [
        key for key in mandatory_scenarios_keys if key not in scenario_keys
    ]

    if missing_keys:
        raise KeyError(
            'Missing the following keys in scenarios: %s' % missing_keys)

    return True


def _get_optimisation_input(scenarios, settings):
    maximise_metric_key = settings.get('maximise_metric')
    constraint_metric_key = settings.get('constraint_metric')
    constraint_value = settings.get('constraint_value')

    to_maximise_metric = scenarios[maximise_metric_key]
    constraint_metric = scenarios[constraint_metric_key]
    return {
        'to_maximise_metric': to_maximise_metric,
        'constraint_metric': constraint_metric,
        'constraint_value': constraint_value
    }


def _run_optimiser(scenarios, settings, method):

    if method == 'linear':
        log.info('Optimising using linear programming...')
        return optimise_scenarios_with_linear_programming(scenarios, settings)

    if method == 'gradient':
        log.info('Optimising using gradient method...')
        return optimise_scenarios_with_gradient_method(scenarios, settings)

    if method == 'mip':
        log.info('Optimising using mixed integer programming...')
        return optimise_scenarios_with_mip(scenarios, settings)

    try:
        log.info('Trying linear programming solution')
        return optimise_scenarios_with_linear_programming(scenarios, settings)

    except errors.ScenariosNotConcaveError as e:
        log.info(e)
        log.info('Optimise using gradient method...')
        return optimise_scenarios_with_gradient_method(scenarios, settings)


def _get_bounded_results(scenarios, settings, constraint):
    from_metric = settings.get('constraint_metric')
    to_metric = settings.get('maximise_metric')
    constraint_metric_values = constraint.get('bounded_values')
    maximised_result = linear_interpolate(scenarios, from_metric, to_metric,
                                          constraint_metric_values)

    return {
        'message': constraint.get('message'),
        'maximised_result': maximised_result.sum(),
        'success': False,
        'constraint_metric_values': constraint_metric_values,
        'iterations': 0
    }


def _interpolate_results(scenarios, settings, optimised):
    return interpolate_all_metrics(scenarios, settings['constraint_metric'],
                                   settings['identifier'],
                                   optimised['constraint_metric_values'])
