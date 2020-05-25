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
""" Algorithms for Stage B: Construction of Standard Factorizations

.. moduleauthor:: Valentin Emiya
"""
import numpy as np
from numpy.linalg import cholesky  # TODO check np vs sp implementations
from scipy.linalg import solve_triangular
from scipy.sparse.linalg import aslinearoperator, eigs, svds


def direct_svd(a_mat, q_mat):
    """
    Algo 5.1: direct SVD

    Parameters
    ----------
    a_mat : nd-array
        Positive semidefinite matrix to be decomposed
    q_mat : nd-array
        Matrix whose range captures the action of a_mat

    Returns
    -------
    u_mat: nd-array
        Eigenvectors
    lambda_vec :
        Eigenvalues

    """
    b_mat = q_mat.T.conj() @ a_mat
    u_tilde, lambda_vec, vh_mat = np.linalg.svd(b_mat, full_matrices=False)
    u_mat = q_mat @ u_tilde
    return u_mat, lambda_vec, vh_mat


def evd_nystrom(a, q_mat):
    """
    Algo 5.5: Eigenvalue decomposition via Nyström method

    Parameters
    ----------
    a : nd-array or LinearOperator
        Positive semidefinite matrix or linear operator to be decomposed
    q_mat : nd-array
        Matrix whose range captures the action of a_mat

    Returns
    -------
    u_mat: nd-array
        Eigenvectors
    lambda_vec :
        Eigenvalues
    """
    if isinstance(a, np.ndarray):
        a = aslinearoperator(a)
    b1_mat = a(q_mat)
    b2_mat = q_mat.T.conj() @ b1_mat
    c = cholesky(b2_mat).T.conj()
    f_mat = solve_triangular(a=c.T, b=b1_mat.T, lower=True).T
    u_mat, sigma, _ = np.linalg.svd(f_mat, full_matrices=False)
    return sigma**2, u_mat


# TODO refactor this code into nb
# if __name__ == '__main__':
#     from skpomade.range_approximation import randomized_range_finder
#     import matplotlib.pyplot as plt
#     from skpomade.utils import FourierMultiplierOp
#     print('Test evd with operator')
#
#     n = 53
#     n_l = 41
#     p = 5
#     a_op = FourierMultiplierOp(n, p)
#     q = randomized_range_finder(a_mat=a_op, n_l=n_l)
#     w_sort = np.sort(a_op.w)[::-1]
#     plt.semilogy(w_sort, label='w')
#     print('sing value:', w_sort[n_l])
#     q_op = aslinearoperator(q)
#     qh_op = aslinearoperator(q.T.conj())
#     range_err_op = a_op - q_op @ qh_op @ a_op
#     print('range approx error:', eigs(range_err_op, k=1)[0][0])
#     # u51, s51, vh51 = direct_svd(a_mat=a_op, q_mat=q)
#     # print(eigs(
#     #     aslinearoperator(SvdErrOp(a_op=a_op, u=u51, s=s51, vh=vh51), k=1)))
#     s55, u55 = evd_nystrom(a_mat=a_op, q_mat=q)
#     a_est = u55 @ np.diag(s55) @ u55.T.conj()
#     print(eigs(a_op - aslinearoperator(a_est))[0][0])
#
#     plt.grid()
#     plt.legend()
#     e = a_op - aslinearoperator(u55 @ np.diag(s55) @ u55.T.conj())
