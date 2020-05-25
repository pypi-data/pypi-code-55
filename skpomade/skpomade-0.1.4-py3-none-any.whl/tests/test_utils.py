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

"""Test of the module :module:`skpomade.utils`

.. moduleauthor:: Valentin Emiya
"""
import unittest

import numpy as np

from skpomade.utils import \
    build_test_matrix, build_random_psd_matrix, FourierMultiplierOp


class TestBuildRandomMatrix(unittest.TestCase):
    def test_real(self):
        m, n, p = 13, 17, 1
        for rand_state in (None, 0):
            a_mat = build_test_matrix(m=m, n=n, p=p, rand_state=rand_state)
            np.testing.assert_array_equal(a_mat.shape, (m, n))
            self.assertFalse(np.iscomplexobj(a_mat))


class TestBuildRandomPsdMatrix(unittest.TestCase):
    def test_real(self):
        n = 29
        is_complex = False
        for p in (0, 1):
            for rand_state in (None, 0):
                a_mat = build_random_psd_matrix(n=n,
                                            p=p,
                                            rank=None,
                                            rand_state=rand_state,
                                            is_complex=is_complex)
                s_vec, _ = np.linalg.eig(a_mat)

                np.testing.assert_array_equal(a_mat.shape, (n, n))
                self.assertFalse(np.iscomplexobj(a_mat))
                np.testing.assert_array_almost_equal(np.imag(s_vec), 0)
                np.testing.assert_array_equal(np.real(s_vec) > 0, True)

    def test_cpx(self):
        n = 19
        is_complex = True
        for p in (0, 1):
            a_mat = build_random_psd_matrix(n=n,
                                            p=p,
                                            rank=None,
                                            rand_state=None,
                                            is_complex=is_complex)
            s_vec, _ = np.linalg.eig(a_mat)

            np.testing.assert_array_equal(a_mat.shape, (n, n))
            self.assertTrue(np.iscomplexobj(a_mat))
            np.testing.assert_array_almost_equal(np.imag(s_vec), 0)
            np.testing.assert_array_equal(np.real(s_vec) > 0, True)

    def test_rank(self):
        n = 17
        r = 11
        is_complex = True
        for p in (0, 1):
            a_mat = build_random_psd_matrix(n=n,
                                            p=p,
                                            rank=r,
                                            rand_state=None,
                                            is_complex=is_complex)
            s_vec, _ = np.linalg.eig(a_mat)
            s_vec.sort()
            s_vec = s_vec[::-1]

            np.testing.assert_array_equal(a_mat.shape, (n, n))
            self.assertTrue(np.iscomplexobj(a_mat))
            np.testing.assert_array_almost_equal(np.imag(s_vec), 0)
            np.testing.assert_array_equal(np.real(s_vec[:r]) > 0, True)
            np.testing.assert_array_almost_equal(np.real(s_vec[r:]), 0)
            np.testing.assert_array_equal(np.isclose(np.real(s_vec[:r]), 0),
                                          False)


class TestFourierMultiplierOp(unittest.TestCase):
    def test_fourier_mult_op_vec(self):
        n = 29
        for p in (0, 1, 5):
            op = FourierMultiplierOp(n=n, p=p)
            np.testing.assert_array_equal(op.shape, (n, n))

            w = op.w
            x = np.random.randn(n)
            y = np.fft.ifft(w * np.fft.fft(x))
            np.testing.assert_array_almost_equal(op(x), y)
            np.testing.assert_array_almost_equal(op @ x, y)
            # Auto-adjoint
            np.testing.assert_array_almost_equal(op.H(x), y)
            np.testing.assert_array_almost_equal(op.H @ x, y)

    def test_fourier_mult_op_mat1(self):
        n = 17
        n_samples = 1
        for p in (0, 1, 7):
            op = FourierMultiplierOp(n=n, p=p)
            np.testing.assert_array_equal(op.shape, (n, n))

            w = op.w
            x_mat = np.random.randn(n, n_samples)
            y = np.fft.ifft(w[:, None] * np.fft.fft(x_mat, axis=0), axis=0)
            np.testing.assert_array_almost_equal(op(x_mat), y)
            np.testing.assert_array_almost_equal(op @ x_mat, y)
            # Auto-adjoint
            np.testing.assert_array_almost_equal(op.H(x_mat), y)
            np.testing.assert_array_almost_equal(op.H @ x_mat, y)

    def test_fourier_mult_op_mat7(self):
        n = 22
        n_samples = 7
        for p in (0, 1, 4):
            op = FourierMultiplierOp(n=n, p=p)
            np.testing.assert_array_equal(op.shape, (n, n))

            w = op.w
            x_mat = np.random.randn(n, n_samples)
            y = np.fft.ifft(w[:, None] * np.fft.fft(x_mat, axis=0), axis=0)
            np.testing.assert_array_almost_equal(op(x_mat), y)
            np.testing.assert_array_almost_equal(op @ x_mat, y)
            # Auto-adjoint
            np.testing.assert_array_almost_equal(op.H(x_mat), y)
            np.testing.assert_array_almost_equal(op.H @ x_mat, y)
