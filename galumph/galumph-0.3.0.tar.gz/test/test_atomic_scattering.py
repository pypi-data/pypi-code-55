# SPDX-FileCopyrightText: 2016 European Molecular Biology Laboratory (EMBL)
# SPDX-FileCopyrightText: 2018-2020 Christopher Kerr
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from hypothesis import assume, given, settings
import hypothesis.strategies as st
import hypothesis.extra.numpy as npst
import numpy as np
import numpy.testing as npt

from galumph.atomicscattering import AtomicScattering


@st.composite
def alm_parameters(draw,
                   LMAX=st.integers(min_value=3, max_value=20),
                   smax=st.floats(min_value=0.1, max_value=10),
                   worksize=st.integers(min_value=8, max_value=64),
                   natwork=st.integers(min_value=4, max_value=16),
                   ):
    """Hypothesis strategy to get parameters for an Alm array."""
    LMAX = draw(LMAX)
    smax = draw(smax)
    nchunks = draw(st.integers(min_value=4, max_value=16))
    worksize = draw(worksize)
    natwork = draw(natwork)
    NS = worksize * nchunks
    s = np.linspace(0, smax, NS, endpoint=True)
    return dict(
        LMAX=LMAX,
        s=s,
        worksize=worksize,
        natwork=natwork,
    )


@st.composite
def atom_xyzf(draw,
              natoms=st.integers(min_value=1, max_value=5),
              xyz_elements=st.floats(min_value=-10, max_value=10, width=32),
              ff_elements=st.floats(min_value=1, max_value=10, width=32),
              min_distance=0.5,
              # TODO allow specifying s-dependent form factors
              ):
    """Hypothesis strategy to get atomic positions and form factors."""
    natoms = draw(natoms)
    xyz = draw(npst.arrays(
        shape=(natoms, 3),
        elements=xyz_elements,
        dtype=draw(st.sampled_from(('f4', 'f8'))),
    ))
    for i in range(natoms):
        for j in range(i):
            distance = np.linalg.norm(xyz[i, :] - xyz[j, :])
            assume(distance >= min_distance)
    ff = draw(npst.arrays(
        shape=(natoms,),
        elements=ff_elements,
        dtype=draw(st.sampled_from(('f4', 'f8'))),
    ))
    return (xyz, ff)


@settings(max_examples=10)
@given(
    almparams=alm_parameters(),
    xyz_ff=atom_xyzf(natoms=st.integers(min_value=2, max_value=20)),
)
def test_single_multiple(cl_context, almparams, xyz_ff):
    """Check that adding atoms one at a time and all together is the same."""
    kernel = AtomicScattering(context=cl_context, **almparams)
    alm1 = kernel.zeros()
    alm2 = kernel.zeros()
    xyz, ff = xyz_ff
    natoms = xyz.shape[0]

    kernel.add_many_atoms(alm1, xyz, ff)
    for iAt in range(natoms):
        kernel.add_atom(alm2, xyz[iAt, :], ff[iAt])

    np_alm1 = alm1.get()
    np_alm2 = alm2.get()
    npt.assert_allclose(np_alm1, np_alm2, rtol=1e-3, atol=1e-5)


@settings(max_examples=10)
@given(
    almparams=alm_parameters(),
    xyz_ff=atom_xyzf(natoms=st.integers(min_value=2, max_value=20)),
    hyp=st.data(),
)
def test_reorder_atoms(cl_context, almparams, xyz_ff, hyp):
    """Check that Alm is independent of the order in which atoms are added."""
    kernel = AtomicScattering(context=cl_context, **almparams)
    xyz, ff = xyz_ff
    natoms = xyz.shape[0]

    alm1 = kernel(xyz, ff)

    permutation = list(hyp.draw(st.permutations(range(natoms))))
    xyz2 = xyz[permutation, :]
    ff2 = ff[permutation]
    alm2 = kernel(xyz2, ff2)

    np_alm1 = alm1.get()
    np_alm2 = alm2.get()
    npt.assert_allclose(np_alm1, np_alm2, rtol=1e-4, atol=1e-6)
