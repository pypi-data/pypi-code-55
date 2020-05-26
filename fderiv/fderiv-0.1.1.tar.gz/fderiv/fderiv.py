#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 19:57:12 2020

Five point derivative for a given input array

Version : 0.1
@author: Sudhanva Lalit
"""

'''
Five point derivatives for an array using formulae and tables from Abramovitz-Stegun.
Inputs : N   --  length of array (N > 5)
        x(N) --  Array of equally spaced x values
        f(N) --  Array of f(x) values
Outputs: fd(N) -- Array of df(x)/dx values
        fdd(N) -- Array of d^2f(x)/dx^2 values
'''

import numpy as np


class fderiv(object):
    '''
    fderiv(x,y)

    Derivative of a 1-D array

    `x`, `y` are values used to evaluate the derivative of y with respect to x.
    this class returns the first and the second derivative of the function.

    Methods:
    --------
    __call__



    '''

    def __init__(self, x, y, yd, ydd):
        x = np.ravel(x)
        y = np.ravel(y)
        yd = np.asarray(yd)
        ydd = np.asarray(ydd)
        #
        self.x, self.y = x, y

    def __call__(self, x, y):
        """ 5 point derivative of the function

        Parameters:
        -----------
        x : 1-D array
            x-values of the mesh on which to calculate the derivative
        y : 1-D array
            y-values of the mesh of which derivative is calculated

        Returns:
        --------
        yd : 1-D array
            first derivative of the function y
        ydd : 1-D array
            second derivative of the function y

        """
        x = np.atleast_1d(x)
        y = np.atleast_1d(y)
        N = len(x)
        yd = np.zeros(N)
        ydd = np.zeros(N)

        yd, ydd = fd5pt(x, y)

        return yd, ydd

    @staticmethod
    def func(x, f):

        fd = np.empty(5)
        fdd = np.empty(5)
        a00, a01, a02, a03, a04 = -50., 96., -72., 32., -6.
        a10, a11, a12, a13, a14 = -6., -20., 36., -12., 2.
        a20, a21, a22, a23, a24 = 2., -16., 0., 16., -2.
        a30, a31, a32, a33, a34 = -2., 12., -36., 20., 6.
        a40, a41, a42, a43, a44 = 6., -32., 72., -96., 50.
        #
        b00, b01, b02, b03, b04 = 70., -208., 228., -112., 22.
        b10, b11, b12, b13, b14 = 22., -40., 12., 8., -2.
        b20, b21, b22, b23, b24 = -2., 32., -60., 32., -2.
        b30, b31, b32, b33, b34 = -2., 8., 12., -40., 22.
        b40, b41, b42, b43, b44 = 22., -112., 228., -208., 70.

        h = x[1] - x[0]

        fd[0] = (a00 * f[0] + a01 * f[1] + a02 * f[2] + a03 * f[3] + a04 * f[4]) / (24. * h)
        fd[1] = (a10 * f[0] + a11 * f[1] + a12 * f[2] + a13 * f[3] + a14 * f[4]) / (24. * h)
        fd[2] = (a20 * f[0] + a21 * f[1] + a22 * f[2] + a23 * f[3] + a24 * f[4]) / (24. * h)
        fd[3] = (a30 * f[0] + a31 * f[1] + a32 * f[2] + a33 * f[3] + a34 * f[4]) / (24. * h)
        fd[4] = (a40 * f[0] + a41 * f[1] + a42 * f[2] + a43 * f[3] + a44 * f[4]) / (24. * h)
    #
        fdd[0] = (b00 * f[0] + b01 * f[1] + b02 * f[2] + b03 * f[3] + b04 * f[4]) / (24. * h**2)
        fdd[1] = (b10 * f[0] + b11 * f[1] + b12 * f[2] + b13 * f[3] + b14 * f[4]) / (24. * h**2)
        fdd[2] = (b20 * f[0] + b21 * f[1] + b22 * f[2] + b23 * f[3] + b24 * f[4]) / (24. * h**2)
        fdd[3] = (b30 * f[0] + b31 * f[1] + b32 * f[2] + b33 * f[3] + b34 * f[4]) / (24. * h**2)
        fdd[4] = (b40 * f[0] + b41 * f[1] + b42 * f[2] + b43 * f[3] + b44 * f[4]) / (24. * h**2)

        return fd, fdd

    @staticmethod
    def fd5pt(x, f):
        N = len(x)
        dy = np.empty(N)
        dyy = np.empty(N)
        y = np.zeros(5)
        fy = np.zeros(5)
        res1 = np.zeros(5)
        res2 = np.zeros(5)
        for i in range(N):
            if i == 0:
                m = 0
                p = 0
            elif i == 1:
                m = 1
                p = 0
            elif i == (N - 2):
                m = N - 5
                p = 3
            elif i == N - 1:
                m = N - 5
                p = 4
            else:
                m = i - 2
                p = 2
            for j in range(5):
                y[j] = x[j + m]
                fy[j] = f[j + m]
            res1, res2 = fderiv.func(y, fy)
            dy[i], dyy[i] = res1[p], res2[p]
        return dy, dyy
