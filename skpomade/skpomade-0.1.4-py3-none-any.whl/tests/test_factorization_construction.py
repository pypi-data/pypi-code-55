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

"""Test of the module :module:`skpomade.factorization_construction`

.. moduleauthor:: Valentin Emiya
"""
import unittest
import numpy as np
from scipy.sparse.linalg import aslinearoperator, eigs, svds

from skpomade.factorization_construction import direct_svd, evd_nystrom
from skpomade.range_approximation import randomized_range_finder
from skpomade.utils import \
    build_random_psd_matrix, build_test_matrix, FourierMultiplierOp


class TestDirectSvd(unittest.TestCase):
    # TODO add test with complex matrices
    def test_approximation_error_from_true_range(self):
        """ Check equation (5.2) using true left singular vectors as matrix Q
        """
        m = 47
        n = 53
        q_width = 41
        p = 0

        a = build_test_matrix(m=m, n=n, p=p, rand_state=None)
        u_true, s_true, vh_true = svds(a, k=q_width)

        # Call to tested code
        u_est, s_est, vh_est = direct_svd(a_mat=a, q_mat=u_true)
        
        eps = np.linalg.norm(a - u_true @ np.diag(s_true) @ vh_true)
        err = np.linalg.norm(a - u_est @ np.diag(s_est) @ vh_est)
        try:
            self.assertLessEqual(err, eps)
        except AssertionError:
            np.testing.assert_almost_equal(err - eps, 0)

    def test_approximation_error_from_q_est(self):
        """ Check equation (5.2) using matrix Q estimated with randomized
        range finder.
        """
        m = 47
        n = 53
        q_width = 41
        p = 0

        a = build_test_matrix(m=m, n=n, p=p, rand_state=None)
        q = randomized_range_finder(a=a, n_l=q_width)

        # Call to tested code
        u_est, s_est, vh_est = direct_svd(a_mat=a, q_mat=q)

        eps = np.linalg.norm(a - q @ q.T.conj() @ a)
        err = np.linalg.norm(a - u_est @ np.diag(s_est) @ vh_est)
        try:
            self.assertLessEqual(err, eps)
        except AssertionError:
            np.testing.assert_almost_equal(err - eps, 0)


class TestEvdNystrom(unittest.TestCase):
    def setUp(self):
        n = 53
        p = 0
        self.a_dict = {False: build_random_psd_matrix(n=n,
                                                      p=p,
                                                      rank=None,
                                                      rand_state=None,
                                                      is_complex=False),
                       True: build_random_psd_matrix(n=n,
                                                     p=p,
                                                     rank=None,
                                                     rand_state=None,
                                                     is_complex=True)}

    def test_approximation_error_from_true_range(self):
        """ Check equation (5.2) using true left singular vectors as matrix Q
        """
        k = 41
        for is_complex in (False, True):
            a = self.a_dict[is_complex]
            s_true, u_true = eigs(a, k=k)
            q = u_true

            # Call to tested code
            s_est, u_est = evd_nystrom(a=a, q_mat=q)

            eps = np.linalg.norm(a - q @ q.T.conj() @ a)
            err = np.linalg.norm(a - u_est @ np.diag(s_est) @ u_est.T.conj())
            try:
                self.assertLessEqual(
                    err, eps, msg='is_complex={}'.format(is_complex))
            except AssertionError:
                np.testing.assert_almost_equal(
                    err - eps, 0, err_msg='is_complex={}'.format(is_complex))

    def test_approximation_error_from_q_est(self):
        """ Check equation (5.2) using matrix Q estimated with randomized
        range finder.
        """
        k = 41
        for is_complex in (False, True):
            a = self.a_dict[is_complex]
            q = randomized_range_finder(a=a, n_l=k)

            # Call to tested code
            s_est, u_est = evd_nystrom(a=a, q_mat=q)

            eps = np.linalg.norm(a - q @ q.T.conj() @ a)
            err = np.linalg.norm(a - u_est @ np.diag(s_est) @ u_est.T.conj())
            try:
                self.assertLessEqual(
                    err, eps, msg='is_complex={}'.format(is_complex))
            except AssertionError:
                np.testing.assert_almost_equal(
                    err - eps, 0, err_msg='is_complex={}'.format(is_complex))

    def test_approximation_error_operator(self):
        """ Check equation (5.2) with A as an operator.
        """
        n = 53
        n_l = 41
        p = 5
        a_op = FourierMultiplierOp(n, p)
        q = randomized_range_finder(a=a_op, n_l=n_l)

        # Call to tested code
        s_est, u_est = evd_nystrom(a=a_op, q_mat=q)

        q_op = aslinearoperator(q)
        qh_op = aslinearoperator(q.T.conj())
        eps = eigs(a_op - q_op @ qh_op @ a_op, k=1)[0][0]

        a_op_est = aslinearoperator(u_est @ np.diag(s_est) @ u_est.T.conj())
        err = eigs(a_op - a_op_est, k=1)[0][0]

        try:
            self.assertLessEqual(err, eps)
        except AssertionError:
            np.testing.assert_almost_equal(err - eps, 0)
