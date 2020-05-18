# -*- coding: utf-8 -*-
"""
test_compound3d
~~~~~~~~~~~~~~~

Test compound object with 3D record.

"""


import pytest
import warnings
from decimal import Decimal

from chemistry_tools.pubchem.compound import Compound
from chemistry_tools.constants import text_types
from chemistry_tools.pubchem.errors import PubChemPyDeprecationWarning


@pytest.fixture
def c3d():
    """Compound CID 1234, 3D."""
    return Compound.from_cid(1234, record_type='3d')


def test_properties_types(c3d):
    assert isinstance(c3d.volume_3d, Decimal)
    assert isinstance(c3d.multipoles_3d, list)
    assert isinstance(c3d.conformer_rmsd_3d, Decimal)
    assert isinstance(c3d.effective_rotor_count_3d, Decimal)
    assert isinstance(c3d.pharmacophore_features_3d, list)
    assert isinstance(c3d.mmff94_partial_charges_3d, list)
    assert isinstance(c3d.mmff94_energy_3d, Decimal)
    assert isinstance(c3d.conformer_id_3d, text_types)
    assert isinstance(c3d.shape_selfoverlap_3d, Decimal)
    assert isinstance(c3d.feature_selfoverlap_3d, Decimal)
    assert isinstance(c3d.shape_fingerprint_3d, list)

def test_properties_values(c3d):
    assert c3d.volume_3d == Decimal('393.6')
    assert c3d.multipoles_3d == [680.97, 15.07, 5.63, 2.25, 19.23, 0.35, 0.31, 2.55, 1.87, 0.73, -0.08, -2.81, -1.92, 0.5]
    assert c3d.conformer_rmsd_3d == Decimal('1.2')
    assert c3d.effective_rotor_count_3d == Decimal("14")
    assert c3d.pharmacophore_features_3d == ['11', '1 1 acceptor', '1 2 acceptor', '1 3 acceptor', '1 4 acceptor', '1 5 acceptor', '1 6 cation', '1 7 acceptor', '3 9 14 15 hydrophobe', '4 8 9 10 11 hydrophobe', '6 12 17 18 20 21 23 rings', '6 25 26 27 30 32 33 rings']
    assert c3d.mmff94_partial_charges_3d == ['35', '1 -0.36', '12 -0.14', '13 0.27', '16 0.36', '17 -0.15', '18 -0.15', '19 0.27', '2 -0.36', '20 0.08', '21 0.08', '22 0.27', '23 0.08', '24 0.14', '25 -0.14', '26 -0.15', '27 -0.15', '28 0.28', '29 0.28', '3 -0.36', '30 0.08', '31 0.28', '32 -0.15', '33 0.08', '34 0.28', '35 0.28', '4 -0.36', '49 0.15', '5 -0.36', '50 0.15', '58 0.15', '59 0.15', '6 -0.81', '66 0.15', '7 -0.56', '8 0.34']
    assert c3d.mmff94_energy_3d == Decimal('141.9237')
    assert c3d.conformer_id_3d == '000004D200000003'
    assert c3d.shape_selfoverlap_3d == Decimal('1399.076')
    assert c3d.feature_selfoverlap_3d == Decimal('55.858')
    assert c3d.shape_fingerprint_3d == ['10305334 12 17916319242175899273', '10670039 82 18409168779949569190', '11607047 403 16557086463235076097', '1361 2 18337665433691375065', '13627167 48 18334584572831345236', '14068700 675 18272646879130395169', '14279260 333 17559683820334930998', '14394314 77 18410293640316207093', '14840074 17 18114181968673220895', '15001296 14 18042680783823176596', '15183329 4 18343869901331531294', '15575132 122 18186792574094520567', '17809404 112 16443636700853603859', '17899979 19 18261391204461465599', '19611394 137 17970358220374054379', '469060 322 17603596230791808065', '497634 4 18341614784874425348', '50150288 127 17059789788691365057', '50677037 204 18198061585254069968', '6371009 1 18340472392857636514']


def test_coordinate_type(c3d):
    assert c3d.coordinate_type == '3d'


def test_atoms(c3d):
    assert len(c3d.atoms) == 75
    assert set(a.element for a in c3d.atoms) == {'C', 'H', 'O', 'N'}
    assert set(c3d.elements) == {'C', 'H', 'O', 'N'}


def test_atoms_deprecated(c3d):
    with warnings.catch_warnings(record=True) as w:
        assert set(a['element'] for a in c3d.atoms) == {'C', 'H', 'O', 'N'}
        assert len(w) == 1
        assert w[0].category == PubChemPyDeprecationWarning
        assert str(w[0].message) == 'Dictionary style access to Atom attributes is deprecated'


def test_coordinates(c3d):
    for a in c3d.atoms:
        assert isinstance(a.x, (float, int))
        assert isinstance(a.y, (float, int))
        assert isinstance(a.z, (float, int))


def test_coordinates_deprecated(c3d):
    with warnings.catch_warnings(record=True) as w:
        assert isinstance(c3d.atoms[0]['x'], (float, int))
        assert isinstance(c3d.atoms[0]['y'], (float, int))
        assert isinstance(c3d.atoms[0]['z'], (float, int))
        assert len(w) == 3
        assert w[0].category == PubChemPyDeprecationWarning
        assert str(w[0].message) == 'Dictionary style access to Atom attributes is deprecated'
