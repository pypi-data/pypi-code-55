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
"""

.. moduleauthor:: Valentin Emiya
"""
import numpy as np
from scipy.sparse.linalg import aslinearoperator


def adaptive_randomized_range_finder_naive(a, tolerance, r=5, rand_state=None):
    """ Naive implementation for Algo 4.2 """
    if rand_state is None:
        rand_state = np.random.RandomState(None)
    if np.issubdtype(type(rand_state), np.dtype(int).type):
        rand_state = np.random.RandomState(rand_state)
    m, n = a.shape
    W = rand_state.randn(n, r)
    Y = [a @ W[:, i] for i in range(r)]
    j = 0
    Q = np.empty((m, 0), dtype=a.dtype)
    y_norms = [np.linalg.norm(Y[i]) for i in range(r)]

    while np.max(y_norms[j:j + r]) > tolerance / (10 * np.sqrt(2 / np.pi)):
        j += 1
        Y[j-1] -= Q @ (np.conj(Q).T @ Y[j-1])  # Fixed bug with index j
        q = Y[j-1] / np.linalg.norm(Y[j-1])  # Fixed bug with index j
        Q = np.concatenate((Q, q[:, None]), axis=1)
        w = rand_state.randn(n)
        Aw = a @ w
        y = Aw - Q @ (Q.T.conj() @ Aw)
        Y.append(y)
        y_norms.append(np.linalg.norm(y))
        for i in range(j, j + r - 1):  # Fixed bug with final index
            Y[i] -= q * np.dot(q.conj(), Y[i])
    return Q


def adaptive_randomized_range_finder_nolist(a, tolerance, r=5, rand_state=None):
    """ Intermediate implementation for Algo 4.2:
    adaptive_randomized_range_finder_naive enhanced using nd-array instead
    of lists  """
    if rand_state is None:
        rand_state = np.random.RandomState(None)
    if np.issubdtype(type(rand_state), np.dtype(int).type):
        rand_state = np.random.RandomState(rand_state)
    m, n = a.shape
    W = rand_state.randn(n, r)
    Y = a @ W
    y_norms = np.linalg.norm(Y, axis=0)
    j = 0
    Q = np.empty((m, 0), dtype=a.dtype)

    while np.max(y_norms[j:j + r]) > tolerance / (10 * np.sqrt(2 / np.pi)):
        Y[:, j] -= Q @ (np.conj(Q).T @ Y[:, j])
        q = Y[:, j] / np.linalg.norm(Y[:, j])
        j += 1
        Q = np.concatenate((Q, q[:, None]), axis=1)
        w = rand_state.randn(n)
        Aw = a @ w
        y = Aw - Q @ (Q.T.conj() @ Aw)
        Y = np.concatenate((Y, y[:, None]), axis=1)
        y_norms = np.concatenate((y_norms, [np.linalg.norm(y)]))
        for i in range(j, j + r - 1):
            Y[:, i] -= q * np.dot(q.conj(), Y[:, i])
    return Q


def adaptive_randomized_range_finder_circy(a, tolerance, r=5, rand_state=None):
    """ Intermediate implementation for Algo 4.2:
    adaptive_randomized_range_finder_nolist enhanced using circular array
    for Y  """
    if rand_state is None:
        rand_state = np.random.RandomState(None)
    if np.issubdtype(type(rand_state), np.dtype(int).type):
        rand_state = np.random.RandomState(rand_state)
    m, n = a.shape
    W = rand_state.randn(n, r)
    Y = a @ W
    y_norms = np.linalg.norm(Y, axis=0)
    j = 0
    j_incr = 0
    Q = np.empty((m, 0), dtype=a.dtype)

    while np.max(y_norms[j_incr:j_incr + r]) > tolerance / (10 * np.sqrt(2 / np.pi)):
        j_incr += 1
        Y[:, j] -= Q @ (np.conj(Q).T @ Y[:, j])
        q = Y[:, j] / np.linalg.norm(Y[:, j])
        j = (j + 1) % r
        Q = np.concatenate((Q, q[:, None]), axis=1)
        w = rand_state.randn(n)
        A_w = a @ w
        y = A_w - Q @ (Q.T.conj() @ A_w)
        Y[:, j - 1] = y
        y_norms = np.concatenate((y_norms, [np.linalg.norm(y)]))
        for i in np.arange(j, j + r - 1) % r:
            Y[:, i] -= q * np.dot(q.conj(), Y[:, i])
    return Q


