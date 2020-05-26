# -*- coding: utf-8 -*-
"""
test_pandas
~~~~~~~~~~~

Test optional pandas functionality.

"""


# 3rd party
import pytest
pandas = pytest.importorskip('pandas')

# this package
from chemistry_tools.pubchem.compound import compounds_to_frame, Compound
from chemistry_tools.pubchem.lookup import get_compounds
from chemistry_tools.pubchem.properties import get_properties


@pytest.mark.skip("TODO")
@pytest.mark.flaky(reruns=5, reruns_delay=10)
def test_compounds_dataframe():
	df = get_compounds('C20H41Br', 'formula', as_dataframe=True)
	assert df.ndim == 2
	assert df.index.names == ['CID']
	assert len(df.index) > 5
	columns = df.columns.values.tolist()
	assert 'atom_stereo_count' in columns
	assert 'atoms' in columns
	assert 'canonical_smiles' in columns
	assert 'exact_mass' in columns


def test_properties_dataframe():
	df = get_properties('1,2,3,4', ['IsomericSMILES', 'XLogP', 'InChIKey'], 'cid', as_dataframe=True)
	assert df.ndim == 2
	assert df.index.names == ['CID']
	assert len(df.index) == 4
	assert df.columns.values.tolist() == ['IsomericSMILES', 'InChIKey', 'XLogP']


def test_compound_series():
	s = Compound.from_cid(241).to_series()
	assert isinstance(s, pandas.Series)


def test_compound_to_frame():
	s = compounds_to_frame(Compound.from_cid(241))
	assert isinstance(s, pandas.DataFrame)
