"""
The ``base_optimizer`` module houses the parent classes ``BaseOptimizer`` from which all
optimisers will inherit. ``BaseConvexOptimizer`` is the base class for all ``cvxpy`` (and ``scipy``)
optimisation.

Additionally, we define a general utility function ``portfolio_performance`` to
evaluate return and risk for a given set of portfolio weights.
"""

import json
import warnings
import numpy as np
import pandas as pd
import cvxpy as cp
import scipy.optimize as sco
from . import objective_functions
from . import exceptions


class BaseOptimizer:

    """
    Instance variables:

    - ``n_assets`` - int
    - ``tickers`` - str list
    - ``weights`` - np.ndarray

    Public methods:

    - ``set_weights()`` creates self.weights (np.ndarray) from a weights dict
    - ``clean_weights()`` rounds the weights and clips near-zeros.
    - ``save_weights_to_file()`` saves the weights to csv, json, or txt.
    """

    def __init__(self, n_assets, tickers=None):
        """
        :param n_assets: number of assets
        :type n_assets: int
        :param tickers: name of assets
        :type tickers: list
        """
        self.n_assets = n_assets
        if tickers is None:
            self.tickers = list(range(n_assets))
        else:
            self.tickers = tickers
        # Outputs
        self.weights = None

    def set_weights(self, weights):
        """
        Utility function to set weights.

        :param weights: {ticker: weight} dictionary
        :type weights: dict
        """
        self.weights = np.array([weights[ticker] for ticker in self.tickers])

    def clean_weights(self, cutoff=1e-4, rounding=5):
        """
        Helper method to clean the raw weights, setting any weights whose absolute
        values are below the cutoff to zero, and rounding the rest.

        :param cutoff: the lower bound, defaults to 1e-4
        :type cutoff: float, optional
        :param rounding: number of decimal places to round the weights, defaults to 5.
                         Set to None if rounding is not desired.
        :type rounding: int, optional
        :return: asset weights
        :rtype: dict
        """
        if self.weights is None:
            raise AttributeError("Weights not yet computed")
        clean_weights = self.weights.copy()
        clean_weights[np.abs(clean_weights) < cutoff] = 0
        if rounding is not None:
            if not isinstance(rounding, int) or rounding < 1:
                raise ValueError("rounding must be a positive integer")
            clean_weights = np.round(clean_weights, rounding)
        return dict(zip(self.tickers, clean_weights))

    def save_weights_to_file(self, filename="weights.csv"):
        """
        Utility method to save weights to a text file.

        :param filename: name of file. Should be csv, json, or txt.
        :type filename: str
        """
        clean_weights = self.clean_weights()

        ext = filename.split(".")[1]
        if ext == "csv":
            pd.Series(clean_weights).to_csv(filename, header=False)
        elif ext == "json":
            with open(filename, "w") as fp:
                json.dump(clean_weights, fp)
        else:
            with open(filename, "w") as f:
                f.write(str(clean_weights))


