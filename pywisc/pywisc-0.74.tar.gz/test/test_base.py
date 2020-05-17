from pywisc.wisc import Wisc


def test_01():
    w = Wisc(wisc_version=4, language='es', country='ar')
    assert w.is_valid