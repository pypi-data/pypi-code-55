# SPDX-FileCopyrightText: 2018-2020 Christopher Kerr
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from hypothesis import given, settings
import hypothesis.strategies as st
import numpy as np
import numpy.testing as npt

from galumph.atomicscattering import AtomicScattering
from galumph.rotalm import RotateAlm

# Import test strategies from test_atomic_scattering
from test_atomic_scattering import alm_parameters, atom_xyzf


@given(
    LMAX=st.integers(min_value=0, max_value=2),
    beta=st.floats(min_value=-np.pi, max_value=np.pi),
)
def test_beta_rotation_matrix_analytical(cl_context, LMAX, beta):
    """Compare early elements of the dlmm matrix with analytical solutions."""
    kernel = RotateAlm(context=cl_context, LMAX=LMAX, NSWORK=8)
    dlmm_dev = kernel.y_rotation_matrix(beta)
    dlmm = dlmm_dev.get()
    # N.B. in the Wikipedia article, the M2 comes before the M1
    npt.assert_approx_equal(dlmm[0], 1)
    if LMAX == 0:
        return
    cosbeta = np.cos(beta)
    sinbeta = np.sin(beta)
    sqrt2 = np.sqrt(2)
    analytical_dlmm_1 = np.array([[
        0,  # -1, 0  # TODO remove
        (1 - cosbeta) / 2,  # -1, 1
    ], [
        cosbeta,  # 0, 0
        -sinbeta / sqrt2,  # 0, 1
    ], [
        0,  # 1, 0  # TODO remove
        (1 + cosbeta) / 2,  # 1, 1
    ]])
    analytical_dlmm_1[0, 0] = analytical_dlmm_1[1, 1]
    analytical_dlmm_1[2, 0] = -analytical_dlmm_1[1, 1]

    dlmm_1 = dlmm[1:7].reshape((3, 2))
    npt.assert_allclose(dlmm_1, analytical_dlmm_1, rtol=1e-4, atol=1e-6)
    if LMAX == 1:
        return
    cos2beta = cosbeta**2
    sqrt38 = np.sqrt(3/8)

    analytical_dlmm_2 = np.array([[
        0,  # -2, 0  # TODO remove
        0,  # -2, 1  # TODO remove
        (1 - cosbeta)**2 / 4,  # -2, 2
    ], [
        0,  # -1, 0  # TODO remove
        (-2 * cos2beta + cosbeta + 1) / 2,  # -1, 1
        -sinbeta * (1 - cosbeta) / 2,  # -1, 2
    ], [
        (3 * cos2beta - 1) / 2,  # 0, 0
        -sqrt38 * np.sin(2*beta),  # 0, 1
        sqrt38 * sinbeta**2,  # 0, 2
    ], [
        0,  # 1, 0  # TODO remove
        (2 * cos2beta + cosbeta - 1) / 2,  # 1, 1
        -sinbeta * (1 + cosbeta) / 2,  # 1, 2
    ], [
        0,  # 2, 0  # TODO remove
        0,  # 2, 1  # TODO remove
        (1 + cosbeta)**2 / 4,  # 2, 2
    ]])
    # Apply symmetry - TODO pack the array more
    for M1 in range(-2, 3):
        iM1 = 2 + M1
        for M2 in range(3):
            if M1 > M2:
                # d[M2,M1] = -1^(M2-M1) * d[M1,M2]
                sign = 1 - 2 * ((M1 - M2) % 2)
                analytical_dlmm_2[iM1, M2] = sign * analytical_dlmm_2[2+M2, M1]
            elif -M1 > M2:
                # d[-M2,-M1] = d[M1,M2]
                analytical_dlmm_2[iM1, M2] = analytical_dlmm_2[2-M2, -M1]

    dlmm_2 = dlmm[7:].reshape((5, 3))
    npt.assert_allclose(dlmm_2, analytical_dlmm_2, rtol=1e-4, atol=1e-6)


@settings(max_examples=10)
@given(
    almparams=alm_parameters(worksize=st.integers(min_value=1, max_value=16)),
    xyz_ff=atom_xyzf(xyz_elements=st.floats(min_value=-5, max_value=5, width=32)),
    alpha=st.floats(min_value=-np.pi, max_value=np.pi),
    beta=st.floats(min_value=-np.pi, max_value=np.pi),
    gamma=st.floats(min_value=-np.pi, max_value=np.pi),
)
def test_atomic_scattering_rotated(cl_context, cl_queue, almparams, xyz_ff,
                                   alpha, beta, gamma):
    """Compare rotating the Alm versus rotating the atomic positions."""
    scattering_kernel = AtomicScattering(context=cl_context, **almparams)
    rotation_kernel = RotateAlm(context=cl_context,
                                LMAX=almparams['LMAX'],
                                NSWORK=almparams['worksize'],)
    xyz, ff = xyz_ff

    alm_orig = scattering_kernel(xyz, ff)

    ev, alm_rotalm = rotation_kernel(alm_orig, alpha, beta, gamma,
                                     queue=cl_queue)

    rotate_alpha = np.array([[np.cos(alpha), np.sin(alpha), 0],
                             [-np.sin(alpha), np.cos(alpha), 0],
                             [0, 0, 1]])
    rotate_beta = np.array([[np.cos(beta), 0, -np.sin(beta)],
                            [0, 1, 0],
                            [np.sin(beta), 0, np.cos(beta)]])
    rotate_gamma = np.array([[np.cos(gamma), np.sin(gamma), 0],
                             [-np.sin(gamma), np.cos(gamma), 0],
                             [0, 0, 1]])
    rotation = np.dot(rotate_alpha, np.dot(rotate_beta, rotate_gamma))
    xyzrot = np.dot(xyz, rotation)
    alm_rotxyz = scattering_kernel(xyzrot, ff)

    ev.wait()
    np_alm_rotalm = alm_rotalm.get(unpack=True)
    # M==0 terms should be real
    npt.assert_array_almost_equal(np_alm_rotalm[:, 0, :].imag, 0, decimal=4)

    tolerance_factor = max(1, np.max(xyz) * np.max(ff) * np.max(almparams['s']))
    np_alm_rotxyz = alm_rotxyz.get(unpack=True)
    npt.assert_allclose(np_alm_rotalm, np_alm_rotxyz,
                        rtol=1e-3 * tolerance_factor,
                        atol=1e-5 * tolerance_factor)
