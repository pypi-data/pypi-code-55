#!/usr/bin/env python3

'''
Author: Igor Amashukeli
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


    def solve(self, f,
              initial_dot: Tuple[float, float],
              offset: float,
              count: Int, epsilon : AlgStep) -> None:

        if not isinstance(f, tuple(sy.core.all_classes)):
            raise Exception("Taylor Method supports only sympy objects as given functions")

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
        table.append(
            {
                'i': 0,
                'x': x_0,
                'y': y_0,
            }
        )
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
