# -*- coding: utf-8 -*-
"""
test_Atom
~~~~~~~~~~~~~

Test Atom class

"""

import pytest

from chemistry_tools.pubchem.atom import Atom


@pytest.fixture(scope='module')
def a1():
	return Atom(1234, 6, 7, 8, charge=-1)


def test_atom(a1):
	assert a1.__repr__() == "Atom(1234, C)"
	assert a1.element == "C"
	assert isinstance(a1.element, str)
	assert isinstance(a1.to_dict(), dict)
	assert a1.to_dict()["number"] == 6
	assert a1.aid == 1234
	assert a1.x == 7
	assert a1.y == 8
	assert a1.z is None


def test_coordinates(a1):
	a1.set_coordinates(7, 8, 9)
	assert a1.coordinate_type == "3d"

	a1.set_coordinates(7, 8)
	assert a1.coordinate_type == "2d"
