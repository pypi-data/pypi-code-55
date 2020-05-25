# -*- coding: utf-8 -*-
# ######### COPYRIGHT #########
# Credits
# #######
#
# Copyright(c) 2019-2020
# ----------------------
#
# * Laboratoire d'Informatique et Systèmes <http://www.lis-lab.fr/>
# * Université d'Aix-Marseille <http://www.univ-amu.fr/>
# * Centre National de la Recherche Scientifique <http://www.cnrs.fr/>
# * Université de Toulon <http://www.univ-tln.fr/>
#
# Contributors
# ------------
#
# * Valentin Emiya <firstname.lastname_AT_lis-lab.fr>
#
# This package has been created thanks to the joint work with Florent Jaillet
# and Ronan Hamon on other packages.
#
# Description
# -----------
#
# `skpomade` is a Python implementation of algorithms from
# paper *Finding Structure with Randomness: Probabilistic Algorithms for
# Constructing Approximate Matrix Decompositions*, by N. Halko, P. G.
# Martinsson and J. A. Tropp, SIAM review, 53 (2), 2011, https://arxiv.org/abs/0909.4061.
#
#
# Version
# -------
#
# * skpomade version = 0.1.4
#
# Licence
# -------
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ######### COPYRIGHT #########
""" Algorithms for Stage A: Randomized Schemes for Approximating the Range

.. moduleauthor:: Valentin Emiya
"""
import numpy as np


def randomized_range_finder(a, n_l, rand_state=None):
    """ Algorithm 4.1 : Randomized Range Finder

    Parameters
    ----------
    a : nd-array or LinearOperator [m, n]
        Matrix or linear operator whose range must be computed
    n_l : int
        Number of columns in result
    rand_state : RandomState, int or None
        If RandomState, random generator.
        If int or None, random seed used to initialize the pseudo-random
        number generator.

    Returns
    -------
    nd-array [m, n_l]
        Matrix whose columns are orthonormal and whose range approximates
        the range of a.
    """
    if rand_state is None:
        rand_state = np.random.RandomState(None)
    if np.issubdtype(type(rand_state), np.dtype(int).type):
        rand_state = np.random.RandomState(rand_state)
    n = a.shape[1]
    omega = rand_state.randn(n, n_l)
    y_mat = a @ omega
    q_mat, _ = np.linalg.qr(y_mat)
    return q_mat


def adaptive_randomized_range_finder(a, tolerance, r=5, proba=None,
                                     rand_state=None, n_cols_Q=16):
    """ Algorithm 4.2 : Adaptive Randomized Range Finder

    Parameters
    ----------
    a : nd-array or LinearOperator [m, n]
        Matrix or linear operator whose range must be computed
    tolerance : float
        Required tolerance on the range approximation.
    r : int
        Number of Gaussian vectors used for a posteriori error estimation.
        Either `r` or `proba` should be set, not both.
    proba : float
        Probability that the error is lower than the tolerance. Either `r` or
        `proba` should be set, not both.
    rand_state : RandomState, int or None
        If RandomState, random generator.
        If int or None, random seed used to initialize the pseudo-random
        number generator.
    n_cols_Q : int
        Initial number of columns to be allocated in Q.

    Returns
    -------

    For computational efficiency, this implementation uses circular arrays
    for `Y` and `y_norms`, memory allocation for `Q` and no internal loop
    """
    if proba is None and r is None:
        raise ValueError('Either proba or n_r should not be None.')
    if proba is not None and r is not None:
        raise ValueError('Either proba or n_r should be None.')
    if proba is not None:
        r = int(np.ceil(- np.log10((1 - proba) / np.min(a.shape))))
    if rand_state is None:
        rand_state = np.random.RandomState(None)
    if np.issubdtype(type(rand_state), np.dtype(int).type):
        rand_state = np.random.RandomState(rand_state)
    m, n = a.shape
    W = rand_state.randn(n, r)
    Y = a @ W
    y_norms = np.linalg.norm(Y, axis=0)
    j = 0
    Q_width = 0
    # order='F' necessary for Q.resize
    Q = np.empty((m, n_cols_Q), order='F', dtype=a.dtype)

    while np.max(y_norms) > tolerance / (10 * np.sqrt(2 / np.pi)):
        if Q_width >= n:
            # TODO to be tested
            raise RuntimeError('Required tolerance not reached with maximum '
                               'number of columns ({}). Singular '
                               'values may decrease too slowly.'.format(n))
        Y[:, j] -= Q[:, :Q_width] @ (Q[:, :Q_width].T.conj() @ Y[:, j])
        q = Y[:, j] / np.linalg.norm(Y[:, j])
        j = (j + 1) % r
        Q_width += 1
        if Q_width > Q.shape[1]:
            Q.resize(m, Q.shape[1]*2)
        Q[:, Q_width-1] = q
        # This matrix operation is done on the full matrix and column j-1 is
        # then overwritten with y to comply with the original algorithm,
        # even if the orthogonalization of Y would not affect y significantly.
        Y -= np.outer(q, q.conj() @ Y)
        w = rand_state.randn(n)
        A_w = a @ w
        y = A_w - Q[:, :Q_width] @ (Q[:, :Q_width].T.conj() @ A_w)
        Y[:, j - 1] = y
        y_norms[j - 1] = np.linalg.norm(y)
    return Q[:, :Q_width]