def adaptive_randomized_range_finder_circynorms(a, tolerance, r=5,
                                                rand_state=None):
    """ Intermediate implementation for Algo 4.2:
    adaptive_randomized_range_finder_circy enhanced using circular array
    for y_norms  """
    if rand_state is None:
        rand_state = np.random.RandomState(None)
    if np.issubdtype(type(rand_state), np.dtype(int).type):
        rand_state = np.random.RandomState(rand_state)
    m, n = a.shape
    W = rand_state.randn(n, r)
    Y = a @ W
    y_norms = np.linalg.norm(Y, axis=0)
    j = 0
    Q = np.empty((m, 0), dtype=a.dtype)

    while np.max(y_norms) > tolerance / (10 * np.sqrt(2 / np.pi)):
        Y[:, j] -= Q @ (np.conj(Q).T @ Y[:, j])
        q = Y[:, j] / np.linalg.norm(Y[:, j])
        j = (j + 1) % r
        Q = np.concatenate((Q, q[:, None]), axis=1)
        w = rand_state.randn(n)
        A_w = a @ w
        y = A_w - Q @ (Q.T.conj() @ A_w)
        Y[:, j - 1] = y
        y_norms[j - 1] = np.linalg.norm(y)
        for i in np.arange(j, j + r - 1) % r:
            Y[:, i] -= q * np.dot(q.conj(), Y[:, i])
    return Q


def adaptive_randomized_range_finder_rmloop(a, tolerance, r=5,
                                            rand_state=None):
    """ Intermediate implementation for Algo 4.2:
    adaptive_randomized_range_finder_circynorms enhanced removing internal
    loop  """
    if rand_state is None:
        rand_state = np.random.RandomState(None)
    if np.issubdtype(type(rand_state), np.dtype(int).type):
        rand_state = np.random.RandomState(rand_state)
    m, n = a.shape
    W = rand_state.randn(n, r)
    Y = a @ W
    y_norms = np.linalg.norm(Y, axis=0)
    j = 0
    Q = np.empty((m, 0), dtype=a.dtype)

    while np.max(y_norms) > tolerance / (10 * np.sqrt(2 / np.pi)):
        Y[:, j] -= Q @ (Q.T.conj() @ Y[:, j])
        q = Y[:, j] / np.linalg.norm(Y[:, j])
        j = (j + 1) % r
        Q = np.concatenate((Q, q[:, None]), axis=1)
        w = rand_state.randn(n)
        A_w = a @ w
        Y -= np.outer(q, q.conj() @ Y)
        y = A_w - Q @ (Q.T.conj() @ A_w)
        Y[:, j - 1] = y
        y_norms[j - 1] = np.linalg.norm(y)
    return Q


def adaptive_randomized_range_finder_rmconcQ(a, tolerance, r=5,
                                             rand_state=None):
    """ Intermediate implementation for Algo 4.2:
    adaptive_randomized_range_finder_rmloop enhanced removing concatenation
    for Q, with maximal size for Q (needs to be reduced)  """
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
    Q = np.empty((m, min(m, n)), dtype=a.dtype)

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
        Q[:, Q_width-1] = q
        w = rand_state.randn(n)
        A_w = a @ w
        # Y -= np.outer(q, np.conj(np.conj(q) @ Y))
        Y -= np.outer(q, q.conj() @ Y)
        y = A_w - Q[:, :Q_width] @ (Q[:, :Q_width].T.conj() @ A_w)
        Y[:, j - 1] = y
        y_norms[j - 1] = np.linalg.norm(y)
    return Q[:, :Q_width]


