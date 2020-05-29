from math import isclose


def assert_allclose(actual, desired, rtol=1e-07, atol=0):
    try:
        actual = list(actual)
        desired = list(desired)
    except TypeError:
        assert isclose(actual, desired, rel_tol=rtol, abs_tol=atol)
        return

    assert len(actual) == len(desired)
    for a, d in zip(actual, desired):
        assert isclose(a, d, rel_tol=rtol, abs_tol=atol)
