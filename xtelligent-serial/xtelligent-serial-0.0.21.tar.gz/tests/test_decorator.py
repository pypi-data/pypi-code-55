from xtelligent_serial import (to_serializable, from_serializable)

from .fixtures import Boo, Yah, NoneAble

def test_decorator1():
    d = to_serializable(Boo(2))
    assert d['y'] == 4
    b = from_serializable(Boo, d)
    assert b.root == 2

def test_decorator2():
    yah = Yah(3)
    d = to_serializable(yah)
    assert isinstance(d, dict)
    y2 = from_serializable(Yah, d)
    assert yah.root == y2.root

def test_noneable():
    n1 = NoneAble(None)
    d = to_serializable(n1)
    assert d == {'x': None}
    n2 = from_serializable(NoneAble, d)
    assert n2.x is None
