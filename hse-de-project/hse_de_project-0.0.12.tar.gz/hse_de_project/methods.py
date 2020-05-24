#!/usr/bin/env python3

'''
All methods here
'''

import sys
sys.path.append(".")


import matplotlib.pyplot as plt
import numpy as np
import sympy as sy
from fractions import Fraction as frac
sy.init_printing()


from typing import Callable, Tuple, List, NewType
import pandas as pd
import matplotlib.pyplot as plt
import math
from . import DEMethod


AlgStep = NewType('step', float)
Frame = NewType('frame', pd.DataFrame)
Int = NewType('int', int)
Float = NewType('step', float)


class AdamsMethodII(DEMethod.DESolveMethod):
    def __init__(self):
        pass

    @staticmethod
    def n_iterations(segment: List[float], step: Float) -> int:
        return int((segment[1] - segment[0]) / step)

    @staticmethod
    def add_new_entry(i, table,
                      f: Callable[[float, float], float],
                      x: Float,
                      y: Float):

        table.append(
            {
                'i': i,
                'x': x,
                'y': y,
                'func': f(x, y)
            }
        )

    @staticmethod
    def runge_kutta(f: Callable[[float, float], float],
                    x: Float,
                    y: Float,
                    step: Float) -> Float:
        k_1 = f(x, y)
        k_2 = f(x + step/2, y + step/2 * k_1)
        k_3 = f(x + step/2, y + step/2 * k_2)
        k_4 = f(x + step, y + step * k_3)
        return y + step/6 * (k_1 + 2 * k_2 + 2 * k_3 + k_4)

    # Using Runge-Kutta method for initial points
    def precount(self, table, f: Callable[[float, float], float],
                 initial_dot: Tuple[float, float],
                 step: Float):

        x_0, y_0 = initial_dot[0], initial_dot[1]
        self.add_new_entry(0, table, f, x_0, y_0)

        x_1 = x_0 + step
        y_1 = self.runge_kutta(f, x_0, y_0, step)
        self.add_new_entry(1, table, f, x_1, y_1)

    @DEMethod.support_lambda
    def solve(self, f: Callable[[float, float], float],
              initial_dot: Tuple[float, float],
              segment: List[float],
              step: Float) -> pd.DataFrame:

        if len(segment) != 2:
            raise Exception('Segment must be a list of size = 2.')

        table = []
        self.precount(table, f, initial_dot, step)

        for i in range(2, self.n_iterations(segment, step) + 1):
            x_new = table[i - 1]['x'] + step
            y_new = table[i - 1]['y'] + step * (3/2 * table[i - 1]['func'] - 1/2 * table[i - 2]['func'])
            self.add_new_entry(i, table, f, x_new, y_new)

        df = pd.DataFrame(table)
        return df

    def __str__(self):
        return 'Adams-Bashforth method of solving differential equations.'


class AdamsMethodIII(DEMethod.DESolveMethod):
    def __init__(self):
        pass

    @staticmethod
    def n_iterations(segment: List[float], step: Float) -> int:
        return int((segment[1] - segment[0]) / step)

    @staticmethod
    def add_new_entry(i, table,
                      f: Callable[[float, float], float],
                      x: Float,
                      y: Float):

        table.append(
            {
                'i': i,
                'x': x,
                'y': y,
                'func': f(x, y)
            }
        )

    @staticmethod
    def runge_kutta(f: Callable[[float, float], float],
                    x: Float,
                    y: Float,
                    step: Float) -> Float:
        k_1 = f(x, y)
        k_2 = f(x + step/2, y + step/2 * k_1)
        k_3 = f(x + step/2, y + step/2 * k_2)
        k_4 = f(x + step, y + step * k_3)
        return y + step/6 * (k_1 + 2 * k_2 + 2 * k_3 + k_4)

    # Using Runge-Kutta method for initial points
    def precount(self, table, f: Callable[[float, float], float],
                 initial_dot: Tuple[float, float],
                 step: Float):

        x_0, y_0 = initial_dot[0], initial_dot[1]
        self.add_new_entry(0, table, f, x_0, y_0)

        x_1 = x_0 + step
        y_1 = self.runge_kutta(f, x_0, y_0, step)
        self.add_new_entry(1, table, f, x_1, y_1)

        x_2 = x_1 + step
        y_2 = self.runge_kutta(f, x_1, y_1, step)
        self.add_new_entry(2, table, f, x_2, y_2)

    @DEMethod.support_lambda
    def solve(self, f: Callable[[float, float], float],
              initial_dot: Tuple[float, float],
              segment: List[float],
              step: Float) -> pd.DataFrame:

        if len(segment) != 2:
            raise Exception('Segment must be a list of size = 2.')

        table = []
        self.precount(table, f, initial_dot, step)

        for i in range(3, self.n_iterations(segment, step) + 1):
            x_new = table[i - 1]['x'] + step
            y_new = table[i - 1]['y'] + step * (23/12 * table[i - 1]['func'] - 16/12 * table[i - 2]['func'] + 5/12 * table[i - 3]['func'])
            self.add_new_entry(i, table, f, x_new, y_new)

        df = pd.DataFrame(table)
        return df

    def __str__(self):
        return 'Adams-Bashforth method of solving differential equations.'


