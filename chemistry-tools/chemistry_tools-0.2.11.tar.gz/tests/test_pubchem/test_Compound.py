# -*- coding: utf-8 -*-
"""
test_Compound
~~~~~~~~~~~~~

Test compound object.

"""


import pytest

import re
import warnings
from decimal import Decimal

from chemistry_tools.pubchem.compound import Compound
from chemistry_tools.pubchem.atom import Atom
from chemistry_tools.pubchem.bond import BondType
from chemistry_tools.pubchem.errors import PubChemPyDeprecationWarning
from chemistry_tools.constants import text_types
from chemistry_tools.lookup import get_compounds


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
    assert c1.record


def test_atoms(c1):
    assert len(c1.atoms) == 12
    assert set(a.element for a in c1.atoms) == {'C', 'H'}
    assert set(c1.elements) == {'C', 'H'}


def test_atoms_deprecated(c1):
    with warnings.catch_warnings(record=True) as w:
        assert set(a['element'] for a in c1.atoms) == {'C', 'H'}
        assert len(w) == 1
        assert w[0].category == PubChemPyDeprecationWarning
        assert str(w[0].message) == 'Dictionary style access to Atom attributes is deprecated'


def test_single_atom():
    """Test Compound when there is a single atom and no bonds."""
    c = Compound.from_cid(259)
    assert c.atoms == [Atom(aid=1, number=35, x=2, y=0, charge=-1)]
    assert c.bonds == []


def test_bonds(c1):
    assert len(c1.bonds) == 12
    assert set(b.order for b in c1.bonds) == {BondType.SINGLE, BondType.DOUBLE}


def test_bonds_deprecated(c1):
    with warnings.catch_warnings(record=True) as w:
        assert set(b['order'] for b in c1.bonds) == {BondType.SINGLE, BondType.DOUBLE}
        assert len(w) == 1
        assert w[0].category == PubChemPyDeprecationWarning
        assert str(w[0].message) == 'Dictionary style access to Bond attributes is deprecated'


def test_charge(c1):
    assert c1.charge == 0


def test_coordinates(c1):
    for a in c1.atoms:
        assert isinstance(a.x, (float, int))
        assert isinstance(a.y, (float, int))
        assert a.z is None


def test_coordinates_deprecated(c1):
    with warnings.catch_warnings(record=True) as w:
        assert isinstance(c1.atoms[0]['x'], (float, int))
        assert isinstance(c1.atoms[0]['y'], (float, int))
        assert 'z' not in c1.atoms[0]
        assert len(w) == 3
        assert w[0].category == PubChemPyDeprecationWarning
        assert str(w[0].message) == 'Dictionary style access to Atom attributes is deprecated'


def test_identifiers(c1):
    assert len(c1.canonical_smiles) > 10
    assert len(c1.isomeric_smiles) > 10
    assert c1.smiles == "C1=CC=CC=C1"
    assert c1.inchi.startswith('InChI=')
    assert re.match(r'^[A-Z]{14}-[A-Z]{10}-[A-Z\d]$', c1.inchikey)
    assert isinstance(c1.molecular_formula, str)
    assert c1.molecular_formula == "C6H6"


