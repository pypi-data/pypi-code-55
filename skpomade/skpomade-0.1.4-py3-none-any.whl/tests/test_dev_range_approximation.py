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

"""Test of the module :module:`skpomade._dev_range_approximation`

.. moduleauthor:: Valentin Emiya
"""
import unittest
import numpy as np

from scipy.sparse.linalg import aslinearoperator, svds

from skpomade.range_approximation import adaptive_randomized_range_finder
from skpomade.utils import \
    build_random_psd_matrix, build_test_matrix, FourierMultiplierOp
from skpomade._dev_range_approximation import \
    adaptive_randomized_range_finder_naive, \
    adaptive_randomized_range_finder_nolist, \
    adaptive_randomized_range_finder_circy, \
    adaptive_randomized_range_finder_circynorms, \
    adaptive_randomized_range_finder_rmloop, \
    adaptive_randomized_range_finder_rmconcQ, \
    adaptive_randomized_range_finder_mem_alloc


class TestDevAdaptiveRandomizedRangeFinder(unittest.TestCase):
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
            'Fourier multiplier': FourierMultiplierOp(n=n, p=30)
        }
        self.f_list = [
            adaptive_randomized_range_finder_naive,
            adaptive_randomized_range_finder_nolist,
            adaptive_randomized_range_finder_circy,
            adaptive_randomized_range_finder_circynorms,
            adaptive_randomized_range_finder_rmloop,
            adaptive_randomized_range_finder_rmconcQ,
            adaptive_randomized_range_finder_mem_alloc,
            adaptive_randomized_range_finder,
        ]

    def test_approximation_error(self):
        """ Check equation (4.2).
        """
        tolerance = 1e-3
        r = 6
        for rand_state in (None, 0):
            for k_a in self.a_dict:
                err = []
                a = self.a_dict[k_a]
                for f in self.f_list:
                    q = f(a=a, tolerance=tolerance, r=r, rand_state=rand_state)

                    a_op = aslinearoperator(a)
                    q_op = aslinearoperator(q)
                    err.append(svds(a_op - q_op @ q_op.H @ a_op, k=1)[1][0])
                    self.assertLessEqual(err[-1], tolerance, msg='Case ' + k_a)
                if rand_state is not None: # Use same seed to compare results
                    np.testing.assert_array_almost_equal(err[:-1], err[1:],
                                                         err_msg='Case ' + k_a)
