# -*- coding: utf-8 -*-
"""
test_properties
~~~~~~~~~~~~~~~

Test properties requests.

"""


from chemistry_tools.pubchem import utils


def test_properties():
	""""""
	results = utils.get_properties(['IsomericSMILES', 'InChIKey'], 'tris-(1,10-phenanthroline)ruthenium', 'name')
	assert len(results) > 0
	for result in results:
		assert 'CID' in result
		assert 'IsomericSMILES' in result
		assert 'InChIKey' in result


def test_underscore_properties():
	"""Properties can also be specified as underscore-separated words, rather than CamelCase."""
	results = utils.get_properties(['isomeric_smiles', 'molecular_weight'], 'tris-(1,10-phenanthroline)ruthenium', 'name')
	assert len(results) > 0
	for result in results:
		assert 'CID' in result
		assert 'IsomericSMILES' in result
		assert 'MolecularWeight' in result


def test_comma_string_properties():
	"""Properties can also be specified as a comma-separated string, rather than a list."""
	results = utils.get_properties('isomeric_smiles,InChIKey,molecular_weight', 'tris-(1,10-phenanthroline)ruthenium', 'name')
	assert len(results) > 0
	for result in results:
		assert 'CID' in result
		assert 'IsomericSMILES' in result
		assert 'MolecularWeight' in result
		assert 'InChIKey' in result


def test_synonyms():
	results = utils.get_synonyms('C1=CC2=C(C3=C(C=CC=N3)C=C2)N=C1', 'smiles')
	assert len(results) > 0
	for result in results:
		assert 'CID' in result
		assert 'Synonym' in result
		assert isinstance(result['Synonym'], list)
		assert len(result['Synonym']) > 0


stringwithmarkup = {'String': 'N-phenylaniline',
					'Markup': [{'Start': 0, 'Length': 1, 'Type': 'Italics'}]}

def test_format_string():
	html_string = utils.format_string(stringwithmarkup)
	assert isinstance(html_string, str)
	assert html_string == '<i>N</i>-phenylaniline'