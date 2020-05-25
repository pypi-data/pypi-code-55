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
"""Utils classes and functions for skpomade.

.. moduleauthor:: Valentin Emiya
"""
import numpy as np
from scipy.sparse.linalg import LinearOperator


def build_test_matrix(m, n, p=10, rand_state=None, is_complex=False):
    if rand_state is None:
        rand_state = np.random.RandomState(None)
    if np.issubdtype(type(rand_state), np.dtype(int).type):
        rand_state = np.random.RandomState(rand_state)
    if is_complex:
        raise NotImplementedError()
    A = rand_state.randn(m, n)
    A = A / np.linalg.norm(A, ord=2)
    return np.linalg.matrix_power(A @ A.T.conj(), p) @ A


def build_random_psd_matrix(n, p=0, rank=None, rand_state=None,
                            is_complex=False):
    """
    Generates a random positive semidefinite matrix

    Parameters
    ----------
    n
    p
    rank
    rand_state
    is_complex

    Returns
    -------

    """
    if rank is None:
        rank = n
    if rand_state is None:
        rand_state = np.random.RandomState(None)
    if np.issubdtype(type(rand_state), np.dtype(int).type):
        rand_state = np.random.RandomState(rand_state)

    if is_complex:
        B = rand_state.randn(n, rank) + 1j*rand_state.randn(n, rank)
    else:
        B = rand_state.randn(n, rank)
    A = B @ B.T.conj()
    A = A / np.linalg.norm(A, ord=2)
    return np.linalg.matrix_power(A @ A.T.conj(), p) @ A


class FourierMultiplierOp(LinearOperator):
    def __init__(self, n, p=1):
        self.w = np.random.rand(n) ** p
        LinearOperator.__init__(self,
                                shape=(self.w.size, self.w.size),
                                dtype=np.complex_)

    def _matvec(self, x):
        if x.ndim == 2:
            return self._matmat(x)
        return np.fft.ifft(np.fft.fft(x) * self.w)

    def _matmat(self, x):
        return np.fft.ifft(np.fft.fft(x, axis=0) * self.w[:, None], axis=0)

    def _adjoint(self):
        return self
