# -*- coding: utf-8 -*-
"""
test_Errors
~~~~~~~~~~~~~

Test Errors.

"""


import pytest

from chemistry_tools.pubchem.compound import Compound
from chemistry_tools.lookup import get_compounds, get_substances
from chemistry_tools.pubchem.substance import Substance
from chemistry_tools.pubchem.errors import BadRequestError, NotFoundError


def test_invalid_identifier():
    """BadRequestError should be raised if identifier is not a positive integer."""
    with pytest.raises(BadRequestError):
        Compound.from_cid('aergaerhg')
    with pytest.raises(BadRequestError):
        get_compounds('srthrthsr')
    with pytest.raises(BadRequestError):
        get_substances('grgrqjksa')


def test_notfound_identifier():
    """NotFoundError should be raised if identifier is a positive integer but record doesn't exist."""
    with pytest.raises(NotFoundError):
        Compound.from_cid(999999999)
    with pytest.raises(NotFoundError):
        Substance.from_sid(999999999)


def test_notfound_search():
    """No error should be raised if a search returns no results."""
    get_compounds(999999999)
    get_substances(999999999)
