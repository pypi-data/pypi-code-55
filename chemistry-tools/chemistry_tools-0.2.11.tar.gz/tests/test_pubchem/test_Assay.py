# -*- coding: utf-8 -*-
"""
test_Assay
~~~~~~~~~~

Test Assay object.

"""


import pytest

from chemistry_tools.constants import ProjectCategory, text_types
from chemistry_tools.pubchem.assay import Assay
from chemistry_tools.lookup import get_assays


@pytest.fixture(scope='module')
def a1():
    """Assay AID 10000."""
    return Assay.from_aid(10000)


def test_basic(a1):
    assert a1.aid == 10000
    assert repr(a1) == 'Assay(10000)'
    assert a1.record


def test_meta(a1):
    assert isinstance(a1.name, text_types)
    assert a1.name == "In vitro inhibition of human ovarian cell line A2780"
    assert a1.project_category == ProjectCategory.LITERATURE_EXTRACTED
    assert isinstance(a1.description, list)
    assert isinstance(a1.comments, list)
    assert isinstance(a1.results, list)
    assert isinstance(a1.results[0], dict)
    assert isinstance(a1.target, list)
    assert isinstance(a1.target[0], dict)
    assert isinstance(a1.revision, int)
    assert isinstance(a1.aid_version, int)
    assert a1.aid_version == 7


def test_assay_equality():
    first = Assay.from_aid(10000)
    second = Assay.from_aid(1000)
    assert first == first
    assert second == second
    assert first != second

def test_get_assays():
    first = Assay.from_aid(10000)
    second = get_assays(10000)[0]
    assert first == second


def test_assay_dict(a1):
    assert isinstance(a1.to_dict(), dict)
    assert a1.to_dict()
