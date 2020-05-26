#!/usr/bin/env python
"""
This module contains functions for fitting models to the numerically
generated average levenshtein distances between random strings.
"""

import numpy as np

codegolf_ref = """https://codegolf.stackexchange.com/questions/197565/
can-you-calculate-the-average-levenshtein-distance-exactly/197576#197576"""


def poly(x, coeffs):
    """Evaluate a polynomial with the given `coeffs` at `x`.

    Args:
        x (array_like, float or int): x-positions at which
                                      to evaluate the polynomial
        coeffs (array_like): array of polynomial coefficients,
                             e.g. [c0, c1, c2] for the polynomial
                             c0 + c1 * x + c2 * x ** 2

    Returns:
        array_like: y-values for the polynomial at the given x positions
    """
    return np.sum([coeffs[i] * x ** i for i in range(len(coeffs))], axis=0)


def _fit_poly(y_data, deg=5):
    """Fit polynomial of degree `deg` to the given
    y_data.

    x-values are assumed to be the integers in the interval [1, len(y_data)].

    Args:
        y_data (array_like): data to fit the model to.
        deg (int, optional): degree of the polynomial to fit.

    Returns:
        array_like: array of the deg + 1 coefficients of the fitted polynomial
        array_like: mean squared error of the model
                    in the interval [1, len(y_data)].
    """
    x = np.arange(1, len(y_data) + 1)
    coeffs = np.polynomial.polynomial.polyfit(
        x, y_data, deg=deg)
    y_pred = poly(x, coeffs)
    return coeffs, np.mean((y_data - y_pred) ** 2)


def model_average_levenshtein(sampled_levenshtein, model_rows='all', deg=5):
    """Fit polynomial models to rows obtained from a
    sample.random_average_levenshtein() run.

    For a particular length n, the model is fitted only to the
    data for lengths <= n. DO NOT use a model generated for a length
    n to predict an expected distance between a string of length n
    a longer one!

    Args:
        sampled_levenshtein (array_like): distance matrix as returned by
                                          sample.random_average_levenshtein()
        model_rows (str, optional): the rows in the distance matrix to which
                                    models should be fitted. Only rows >= 25
                                    are accepted. If not specified, models
                                    will be generated for all rows
                                    with index >= 25.
        deg (int, optional): Degree of the polynomials that will be fitted.

    Returns:
        array_like: row indices for which models were computed
        array_like: coefficients of the fitted polynomials
        array_like: mean squared deviations between values predicted by the
                    models and the input data.
    """
    n = sampled_levenshtein.shape[0]
    assert n >= 25, """Modeling is not supported for n < 25.
        The exact expected distances are known for these lengths: {}""".format(
            codegolf_ref)
    if model_rows == 'all':
        model_rows = np.arange(25, n)
    else:
        model_rows = np.array(model_rows)
        model_rows = model_rows[model_rows >= 25]
        assert len(model_rows) > 0, """Modeling is not
            supported for n < 25. The exact expected distances
            are known for these lengths: {}""".format(
                codegolf_ref)

    n_rows = len(model_rows)
    coeffs = np.empty(shape=(n_rows, deg + 1))
    mses = np.empty(n_rows)
    for i, row in enumerate(model_rows):
        c, m = _fit_poly(sampled_levenshtein[row, :row+1])
        coeffs[i] = c
        mses[i] = m
    return model_rows, coeffs, mses
