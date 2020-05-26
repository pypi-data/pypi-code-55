# -*- coding: utf-8 -*-
"""
test_compound3d
~~~~~~~~~~~~~~~

Test compound object with 3D record.

"""

# 3rd party
import pytest

# this package
from chemistry_tools.pubchem.compound import Compound


@pytest.fixture
def c3d():
	"""Compound CID 1234, 3D."""
	return Compound.from_cid(1234, record_type='3d')


def test_coordinate_type(c3d):
	assert c3d.coordinate_type == '3d'


def test_atoms(c3d):
	assert len(c3d.atoms) == 75
	assert set(a.element for a in c3d.atoms) == {'C', 'H', 'O', 'N'}
	assert set(c3d.elements) == {'C', 'H', 'O', 'N'}


def test_coordinates(c3d):
	for a in c3d.atoms:
		assert isinstance(a.x, (float, int))
		assert isinstance(a.y, (float, int))
		print(a.z)
		assert isinstance(a.z, (float, int))

