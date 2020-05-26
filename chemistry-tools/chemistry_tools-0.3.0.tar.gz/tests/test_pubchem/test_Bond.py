# -*- coding: utf-8 -*-
"""
test_Bond
~~~~~~~~~~~~~

Test Bond class

"""

import pytest

from chemistry_tools.pubchem.bond import Bond, BondType


@pytest.fixture(scope='module')
def b1():
	return Bond(1, 2, order=BondType.QUADRUPLE)


def test_bond(b1):
	assert b1.__repr__() == "Bond(1, 2, BondType.QUADRUPLE)"
	assert isinstance(b1.to_dict(), dict)
	assert b1.to_dict()["order"] == BondType.QUADRUPLE
