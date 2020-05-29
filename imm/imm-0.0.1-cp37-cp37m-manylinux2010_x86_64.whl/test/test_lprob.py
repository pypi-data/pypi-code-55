from math import log

from imm import lprob_normalize
from imm.testing import assert_allclose


def test_lprob_normalize():
    arr = [log(0.3), log(0.001), log(3.4)]
    arr = lprob_normalize(arr)
    assert_allclose(arr, [-2.512575857729955, -8.216358332386156, -0.08482762178190328])
