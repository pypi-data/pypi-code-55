# SPDX-FileCopyrightText: 2016 European Molecular Biology Laboratory (EMBL)
# SPDX-FileCopyrightText: 2018-2020 Christopher Kerr
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from hypothesis import assume, given, HealthCheck, settings
import hypothesis.strategies as st
import numpy as np
import numpy.testing as npt
from scipy.stats import linregress

from galumph.atomicscattering import AtomicScattering
from galumph.intensity import Intensity

# Import test strategies from test_atomic_scattering
from test_atomic_scattering import alm_parameters, atom_xyzf


def structure_Guinier(xyz, ff):
    I0 = np.sum(ff)**2

    centre = np.dot(xyz.T, ff) / np.sum(ff)
    r2 = np.sum((xyz - centre[np.newaxis, :])**2, axis=1)
    rG = np.dot(r2, ff) / np.sum(ff)

    return rG, I0


def scattering_Guinier(s, I_s, rGest=None):
    if rGest:
        fitrange = (s <= (1/rGest))
        s = s[fitrange]
        I_s = I_s[fitrange]

    result = linregress(s**2, np.log(I_s))
    rG = -3 * result[0]
    I0 = np.exp(result[1])

    return rG, I0


@settings(max_examples=10)
@given(
    almparams=alm_parameters(),
    xyz_ff1=atom_xyzf(),
    xyz_ff2=atom_xyzf(),
)
def test_cross_intensity(cl_context, cl_queue, almparams, xyz_ff1, xyz_ff2):
    """Test scattering from two separate structures vs. a combined structure.

    The cross scattering plus the self scattering of the two substructures
    should be equal to the self scattering of the combined structure.
    """
    scattering_kernel = AtomicScattering(context=cl_context, **almparams)
    intensity_kernel = Intensity(context=cl_context,
                                 worksize=almparams['worksize'])

    xyz1, ff1 = xyz_ff1
    xyz2, ff2 = xyz_ff2

    ev_alm1, alm1 = scattering_kernel(xyz1, ff1, queue=cl_queue)
    ev_alm2, alm2 = scattering_kernel(xyz2, ff2, queue=cl_queue)

    xyzboth = np.concatenate((xyz1, xyz2), axis=0)
    ffboth = np.concatenate((ff1, ff2), axis=0)
    ev_almboth, almboth = scattering_kernel(xyzboth, ffboth, queue=cl_queue)

    ev_alm1.wait()
    ev1, int1 = intensity_kernel(alm1, queue=cl_queue)
    ev_alm2.wait()
    ev2, int2 = intensity_kernel(alm2, queue=cl_queue)
    evcross, intcross = intensity_kernel.cross(alm1, alm2, queue=cl_queue)

    ev_almboth.wait()
    evboth, intboth = intensity_kernel(almboth, queue=cl_queue)

    cl_queue.finish()
    int1 = int1.get()
    int2 = int2.get()
    intcross = intcross.get()
    intboth = intboth.get()

    npt.assert_allclose(int1 + int2 + intcross, intboth, rtol=1e-4, atol=1e-6)


@settings(max_examples=10,
          # Getting a suitable xyz array requires a lot of filtering
          suppress_health_check=[HealthCheck.filter_too_much])
@given(
    almparams=alm_parameters(
        # need a larger LMAX to get a good fit
        LMAX=st.integers(min_value=20, max_value=30),
        smax=st.floats(min_value=0.3, max_value=3),
        natwork=st.just(16),
    ),
    xyz_ff=atom_xyzf(natoms=st.integers(min_value=2, max_value=20)),
)
def test_Guinier(cl_context, almparams, xyz_ff):
    """Check that the calculated intensity has a sensible Guinier plot.

    Calculates rG and I0 from the Guinier plot and from the atomic structure
    and checks that the two match.
    """
    s = almparams['s']
    scattering_kernel = AtomicScattering(context=cl_context, **almparams)
    intensity_kernel = Intensity(context=cl_context,
                                 worksize=almparams['worksize'])
    xyz, ff = xyz_ff
    # Center the xyz array (not accounting for form factor)
    xyz_mean = np.mean(xyz, axis=0)
    xyz -= xyz_mean[None, :]

    rGxyz, I0xyz = structure_Guinier(xyz, ff)
    # without this, hypothesis gives us structures with all atoms at the origin
    assume(rGxyz * s[-1] > 0.5)
    # or structures where the s step is too big
    assume(rGxyz * s[1] < 0.1)

    alm = scattering_kernel(xyz, ff)
    Icalc_dev = intensity_kernel(alm)
    Icalc = Icalc_dev.get()
    rGalm, I0alm = scattering_Guinier(s, Icalc, rGxyz)

    npt.assert_approx_equal(I0alm, I0xyz, significant=2)
    npt.assert_approx_equal(rGalm, rGxyz, significant=1)