class AdamsMethodIV(DEMethod.DESolveMethod):
    def __init__(self):
        pass

    @staticmethod
    def n_iterations(segment: List[float], step: Float) -> int:
        return int((segment[1] - segment[0]) / step)

    @staticmethod
    def add_new_entry(i, table,
                      f: Callable[[float, float], float],
                      x: Float,
                      y: Float):

        table.append(
            {
                'i': i,
                'x': x,
                'y': y,
                'func': f(x, y)
            }
        )

    @staticmethod
    def runge_kutta(f: Callable[[float, float], float],
                    x: Float,
                    y: Float,
                    step: Float) -> Float:
        k_1 = f(x, y)
        k_2 = f(x + step/2, y + step/2 * k_1)
        k_3 = f(x + step/2, y + step/2 * k_2)
        k_4 = f(x + step, y + step * k_3)
        return y + step/6 * (k_1 + 2 * k_2 + 2 * k_3 + k_4)

    # Using Runge-Kutta method for initial points
    def precount(self, table, f: Callable[[float, float], float],
                 initial_dot: Tuple[float, float],
                 step: Float):

        x_0, y_0 = initial_dot[0], initial_dot[1]
        self.add_new_entry(0, table, f, x_0, y_0)

        x_1 = x_0 + step
        y_1 = self.runge_kutta(f, x_0, y_0, step)
        self.add_new_entry(1, table, f, x_1, y_1)

        x_2 = x_1 + step
        y_2 = self.runge_kutta(f, x_1, y_1, step)
        self.add_new_entry(2, table, f, x_2, y_2)

        x_3 = x_2 + step
        y_3 = self.runge_kutta(f, x_2, y_2, step)
        self.add_new_entry(3, table, f, x_3, y_3)

    @DEMethod.support_lambda
    def solve(self, f: Callable[[float, float], float],
              initial_dot: Tuple[float, float],
              segment: List[float],
              step: Float) -> pd.DataFrame:

        if len(segment) != 2:
            raise Exception('Segment must be a list of size = 2.')

        table = []
        self.precount(table, f, initial_dot, step)

        for i in range(4, self.n_iterations(segment, step) + 1):
            x_new = table[i - 1]['x'] + step
            y_new = table[i - 1]['y'] + step * (55/24 * table[i - 1]['func'] - 59/24 * table[i - 2]['func'] + 37/24 * table[i - 3]['func'] - 9/24 * table[i - 4]['func'])
            self.add_new_entry(i, table, f, x_new, y_new)

        df = pd.DataFrame(table)
        return df

    def __str__(self):
        return 'Adams-Bashforth method of solving differential equations.'


class EulerMethod(DEMethod.DESolveMethod):
    def __init__(self):
        pass

    @staticmethod
    def n_iterations(segment: List[float], step: AlgStep) -> int:
        return int((segment[1] - segment[0]) / step)

    @DEMethod.support_lambda
    def solve(self, f: Callable[[float, float], float],
              initial_dot: Tuple[float, float],
              segment: List[float],
              step: AlgStep) -> pd.DataFrame:

        if len(segment) != 2:
            raise Exception('Segment must be a list of size = 2.')

        table = []
        x_0, y_0 = initial_dot[0], initial_dot[1]
        table.append(
            {
                'i': 0,
                'x': x_0,
                'y': y_0,
                'func': f(x_0, y_0)
            }
        )

        for i in range(1, self.n_iterations(segment, step) + 1):
            x_last, y_last, value_last = table[i - 1]['x'], table[i - 1]['y'], table[i - 1]['func']
            x_new = x_last + step
            y_new = y_last + step * value_last
            table.append(
                {
                    'i': i,
                    'x': x_new,
                    'y': y_new,
                    'func': f(x_new, y_new)
                }
            )

        df = pd.DataFrame(table)
        return df

    def __str__(self):
        return 'Euler method of solving differential equations.'


