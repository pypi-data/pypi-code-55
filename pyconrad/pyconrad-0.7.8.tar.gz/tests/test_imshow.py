import os

import numpy as np
import pytest

import pyconrad.autoinit


@pytest.mark.skipif("CI" in os.environ and os.environ["CI"] == "true", reason="Skipping this test on Travis CI.")
def test_imshow():
    import ij
    a = np.random.rand(20, 30)
    luts = ['Fire', 'Spectrum', 'Ice', 'Cyan']

    for lut in luts:
        pyconrad.imshow(a, lut=lut)

    ij.WindowManager.closeAllWindows()

    actions = ['FFT']

    for action in actions:
        pyconrad.imshow(a, run=action, lut='Fire')

    ij.WindowManager.closeAllWindows()

    actions = ['FFT']

    for action in actions:
        pyconrad.imshow(a, "foo", run=action, lut='Fire')


@pytest.mark.skipif("CI" in os.environ and os.environ["CI"] == "true", reason="Skipping this test on Travis CI.")
def test_tile():
    a = np.random.rand(20, 30)
    luts = ['Fire', 'Spectrum', 'Ice', 'Cyan']

    for lut in luts:
        pyconrad.imshow(a, title=lut, lut=lut)
    pyconrad.tile()


@pytest.mark.skipif("CI" in os.environ and os.environ["CI"] == "true", reason="Skipping this test on Travis CI.")
def test_tile_always():
    a = np.random.rand(20, 30)
    luts = ['Fire', 'Spectrum', 'Ice', 'Cyan']

    pyconrad.tile(always=True)
    for lut in luts:
        pyconrad.imshow(a, title=lut, lut=lut)


@pytest.mark.skipif("CI" in os.environ and os.environ["CI"] == "true", reason="Skipping this test on Travis CI.")
def test_cascade_always():
    a = np.random.rand(20, 30)
    luts = ['Fire', 'Spectrum', 'Ice', 'Cyan']

    pyconrad.tile(always=True)
    pyconrad.cascade(always=True)
    for lut in luts:
        pyconrad.imshow(a, title=lut, lut=lut)


@pytest.mark.skipif("CI" in os.environ and os.environ["CI"] == "true", reason="Skipping this test on Travis CI.")
def test_cascade():
    a = np.random.rand(20, 30)
    luts = ['Fire', 'Spectrum', 'Ice', 'Cyan']

    pyconrad.tile(always=True)
    for lut in luts:
        pyconrad.imshow(a, title=lut, lut=lut)
    pyconrad.cascade(always=True)


@pytest.mark.skipif("CI" in os.environ and os.environ["CI"] == "true", reason="Skipping this test on Travis CI.")
def test_3d():
    a = np.random.rand(20, 30, 40)
    luts = ['Fire', 'Spectrum', 'Ice', 'Cyan']

    for lut in luts:
        pyconrad.imshow(a, title=lut)