def adaptive_randomized_range_finder_mem_alloc(a, tolerance, r=5,
                                               rand_state=None, n_cols_Q=16):
    """ Intermediate implementation for Algo 4.2:
    adaptive_randomized_range_finder_rmconcQ enhanced using memory
    allocation (subsequently optimized using resize in final version
    adaptive_randomized_range_finder)
    """
    if rand_state is None:
        rand_state = np.random.RandomState(None)
    if np.issubdtype(type(rand_state), np.dtype(int).type):
        rand_state = np.random.RandomState(rand_state)
    if isinstance(a, np.ndarray):
        a = aslinearoperator(a)
    m, n = a.shape
    W = rand_state.randn(n, r)
    Y = a @ W
    y_norms = np.linalg.norm(Y, axis=0)
    j = 0
    Q_width = 0
    Q = np.empty((m, n_cols_Q), order='F', dtype=a.dtype)

    while np.max(y_norms) > tolerance / (10 * np.sqrt(2 / np.pi)):
        if Q_width >= n:
            # TODO to be tested
            raise RuntimeError('Required tolerance not reached with maximum '
                               'number of columns ({}). Singular '
                               'values may decrease too slowly.'.format(n))
        Y[:, j] -= Q[:, :Q_width] @ (np.conj(Q[:, :Q_width]).T @ Y[:, j])
        q = Y[:, j] / np.linalg.norm(Y[:, j])
        j = (j + 1) % r
        Q_width += 1
        if Q_width > Q.shape[1]:
            Q_new = np.empty((m, Q.shape[1]*2), dtype=a.dtype)
            Q_new[:, :Q.shape[1]] = Q
            Q = Q_new
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

# TODO use similar code for measuring running times
# def main_loop():
#     from time import process_time
#     m = 1000
#     n = m
#     p_a = 10
#     m, n, p_a = 100, 100, 2
#     a_mat = build_test_matrix(m, n, p=p_a, rand_state=0)
#     a_op = aslinearoperator(a_mat)
#     from skpomade.utils import FourierMultiplierOp
#     n = 123
#     a_op = FourierMultiplierOp(n=n, p=30)
#     a_mat = a_op @ np.eye(n)
#     tolerance = 10 ** -3
#
#     def adaptive_randomized_range_finder_q2(**nargs):
#         return adaptive_randomized_range_finder(**nargs, n_cols_Q=2)
#
#     def adaptive_randomized_range_finder_q16(**nargs):
#         return adaptive_randomized_range_finder(**nargs, n_cols_Q=16)
#
#     def adaptive_randomized_range_finder_q455(**nargs):
#         return adaptive_randomized_range_finder(**nargs, n_cols_Q=455)
#
#     f_list = [adaptive_randomized_range_finder_naive,
#               adaptive_randomized_range_finder_nolist,
#               adaptive_randomized_range_finder_circy,
#               adaptive_randomized_range_finder_circynorms,
#               adaptive_randomized_range_finder_rmloop,
#               adaptive_randomized_range_finder_rmconcQ,
#               adaptive_randomized_range_finder_mem_alloc,
#               adaptive_randomized_range_finder_q2,
#               adaptive_randomized_range_finder_q16,
#               adaptive_randomized_range_finder_q455,
#               adaptive_randomized_range_finder,
#               ]
#     dt_list = np.empty(len(f_list))
#     err_list = np.empty(len(f_list))
#     for i_f, f in enumerate(f_list):
#         t0 = process_time()
#         q_mat = f(a=a_op, tolerance=tolerance, r=6, rand_state=0)
#         dt_list[i_f] = process_time() - t0
#         err_list[i_f] = np.linalg.norm(a_mat - q_mat @ q_mat.T.conj() @ a_mat,
#                                        ord=2)
#         print('t={:.2f}, gain t={:.1%}, err={:.12e}, delta err={:.2e}, '
#               'Q shape:{} ({})'
#               .format(dt_list[i_f], dt_list[i_f]/dt_list[0], err_list[i_f],
#                       abs(err_list[i_f]-err_list[0]), q_mat.shape, f.__name__))
#
#
# if __name__ == '__main__':
#     main_loop()