class IRK2Method(DEMethod.DESolveMethod):
    def __init__(self):
        pass

    @staticmethod
    def n_iterations(segment: List[float], step: Float) -> int:
        return int((segment[1] - segment[0]) / step)

    @staticmethod
    def update_y(f: Callable[[float, float], float],
                x: Float,
                y: Float,
                step: Float) -> int:

        temporary = y + step * f(x, y)
        y_new = y + step * (f(x, y) + f(x + step, temporary)) / 2

        return y_new

    @DEMethod.support_lambda
    def solve(self, f: Callable[[float, float], float],
              initial_dot: Tuple[float, float],
              segment: List[float],
              step: Float) -> pd.DataFrame:

        if len(segment) != 2:
            raise Exception('Segment must be a list of size = 2.')

        table = []
        x_0, y_0 = initial_dot[0], initial_dot[1]
        table.append(
            {
                'i': 0,
                'x': x_0,
                'y': y_0,
                'func': f(x_0, y_0)
            }
        )

        for i in range(1, self.n_iterations(segment, step) + 1):
            x_last, y_last = table[i - 1]['x'], table[i - 1]['y']
            x_new = x_last + step
            y_new = self.update_y(f, x_last, y_last, step)
            table.append(
                {
                    'i': i,
                    'x': x_new,
                    'y': y_new,
                    'func': f(x_new, y_new)
                }
            )

        df = pd.DataFrame(table)
        return df

    def __str__(self):
        return 'IRK2 method of solving differential equations.'


class ImprovedEulerMethod(DEMethod.DESolveMethod):
    def __init__(self):
        pass

    @staticmethod
    def n_iterations(segment: List[float], step: Float) -> int:
        return int((segment[1] - segment[0]) / step)

    @staticmethod
    def delta_y(f: Callable[[float, float], float],
                x: Float,
                y: Float,
                step: Float) -> int:
        return step * f(x + step / 2, y + step / 2 * f(x, y))

    @DEMethod.support_lambda
    def solve(self, f: Callable[[float, float], float],
              initial_dot: Tuple[float, float],
              segment: List[float],
              step: Float) -> pd.DataFrame:

        if len(segment) != 2:
            raise Exception('Segment must be a list of size = 2.')

        table = []
        x_0, y_0 = initial_dot[0], initial_dot[1]
        table.append(
            {
                'i': 0,
                'x': x_0,
                'y': y_0,
                'func': f(x_0, y_0)
            }
        )

        for i in range(1, self.n_iterations(segment, step) + 1):
            x_last, y_last = table[i - 1]['x'], table[i - 1]['y']
            x_new = x_last + step
            y_new = y_last + self.delta_y(f, x_last, y_last, step)
            table.append(
                {
                    'i': i,
                    'x': x_new,
                    'y': y_new,
                    'func': f(x_new, y_new)
                }
            )

        df = pd.DataFrame(table)
        return df

    def __str__(self):
        return 'Improved Euler method of solving differential equations.'


class RK4Method(DEMethod.DESolveMethod):
    def __init__(self):
        pass

    @staticmethod
    def n_iterations(segment: List[float], step: Float) -> int:
        return int((segment[1] - segment[0]) / step)

    @staticmethod
    def delta_y(f: Callable[[float, float], float],
                x: Float,
                y: Float,
                step: Float) -> int:

        k1 = f(x, y)
        k2 = f(x + step / 2, y + step * k1 / 2)
        k3 = f(x + step / 2, y + step * k2 / 2)
        k4 = f(x + step, y + step * k3)

        return (k1 + 2 * k2 + 2 * k3 + k4) * step / 6

    @DEMethod.support_lambda
    def solve(self, f: Callable[[float, float], float],
              initial_dot: Tuple[float, float],
              segment: List[float],
              step: Float) -> pd.DataFrame:

        if len(segment) != 2:
            raise Exception('Segment must be a list of size = 2.')

        table = []
        x_0, y_0 = initial_dot[0], initial_dot[1]
        table.append(
            {
                'i': 0,
                'x': x_0,
                'y': y_0,
                'func': f(x_0, y_0)
            }
        )

        for i in range(1, self.n_iterations(segment, step) + 1):
            x_last, y_last = table[i - 1]['x'], table[i - 1]['y']
            x_new = x_last + step
            y_new = y_last + self.delta_y(f, x_last, y_last, step)
            table.append(
                {
                    'i': i,
                    'x': x_new,
                    'y': y_new,
                    'func': f(x_new, y_new)
                }
            )

        df = pd.DataFrame(table)
        return df

    def __str__(self):
        return 'RK4 method of solving differential equations.'

