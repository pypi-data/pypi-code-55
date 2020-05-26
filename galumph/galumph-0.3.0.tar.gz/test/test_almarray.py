# SPDX-FileCopyrightText: 2018 Christopher Kerr
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from hypothesis import given
import hypothesis.strategies as st
import numpy as np
import numpy.testing as npt

from galumph import almarray


@given(
    cq=st.sampled_from(('context', 'queue')),
    LMAX=st.integers(min_value=0, max_value=63),
    NS=st.integers(min_value=1, max_value=1024),
)
def test_alm_constructor(cl_context, cl_queue, cq, LMAX, NS):
    """Test allocating an Alm array."""
    if cq == 'context':
        cq = cl_context
    else:
        cq = cl_queue
    alm = almarray.AlmArray(cq, LMAX, NS)
    NLM = (LMAX + 1) * (LMAX + 2) // 2
    assert alm.NLM == NLM
    assert alm.shape == (NLM, NS)


@given(
    LMAX=st.integers(min_value=0, max_value=7),
    NS=st.integers(min_value=1, max_value=64),
)
def test_alm_unpack(cl_queue, LMAX, NS):
    """Test the get() function on an AlmArray."""
    alm = almarray.zeros(cl_queue, LMAX, NS)
    # TODO fill with non-uniform values to test that unpacked values are in
    # the correct order
    alm.fill(np.complex64(1-2j))
    npalm = alm.get(unpack=True)
    assert npalm.shape == (LMAX+1, LMAX+1, NS)
    for L in range(LMAX+1):
        for M in range(LMAX+1):
            if M > L:
                npt.assert_array_equal(npalm[L, M, :], 0)
            else:
                npt.assert_array_equal(npalm[L, M, :], 1-2j)
