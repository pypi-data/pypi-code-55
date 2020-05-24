#!/usr/bin/env python3

import sys
sys.path.append(".")

import sympy
from sympy.abc import x, y

class DESolveMethod:
    def __init__(self):
        pass

    def solve(self, *args):
        raise NotImplementedError('Method not determined.')

    def __str__(self):
        return 'Differential equation solve method.'

def support_lambda(solve_function):
    def wrapper(*args):
        func = args[1]
        if isinstance(func, tuple(sympy.core.all_classes)):
            func = sympy.utilities.lambdify([x, y], func)
        args = list(args)
        args[1] = func
        return solve_function(*args)
    return wrapper
