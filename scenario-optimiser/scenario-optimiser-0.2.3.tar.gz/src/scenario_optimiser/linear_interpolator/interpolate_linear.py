import numpy as np


class LinearInterpolator:

    """
    Linear interpolator for a 2d-array
    """

    def __init__(self, scenarios):
        self.scenarios = scenarios

    def get(self, from_metric, metric_values, to_metric):
        verified_metric_values = self._verify_metric_values_are_in_scenario_range(
            from_metric, metric_values)
        positions = self._look_up_positions_in_scenarios(
            from_metric, metric_values)
        scenarios = self._calculate_scenarios_values(
            from_metric, verified_metric_values, positions, to_metric)
        return self._calculate_to_metric_values(from_metric, to_metric,
                                                scenarios)

    def _verify_metric_values_are_in_scenario_range(self, metric, values):
        scenarios = self.scenarios.get(metric)
        max_values = np.max(scenarios, axis=1, keepdims=True)
        min_values = np.min(scenarios, axis=1, keepdims=True)
        return np.minimum(max_values, np.maximum(values, min_values))

    def _look_up_positions_in_scenarios(self, metric, values):
        values = values.reshape(-1, 1)
        scenarios = self.scenarios.get(metric)
        mask = scenarios <= values
        return np.sum(mask, axis=1, keepdims=True) - 1

    def _calculate_scenarios_values(self, from_metric, from_metric_values,
                                    positions, to_metric):
        positions_higher = self._get_positions_above_current(
            from_metric, positions)
        scenarios = dict()

        for metric in [to_metric, from_metric]:
            metric_scenarios = self.scenarios.get(metric)
            scenarios_low = self._get_values_by_position(metric_scenarios, positions)
            scenarios_high = self._get_values_by_position(
                metric_scenarios, positions_higher)

            scenarios[metric + '_low'] = scenarios_low
            scenarios[metric + '_range'] = scenarios_high - scenarios_low

        scenarios[from_metric +
                  '_position'] = np.squeeze(from_metric_values) - scenarios_low

        return scenarios

    def _get_positions_above_current(self, metric, positions):
        scenarios = self.scenarios.get(metric)
        columns = scenarios.shape[1]
        positions_higher = positions + 1
        positions_higher[positions_higher > columns - 1] = columns - 1
        return positions_higher

    @staticmethod
    def _get_values_by_position(scenarios, positions):
        row_indices = list(np.arange(scenarios.shape[0]))
        column_indices = list(np.squeeze(positions, axis=1))
        return scenarios[row_indices, column_indices]

    def _calculate_to_metric_values(self, from_metric, to_metric, scenarios):
        base_values = self._get_lowest_values(scenarios, to_metric)
        slopes = self._calculate_slopes_of_to_metric(scenarios, from_metric,
                                                     to_metric)
        positions = self._get_from_metric_positions(scenarios, from_metric)
        return base_values + slopes * positions

    @staticmethod
    def _get_lowest_values(scenarios, to_metric):
        return scenarios[to_metric + '_low']

    @staticmethod
    def _calculate_slopes_of_to_metric(scenarios, from_metric, to_metric):
        from_metric_scenario_range = scenarios[from_metric + '_range']
        to_metric_scenario_range = scenarios[to_metric + '_range']

        no_zeros_from_metric_scenario_range = from_metric_scenario_range.copy()
        no_zeros_from_metric_scenario_range[from_metric_scenario_range ==
                                            0] = 1

        slopes = to_metric_scenario_range / no_zeros_from_metric_scenario_range
        slopes[from_metric_scenario_range == 0] = 0
        return slopes

    @staticmethod
    def _get_from_metric_positions(scenarios, from_metric):
        return scenarios[from_metric + '_position']
