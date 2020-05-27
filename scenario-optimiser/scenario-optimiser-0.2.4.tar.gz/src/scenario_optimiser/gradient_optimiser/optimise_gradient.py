from scenario_optimiser.linear_interpolator.interpolate_linear import LinearInterpolator

from .default_gradient_settings import DEFAULT_SETTINGS
from .optimiser import optimise_gradient


def optimise_scenarios_with_gradient_method(scenarios, user_settings):
    """
    Use gradient method to optimise allocation
    """

    settings = _fill_missing_settings_with_defaults(user_settings)
    results = []

    for step_size in settings['step_sizes']:
        results += _optimise_with_step_size(step_size, scenarios, settings)

    best_result = _get_best_result(results)

    return {
        'message': 'optimisation completed successfully',
        'maximised_result': best_result['y_total'],
        'success': best_result['iteration'] > 0,
        'constraint_metric_values': best_result['x_values'],
        'iterations': best_result['iteration']
    }


def _fill_missing_settings_with_defaults(settings):
    new_settings = DEFAULT_SETTINGS.copy()
    new_settings.update(settings)
    return new_settings


def _optimise_with_step_size(step_size, scenarios, settings):
    results = []

    for _ in range(settings['num_tries']):
        results.append(_run_optimiser(step_size, scenarios, settings))

    return results


def _run_optimiser(step_size, scenarios, settings):
    settings['step_size'] = step_size
    settings['interpolator'] = LinearInterpolator
    return optimise_gradient(scenarios, settings)


def _get_best_result(results):
    max_result = max([result['y_total'] for result in results])
    return [result for result in results if result['y_total'] == max_result][0]