class BaseConvexOptimizer(BaseOptimizer):

    """
    The BaseConvexOptimizer contains many private variables for use by
    ``cvxpy``. For example, the immutable optimisation variable for weights
    is stored as self._w. Interacting directly with these variables is highly
    discouraged.

    Instance variables:

    - ``n_assets`` - int
    - ``tickers`` - str list
    - ``weights`` - np.ndarray

    Public methods:

    - ``add_objective()`` adds a (convex) objective to the optimisation problem
    - ``add_constraint()`` adds a (linear) constraint to the optimisation problem
    - ``convex_objective()`` solves for a generic convex objective with linear constraints
    - ``nonconvex_objective()`` solves for a generic nonconvex objective using the scipy backend.
      This is prone to getting stuck in local minima and is generally *not* recommended.
    - ``set_weights()`` creates self.weights (np.ndarray) from a weights dict
    - ``clean_weights()`` rounds the weights and clips near-zeros.
    - ``save_weights_to_file()`` saves the weights to csv, json, or txt.
    """

    def __init__(self, n_assets, tickers=None, weight_bounds=(0, 1)):
        """
        :param weight_bounds: minimum and maximum weight of each asset OR single min/max pair
                              if all identical, defaults to (0, 1). Must be changed to (-1, 1)
                              for portfolios with shorting.
        :type weight_bounds: tuple OR tuple list, optional
        """
        super().__init__(n_assets, tickers)

        # Optimisation variables
        self._w = cp.Variable(n_assets)
        self._objective = None
        self._additional_objectives = []
        self._constraints = []
        self._lower_bounds = None
        self._upper_bounds = None
        self._map_bounds_to_constraints(weight_bounds)

    def _map_bounds_to_constraints(self, test_bounds):
        """
        Process input bounds into a form acceptable by cvxpy and add to the constraints list.

        :param test_bounds: minimum and maximum weight of each asset OR single min/max pair
                            if all identical OR pair of arrays corresponding to lower/upper bounds. defaults to (0, 1).
        :type test_bounds: tuple OR list/tuple of tuples OR pair of np arrays
        :raises TypeError: if ``test_bounds`` is not of the right type
        :return: bounds suitable for cvxpy
        :rtype: tuple pair of np.ndarray
        """
        # If it is a collection with the right length, assume they are all bounds.
        if len(test_bounds) == self.n_assets and not isinstance(
            test_bounds[0], (float, int)
        ):
            bounds = np.array(test_bounds, dtype=np.float)
            self._lower_bounds = np.nan_to_num(bounds[:, 0], nan=-np.inf)
            self._upper_bounds = np.nan_to_num(bounds[:, 1], nan=np.inf)
        else:
            # Otherwise this must be a pair.
            if len(test_bounds) != 2 or not isinstance(test_bounds, (tuple, list)):
                raise TypeError(
                    "test_bounds must be a pair (lower bound, upper bound) "
                    "OR a collection of bounds for each asset"
                )
            lower, upper = test_bounds

            # Replace None values with the appropriate +/- 1
            if np.isscalar(lower) or lower is None:
                lower = -1 if lower is None else lower
                self._lower_bounds = np.array([lower] * self.n_assets)
                upper = 1 if upper is None else upper
                self._upper_bounds = np.array([upper] * self.n_assets)
            else:
                self._lower_bounds = np.nan_to_num(lower, nan=-1)
                self._upper_bounds = np.nan_to_num(upper, nan=1)

        self._constraints.append(self._w >= self._lower_bounds)
        self._constraints.append(self._w <= self._upper_bounds)

    def _solve_cvxpy_opt_problem(self):
        """
        Helper method to solve the cvxpy problem and check output,
        once objectives and constraints have been defined

        :raises exceptions.OptimizationError: if problem is not solvable by cvxpy
        """
        try:
            opt = cp.Problem(cp.Minimize(self._objective), self._constraints)
            opt.solve()
        except (TypeError, cp.DCPError):
            raise exceptions.OptimizationError
        if opt.status != "optimal":
            raise exceptions.OptimizationError
        self.weights = self._w.value.round(16) + 0.0  # +0.0 removes signed zero

    def add_objective(self, new_objective, **kwargs):
        """
        Add a new term into the objective function. This term must be convex,
        and built from cvxpy atomic functions.

        Example::

            def L1_norm(w, k=1):
                return k * cp.norm(w, 1)

            ef.add_objective(L1_norm, k=2)

        :param new_objective: the objective to be added
        :type new_objective: cp.Expression (i.e function of cp.Variable)
        """
        self._additional_objectives.append(new_objective(self._w, **kwargs))

    def add_constraint(self, new_constraint):
        """
        Add a new constraint to the optimisation problem. This constraint must be linear and
        must be either an equality or simple inequality.

        Examples::

            ef.add_constraint(lambda x : x[0] == 0.02)
            ef.add_constraint(lambda x : x >= 0.01)
            ef.add_constraint(lambda x: x <= np.array([0.01, 0.08, ..., 0.5]))

        :param new_constraint: the constraint to be added
        :type constraintfunc: lambda function
        """
        if not callable(new_constraint):
            raise TypeError("New constraint must be provided as a lambda function")
        self._constraints.append(new_constraint(self._w))

    def add_sector_constraints(self, sector_mapper, sector_lower, sector_upper):
        """
        Adds constraints on the sum of weights of different groups of assets.
        Most commonly, these will be sector constraints e.g portfolio's exposure to
        tech must be less than x%::

            sector_mapper = {
                "GOOG": "tech",
                "FB": "tech",,
                "XOM": "Oil/Gas",
                "RRC": "Oil/Gas",
                "MA": "Financials",
                "JPM": "Financials",
            }

            sector_lower = {"tech": 0.1}  # at least 10% to tech
            sector_upper = {
                "tech": 0.4, # less than 40% tech
                "Oil/Gas: 0.1 # less than 10% oil and gas
            }

        :param sector_mapper: dict that maps tickers to sectors
        :type sector_mapper: {str: str} dict
        :param sector_lower: lower bounds for each sector
        :type sector_lower: {str: float} dict
        :param sector_upper: upper bounds for each sector
        :type sector_upper: {str:float} dict
        """
        if np.any(self._lower_bounds < 0):
            warnings.warn(
                "Sector constraints may not produce reasonable results if shorts are allowed."
            )
        for sector in sector_upper:
            is_sector = [sector_mapper[t] == sector for t in self.tickers]
            self._constraints.append(cp.sum(self._w[is_sector]) <= sector_upper[sector])
        for sector in sector_lower:
            is_sector = [sector_mapper[t] == sector for t in self.tickers]
            self._constraints.append(cp.sum(self._w[is_sector]) >= sector_lower[sector])

    def convex_objective(self, custom_objective, weights_sum_to_one=True, **kwargs):
        """
        Optimise a custom convex objective function. Constraints should be added with
        ``ef.add_constraint()``. Optimiser arguments must be passed as keyword-args. Example::

            # Could define as a lambda function instead
            def logarithmic_barrier(w, cov_matrix, k=0.1):
                # 60 Years of Portfolio Optimisation, Kolm et al (2014)
                return cp.quad_form(w, cov_matrix) - k * cp.sum(cp.log(w))

            w = ef.convex_objective(logarithmic_barrier, cov_matrix=ef.cov_matrix)

        :param custom_objective: an objective function to be MINIMISED. This should be written using
                                 cvxpy atoms Should map (w, `**kwargs`) -> float.
        :type custom_objective: function with signature (cp.Variable, `**kwargs`) -> cp.Expression
        :param weights_sum_to_one: whether to add the default objective, defaults to True
        :type weights_sum_to_one: bool, optional
        :raises OptimizationError: if the objective is nonconvex or constraints nonlinear.
        :return: asset weights for the efficient risk portfolio
        :rtype: dict
        """
        # custom_objective must have the right signature (w, **kwargs)
        self._objective = custom_objective(self._w, **kwargs)

        for obj in self._additional_objectives:
            self._objective += obj

        if weights_sum_to_one:
            self._constraints.append(cp.sum(self._w) == 1)

        self._solve_cvxpy_opt_problem()
        return dict(zip(self.tickers, self.weights))

    def nonconvex_objective(
        self,
        custom_objective,
        objective_args=None,
        weights_sum_to_one=True,
        constraints=None,
        solver="SLSQP",
    ):
        """
        Optimise some objective function using the scipy backend. This can
        support nonconvex objectives and nonlinear constraints, but often gets stuck
        at local minima. This method is not recommended – caveat emptor. Example::

            # Market-neutral efficient risk
            constraints = [
                {"type": "eq", "fun": lambda w: np.sum(w)},  # weights sum to zero
                {
                    "type": "eq",
                    "fun": lambda w: target_risk ** 2 - np.dot(w.T, np.dot(ef.cov_matrix, w)),
                },  # risk = target_risk
            ]
            ef.nonconvex_objective(
                lambda w, mu: -w.T.dot(mu),  # min negative return (i.e maximise return)
                objective_args=(ef.expected_returns,),
                weights_sum_to_one=False,
                constraints=constraints,
            )

        :param objective_function: an objective function to be MINIMISED. This function
                                   should map (weight, args) -> cost
        :type objective_function: function with signature (np.ndarray, args) -> float
        :param objective_args: arguments for the objective function (excluding weight)
        :type objective_args: tuple of np.ndarrays
        :param weights_sum_to_one: whether to add the default objective, defaults to True
        :type weights_sum_to_one: bool, optional
        :param constraints: list of constraints in the scipy format (i.e dicts)
        :type constraints: dict list
        :param solver: which SCIPY solver to use, e.g "SLSQP", "COBYLA", "BFGS".
                       User beware: different optimisers require different inputs.
        :type solver: string
        :return: asset weights that optimise the custom objective
        :rtype: dict
        """
        # Sanitise inputs
        if not isinstance(objective_args, tuple):
            objective_args = (objective_args,)

        # Make scipy bounds
        bound_array = np.vstack((self._lower_bounds, self._upper_bounds)).T
        bounds = list(map(tuple, bound_array))

        initial_guess = np.array([1 / self.n_assets] * self.n_assets)

        # Construct constraints
        final_constraints = []
        if weights_sum_to_one:
            final_constraints.append({"type": "eq", "fun": lambda x: np.sum(x) - 1})
        if constraints is not None:
            final_constraints += constraints

        result = sco.minimize(
            custom_objective,
            x0=initial_guess,
            args=objective_args,
            method=solver,
            bounds=bounds,
            constraints=final_constraints,
        )
        self.weights = result["x"]
        return dict(zip(self.tickers, self.weights))


