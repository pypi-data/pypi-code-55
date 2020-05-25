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

"""Test of the module :module:`skpomade.range_approximation`

.. moduleauthor:: Valentin Emiya
"""
import unittest
import numpy as np

from scipy.sparse.linalg import aslinearoperator, svds

from skpomade.range_approximation import \
    randomized_range_finder, adaptive_randomized_range_finder
from skpomade.utils import \
    build_random_psd_matrix, build_test_matrix, FourierMultiplierOp


# TODO to be implemented: approximation, time, complex values
class TestRandomizedRangeFinder(unittest.TestCase):
    def setUp(self) -> None:
        m = 47
        n = 53
        self.a_dict = {
            'random matrix':
                build_test_matrix(m=m, n=n, p=0, rand_state=None),
            'operator from random matrix':
                aslinearoperator(build_test_matrix(m=m, n=n, p=2,
                                                   rand_state=None)),
            'PSD matrix':
                build_random_psd_matrix(n=n, rank=m, p=0, rand_state=None),
            'Fourier multiplier': FourierMultiplierOp(n=n)
        }

    def test_approximation_error(self):
        """ Check equation (1.9).
        """

        k = 25
        p = 5
        for k_a in self.a_dict:
            a = self.a_dict[k_a]
            m, n = a.shape

            # code to be tested
            q_width = k + p
            q = randomized_range_finder(a=a, n_l=q_width)

            a_op = aslinearoperator(a)
            q_op = aslinearoperator(q)
            _, s_true, _ = svds(a, k=k+1)
            err = svds(a_op - q_op @ q_op.H @ a_op, k=1)[0][0]
            err_bound = (1 + 9 * np.sqrt((k + p) * min(m, n))) * s_true[k]
            self.assertLessEqual(err, err_bound, msg='Case ' + k_a)


class TestAdaptiveRandomizedRangeFinder(unittest.TestCase):
    def setUp(self) -> None:
        m = 79
        n = 123
        self.a_dict = {
            'random matrix':
                build_test_matrix(m=m, n=n, p=5, rand_state=None),
            'operator from random matrix':
                aslinearoperator(build_test_matrix(m=m, n=n, p=5,
                                                   rand_state=None)),
            'PSD matrix':
                build_random_psd_matrix(n=n, rank=m, p=5, rand_state=None),
            'Fourier multiplier': FourierMultiplierOp(n=n, p=20)
        }

    def test_approximation_error(self):
        """ Check equation (4.2).
        """
        # raise NotImplementedError
        # TODO debug this test, takes too much time (loop in
        #  adaptive_randomized_range_finder)
        # k = 11
        # p = 5
        tolerance = 1e-4
        r = 6
        proba = None
        rand_state = None
        n_cols_Q = 4
        for k_a in self.a_dict:
            a = self.a_dict[k_a]

            q = adaptive_randomized_range_finder(a=a,
                                                 tolerance=tolerance,
                                                 r=r,
                                                 proba=proba,
                                                 rand_state=rand_state,
                                                 n_cols_Q=n_cols_Q
                                                 )

            a_op = aslinearoperator(a)
            q_op = aslinearoperator(q)
            err = svds(a_op - q_op @ q_op.H @ a_op, k=1)[1][0]
            self.assertLessEqual(err, tolerance, msg='Case ' + k_a)