def test_properties_types(c1):
    assert isinstance(c1.molecular_mass, Decimal)
    assert isinstance(c1.molecular_weight, Decimal)
    assert isinstance(c1.iupac_name, text_types)
    assert isinstance(c1.systematic_name, text_types)
    assert isinstance(c1.xlogp, Decimal)
    assert isinstance(c1.exact_mass, Decimal)
    assert isinstance(c1.monoisotopic_mass, Decimal)
    assert isinstance(c1.tpsa, (int, Decimal))
    assert isinstance(c1.complexity, Decimal)
    assert isinstance(c1.h_bond_donor_count, Decimal)
    assert isinstance(c1.h_bond_acceptor_count, Decimal)
    assert isinstance(c1.rotatable_bond_count, Decimal)
    assert isinstance(c1.heavy_atom_count, Decimal)
    assert isinstance(c1.isotope_atom_count, Decimal)
    assert isinstance(c1.atom_stereo_count, int)
    assert isinstance(c1.defined_atom_stereo_count, Decimal)
    assert isinstance(c1.undefined_atom_stereo_count, Decimal)
    assert isinstance(c1.bond_stereo_count, int)
    assert isinstance(c1.defined_bond_stereo_count, Decimal)
    assert isinstance(c1.undefined_bond_stereo_count, Decimal)
    assert isinstance(c1.covalent_unit_count, Decimal)
    assert isinstance(c1.fingerprint, text_types)
    assert isinstance(c1.hill_formula, text_types)
    assert isinstance(c1.is_canonicalized, bool)
    # assert isinstance(c1.boiling_point, Decimal)
    # TODO: Boiling point now returns string
    assert c1.boiling_point == '80.11111111111111111111111112°C at 760 mm Hg (NTP, 1992)'
    assert isinstance(c1.color, str)
    assert isinstance(c1.density, str)
    assert isinstance(c1.specific_gravity, str)
    # assert isinstance(c1.dissociation_constant, )
    # TODO
    assert isinstance(c1.heat_combustion, str)
    # assert isinstance(c1.melting_point, Decimal)
    assert c1.melting_point == '5.5°C (NTP, 1992)'
    # TODO: melting point now returns string

    assert isinstance(c1.partition_coeff, str)
    assert isinstance(c1.odor, str)
    assert isinstance(c1.other_props, str)
    assert isinstance(c1.solubility, str)
    assert isinstance(c1.spectral_props, str)
    assert isinstance(c1.surface_tension, str)
    assert isinstance(c1.vapor_density, str)
    assert isinstance(c1.vapor_pressure, str)
    assert isinstance(c1.full_record, dict)


def test_properties_values(c1):
    assert c1.molecular_mass == Decimal('78.11')
    assert c1.molecular_weight == Decimal('78.11')
    assert c1.molecular_mass == c1.molecular_weight
    assert c1.iupac_name == "benzene"
    assert c1.systematic_name == "benzene"
    assert c1.xlogp == Decimal("2.1")
    assert c1.exact_mass == Decimal('78.04695')
    assert c1.monoisotopic_mass == Decimal('78.04695')
    assert c1.tpsa == Decimal(0)
    assert c1.complexity == Decimal("15.5")
    assert c1.h_bond_donor_count == Decimal("0")
    assert c1.h_bond_acceptor_count == Decimal("0")
    assert c1.rotatable_bond_count == Decimal("0")
    assert c1.heavy_atom_count == Decimal("6")
    assert c1.isotope_atom_count == Decimal("0")
    assert c1.atom_stereo_count == 0
    assert c1.defined_atom_stereo_count == Decimal("0")
    assert c1.undefined_atom_stereo_count == Decimal("0")
    assert c1.bond_stereo_count == 0
    assert c1.defined_bond_stereo_count == Decimal("0")
    assert c1.undefined_bond_stereo_count == Decimal("0")
    assert c1.covalent_unit_count == Decimal("1")
    assert c1.hill_formula == 'C<sub>6</sub>H<sub>6</sub>'
    assert c1.is_canonicalized is True
    # TODO: Now seems to return formatted string
    # assert c1.boiling_point == Decimal('80.08')
    assert c1.boiling_point == "80.11111111111111111111111112°C at 760 mm Hg (NTP, 1992)"
    assert c1.color == 'Clear, colorless liquid'
    assert c1.density == '0.879 at 20°C'
    assert c1.specific_gravity == '0.879 at 20°C'
    # TODO: What happened to the units (g/cu cm) for density and specific gravity?
    # assert c1.dissociation_constant ==
    # TODO
    assert c1.heat_combustion == '-3267.6 kJ/mol (liquid)'
    # assert c1.melting_point == Decimal('5.558')
    assert c1.melting_point == "5.5°C (NTP, 1992)"
    # assert c1.partition_coeff == 'log Kow = 2.13'
    assert c1.partition_coeff == '2.13 (LogP)'
    assert c1.odor == 'Aromatic odor'
    assert c1.other_props == 'Conversion factors: 1 mg/cu m = 0.31 ppm; 1 ppm = 3.26 mg/cu m'
    # assert c1.solubility == 'In water, 1.79×10<sup>+3</sup> mg/L at 25°C'
    # assert c1.spectral_props == 'MAX ABSORPTION (ALCOHOL): 243 NM (LOG E = 2.2), 249 NM (LOG E = 2.3), 256 NM (LOG E = 2.4), 261 NM (LOG E = 2.2); SADTLER REF NUMBER: 6402 (IR, PRISM), 1765 (UV)'
    assert c1.surface_tension == '28.22 mN/m at 25 °C'
    # assert c1.vapor_density == '2.8 (Air = 1)'
    # assert c1.vapor_pressure == '94.8 mm Hg at 25 °C'
    # TODO: Sort out solubility, spectral_props, vapor_density, vapor_pressure