def portfolio_performance(
    weights, expected_returns, cov_matrix, verbose=False, risk_free_rate=0.02
):
    """
    After optimising, calculate (and optionally print) the performance of the optimal
    portfolio. Currently calculates expected return, volatility, and the Sharpe ratio.

    :param expected_returns: expected returns for each asset. Can be None if
                             optimising for volatility only (but not recommended).
    :type expected_returns: np.ndarray or pd.Series
    :param cov_matrix: covariance of returns for each asset
    :type cov_matrix: np.array or pd.DataFrame
    :param weights: weights or assets
    :type weights: list, np.array or dict, optional
    :param verbose: whether performance should be printed, defaults to False
    :type verbose: bool, optional
    :param risk_free_rate: risk-free rate of borrowing/lending, defaults to 0.02
    :type risk_free_rate: float, optional
    :raises ValueError: if weights have not been calcualted yet
    :return: expected return, volatility, Sharpe ratio.
    :rtype: (float, float, float)
    """
    if isinstance(weights, dict):
        if isinstance(expected_returns, pd.Series):
            tickers = list(expected_returns.index)
        elif isinstance(cov_matrix, pd.DataFrame):
            tickers = list(cov_matrix.columns)
        else:
            tickers = list(range(len(expected_returns)))
        new_weights = np.zeros(len(tickers))

        for i, k in enumerate(tickers):
            if k in weights:
                new_weights[i] = weights[k]
        if new_weights.sum() == 0:
            raise ValueError("Weights add to zero, or ticker names don't match")
    elif weights is not None:
        new_weights = np.asarray(weights)
    else:
        raise ValueError("Weights is None")

    sigma = np.sqrt(objective_functions.portfolio_variance(new_weights, cov_matrix))

    if expected_returns is not None:
        mu = objective_functions.portfolio_return(
            new_weights, expected_returns, negative=False
        )

        sharpe = objective_functions.sharpe_ratio(
            new_weights,
            expected_returns,
            cov_matrix,
            risk_free_rate=risk_free_rate,
            negative=False,
        )
        if verbose:
            print("Expected annual return: {:.1f}%".format(100 * mu))
            print("Annual volatility: {:.1f}%".format(100 * sigma))
            print("Sharpe Ratio: {:.2f}".format(sharpe))
        return mu, sigma, sharpe
    else:
        if verbose:
            print("Annual volatility: {:.1f}%".format(100 * sigma))
        return None, sigma, None
