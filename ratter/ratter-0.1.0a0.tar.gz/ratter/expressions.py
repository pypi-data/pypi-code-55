"""
This module provides functions to be applied to
sympy expressions to bridge the gap between
symbolic expressions and algorithms and functions
to be applied on numbers or arrays
"""

import sympy as sp


def as_function_of(expression, symbols):
    """Return the symbolic expression as a function
    that can applied onto numbers and numpy arrays.
    This is just a wrapper to sympy's lambdify
    with sanity checks.

    Parameters
    ----------
    expression : sympy expression
        Expression with free symbols to turn into a
        function. The number of free symbols must match
        the list of symbols, such that the expression
        can fully be evaluated
    symbols : list of sympy.symbols
        symbols which will turn into the input arguments
        of the returned callable

    Returns
    -------
    callable : Method to be applied on N numbers or
        N numpy arrays, where N is the number of free
        symbols
    """
    for s in symbols:
        assert s in expression.free_symbols
    assert len(symbols) == len(expression.free_symbols)

    return sp.lambdify(symbols, expression, 'numpy')