def test_get_property(c1):
    assert isinstance(c1.get_property("Melting Point"), dict)
    # TODO: Record for Benzene now seems to return a string with markup, not a number
    # assert isinstance(c1.get_property_value("Melting Point"), Decimal)
    # assert c1.get_property_value("Melting Point") == Decimal('5.558')
    assert isinstance(c1.get_property_value("Melting Point"), str)
    assert c1.get_property_value("Melting Point") == "5.5°C (NTP, 1992)"
    assert c1.melting_point == c1.get_property_value("Melting Point")
    assert isinstance(c1.get_property_description("Melting Point"), str)
    # assert c1.get_property_description("Melting Point") is None
    # assert isinstance(c1.get_property_unit("Melting Point"), str)
    assert c1.get_property_unit("Melting Point") is None

    assert isinstance(c1.get_property("Boiling Point"), dict)
    assert isinstance(c1.get_property("Heat Combustion"), dict)
    assert isinstance(c1.get_property("Exact Mass"), dict)


def test_coordinate_type(c1):
    assert c1.coordinate_type == '2d'


def test_compound_equality():
    assert Compound.from_cid(241) == Compound.from_cid(241)
    assert get_compounds('Benzene', 'name')[0], get_compounds('c1ccccc1' == 'smiles')[0]


def test_synonyms(c1):
    assert len(c1.synonyms) > 5
    assert len(c1.synonyms) > 5


def test_related_records(c1):
    assert len(c1.sids) > 20
    assert len(c1.aids) > 20


def test_compound_dict(c1):
    assert isinstance(c1.to_dict(), dict)
    assert c1.to_dict()
    assert 'atoms' in c1.to_dict()
    assert 'bonds' in c1.to_dict()
    assert 'element' in c1.to_dict()['atoms'][0]


def test_charged_compound(c2):
    assert len(c2.atoms) == 7
    assert c2.atoms[0].charge == -1


def test_charged_compound_deprecated(c2):
    with warnings.catch_warnings(record=True) as w:
        assert c2.atoms[0]['charge'] == -1
        assert len(w) == 1
        assert w[0].category == PubChemPyDeprecationWarning
        assert str(w[0].message) == 'Dictionary style access to Atom attributes is deprecated'


def test_fingerprint(c1):
    # CACTVS fingerprint is 881 bits
    assert len(c1.cactvs_fingerprint) == 881
    # Raw fingerprint has 4 byte prefix, 7 bit suffix, and is hex encoded (/4) = 230
    assert len(c1.fingerprint) == (881 + (4 * 8) + 7) / 4

# TODO: Compound.to_series, compounds_to_frame()
