# -*- coding: utf-8 -*-
"""
test_Compound
~~~~~~~~~~~~~

Test compound object.

"""

# stdlib
import re
from decimal import Decimal

# 3rd party
import pytest

# this package
from chemistry_tools.pubchem.lookup import get_compounds
from chemistry_tools.pubchem.atom import Atom
from chemistry_tools.pubchem.bond import BondType
from chemistry_tools.pubchem.compound import Compound


@pytest.fixture(scope='module')
def c1():
	"""Compound CID 241."""
	return Compound.from_cid(241)


@pytest.fixture(scope='module')
def c2():
	"""Compound CID 175."""
	return Compound.from_cid(175)


def test_basic(c1):
	"""Test Compound is retrieved and has a record and correct CID."""
	assert c1.cid == 241
	assert repr(c1) == 'Compound(241)'


def test_atoms(c1):
	assert len(c1.atoms) == 12
	print([a.element for a in c1.atoms])
	assert set(a.element for a in c1.atoms) == {'C', 'H'}
	assert set(c1.elements) == {'C', 'H'}


def test_single_atom():
	"""Test Compound when there is a single atom and no bonds."""
	c = Compound.from_cid(259)
	assert c.atoms == [Atom(aid=1, number=35, x=2, y=0, charge=-1)]
	assert c.bonds == []


def test_bonds(c1):
	assert len(c1.bonds) == 12
	assert set(int(b.order) for b in c1.bonds) == {int(BondType.SINGLE), int(BondType.DOUBLE)}


def test_charge(c1):
	assert c1.get_property("Charge") == 0


def test_coordinates(c1):
	for a in c1.atoms:
		assert isinstance(a.x, (float, int))
		assert isinstance(a.y, (float, int))
		assert a.z is None


def test_identifiers(c1):
	# precache properties
	c1.precache()

	assert len(c1.canonical_smiles) > 10
	assert len(c1.get_property("IsomericSMILES")) > 10
	assert c1.smiles == "C1=CC=CC=C1"
	assert c1.get_property("InChI").startswith('InChI=')
	assert re.match(r'^[A-Z]{14}-[A-Z]{10}-[A-Z\d]$', c1.get_property("InChIKey"))
	from chemistry_tools.formulae import Formula
	assert isinstance(c1.get_property("MolecularFormula"), Formula)
	assert isinstance(c1.molecular_formula, Formula)
	assert c1.get_property("MolecularFormula").hill_formula == "C6H6"
	assert c1.molecular_formula.hill_formula == "C6H6"


def test_properties_types(c1):
	# precache properties
	c1.precache()

	assert isinstance(c1.molecular_mass, float)
	assert isinstance(c1.molecular_weight, float)
	assert isinstance(c1.get_property("MolecularWeight"), float)
	assert isinstance(c1.iupac_name, str)
	assert isinstance(c1.systematic_name, str)
	assert isinstance(c1.get_property("XLogP"), float)
	assert isinstance(c1.get_property("ExactMass"), float)
	assert isinstance(c1.get_property("MonoisotopicMass"), float)
	assert isinstance(c1.get_property("TPSA"), (int, float))
	assert isinstance(c1.get_property("Complexity"), float)
	assert isinstance(c1.get_property("HBondDonorCount"), int)
	assert isinstance(c1.get_property("HBondAcceptorCount"), int)
	assert isinstance(c1.get_property("RotatableBondCount"), int)
	assert isinstance(c1.get_property("HeavyAtomCount"), int)
	assert isinstance(c1.get_property("IsotopeAtomCount"), int)
	assert isinstance(c1.get_property("AtomStereoCount"), int)
	assert isinstance(c1.get_property("DefinedAtomStereoCount"), int)
	assert isinstance(c1.get_property("UndefinedAtomStereoCount"), int)
	assert isinstance(c1.get_property("BondStereoCount"), int)
	assert isinstance(c1.get_property("DefinedBondStereoCount"), int)
	assert isinstance(c1.get_property("UndefinedBondStereoCount"), int)
	assert isinstance(c1.get_property("CovalentUnitCount"), int)
	assert isinstance(c1.fingerprint, str)
	# TODO:assert isinstance(c1.hill_formula, text_types)
	assert isinstance(c1.canonicalized, bool) # TODO


def test_properties_values(c1):
	# precache properties
	c1.precache()

	assert c1.molecular_mass == 78.11
	assert c1.molecular_weight == 78.11
	assert c1.molecular_mass == c1.molecular_weight
	assert c1.iupac_name == "benzene"
	assert c1.systematic_name == "benzene"
	assert c1.get_property("XLogP") == 2.1
	assert c1.get_property("ExactMass") == 78.04695
	assert c1.get_property("MonoisotopicMass") == 78.04695
	assert c1.get_property("TPSA") == Decimal(0)
	# assert c1.get_property("Complexity") == 15.5  # TODO: full record has 15.5 but getting just property gives 15
	assert c1.get_property("HBondDonorCount") == Decimal("0")
	assert c1.get_property("HBondAcceptorCount") == Decimal("0")
	assert c1.get_property("RotatableBondCount") == Decimal("0")
	assert c1.get_property("HeavyAtomCount") == Decimal("6")
	assert c1.get_property("IsotopeAtomCount") == Decimal("0")
	assert c1.get_property("AtomStereoCount") == 0
	assert c1.get_property("DefinedAtomStereoCount") == Decimal("0")
	assert c1.get_property("UndefinedAtomStereoCount") == Decimal("0")
	assert c1.get_property("BondStereoCount") == 0
	assert c1.get_property("DefinedBondStereoCount") == Decimal("0")
	assert c1.get_property("UndefinedBondStereoCount") == Decimal("0")
	assert c1.get_property("CovalentUnitCount") == Decimal("1")
	# TODO:assert c1.hill_formula == 'C<sub>6</sub>H<sub>6</sub>'
	assert c1.canonicalized is True


def test_coordinate_type(c1):
	assert c1.coordinate_type == '2d'


def test_compound_equality():
	assert Compound.from_cid(241) == Compound.from_cid(241)
	assert get_compounds('Benzene', 'name')[0], get_compounds('c1ccccc1' == 'smiles')[0]


def test_synonyms(c1):
	assert len(c1.synonyms) > 5
	assert len(c1.synonyms) > 5


def test_compound_dict(c1):
	assert dict(c1)
	assert isinstance(dict(c1), dict)
	assert 'atoms' in dict(c1)
	assert 'bonds' in dict(c1)
	assert dict(c1)['atoms'][1].element


def test_charged_compound(c2):
	assert len(c2.atoms) == 7
	assert c2.atoms[0].charge == -1


def test_fingerprint(c1):
	# CACTVS fingerprint is 881 bits
	assert len(c1.cactvs_fingerprint) == 881
	# Raw fingerprint has 4 byte prefix, 7 bit suffix, and is hex encoded (/4) = 230
	assert len(c1.fingerprint) == (881 + (4 * 8) + 7) / 4

# TODO: Compound.to_series, compounds_to_frame()