class TaylorMethod(DEMethod.DESolveMethod):
    def __init__(self):
        pass

    @staticmethod
    def n_iterations(segment: List[float], step: AlgStep) -> int:
        return int((segment[1] - segment[0]) / step)


    def generate_list_of_trees_of_derivatives(self, number : Int) -> list:
        x = sy.Symbol('x')
        y = sy.Function('y')
        result = y(x)
        my_list = []
        for _ in range(number):
            result = self.find_derivative_dx(result)
            my_list.append(result)
        return my_list


    @staticmethod
    def make_subs(i_step : Int, count : Int, sub_list, der_list,
    in_dot : Tuple[float, float]) -> int:
        x = sy.Symbol('x')
        y = sy.Function('y')
        x_0 = in_dot[0]
        y_0 = in_dot[1]
        result = i_step
        for i in range(count):
            j = count - i - 1
            result = result.subs(der_list[j - 1], sub_list[j])
        result = result.subs(y(x), y_0).subs(x, x_0)
        return result


    @staticmethod
    def find_derivative_dx(function) -> sy.core.all_classes:
        x = sy.Symbol('x')
        return sy.diff(function, x)

    @staticmethod
    def find_derivative_dy(function) -> sy.core.all_classes:
        y = sy.Symbol('y')
        return sy.diff(function, y)


    def calculate_main_derivative(self, step : Int, f,
    in_dot : Tuple[float, float], der_list) -> list:
        x_0 = in_dot[0]
        y_0 = in_dot[1]
        x = sy.Symbol('x')
        y = sy.Function('y')
        i_result = y_0
        i_step = f
        der_subs_list = [i_result]
        for i in range(step):
            if i_step == f:
                i_result = f.subs(y(x), y_0).subs(x, x_0)
            else:
                i_result = self.make_subs(i_step, i + 1, der_subs_list, der_list, in_dot)
            i_step = self.find_derivative_dx(i_step) + self.find_derivative_dy(i_step)
            der_subs_list.append(i_result)
        return der_subs_list


    @staticmethod
    def start_proccess(count: Int, x : Int, sub_list,
    initial_dot : Tuple[float, float]):
        x_0 = initial_dot[0]
        y = 0
        divider = 1
        argument_of_fact = 0
        multiplier = 1
        for i in range(count):
            element = sub_list[i]
            element /= divider
            element *= multiplier
            y += element
            argument_of_fact += 1
            divider *= argument_of_fact
            multiplier *= (x - x_0)
        return y

    @staticmethod
    def convert(func):
        x = sy.Symbol('x')
        y_symb = sy.Symbol('y')
        y_func = sy.Function('y')(x)

        return func.subs(y_symb, y_func)

    def solve(self, f,
              initial_dot: Tuple[float, float],
              offset: float,
              count: Int, epsilon : AlgStep) -> None:

        if not isinstance(f, tuple(sy.core.all_classes)):
            raise Exception("Taylor Method supports only sympy objects as given functions")

        f = self.convert(f)

        x_0 = initial_dot[0]
        y_0 = initial_dot[1]
        der_list = self.generate_list_of_trees_of_derivatives(count)
        sub_list = self.calculate_main_derivative(count, f, initial_dot, der_list)
        if (epsilon <= 0):
            raise ValueError("Epsilon must be greater than 0")
        number = self.n_iterations([0, offset], epsilon) + 1
        my_array = [0 for i in range(number)]
        func_array = [0 for i in range(number)]
        for j in range(number):
            my_array[j] = x_0 + j * epsilon
            func_array[j] = self.start_proccess(count, my_array[j], sub_list, initial_dot)
        table = []
        for i in range(number):
            table.append(
                {
                    'i': i,
                    'x': my_array[i],
                    'y': func_array[i],
                }
            )
        df = pd.DataFrame(table)
        return df

    def __str__(self):
        return 'Taylor method of solving differential equations.'
