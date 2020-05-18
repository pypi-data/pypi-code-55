#  !/usr/bin/env python
#
#  lookup.py
"""
Lookup properties for compound by name or CAS number
Uses data from PubChem and toxnet
"""
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as
#  published by the Free Software Foundation; either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

from chemistry_tools.pubchem.assay import Assay
from chemistry_tools.pubchem.compound import Compound, compounds_to_frame
from chemistry_tools.pubchem.substance import Substance, substances_to_frame
from chemistry_tools.pubchem.utils import get_json


def get_compounds(identifier, namespace='cid', searchtype=None, as_dataframe=False, **kwargs):
	"""
	Retrieve the specified compound records from PubChem.

	:param identifier: The compound identifier to use as a search query.
	:param namespace: (optional) The identifier type, one of cid, name, smiles, sdf, inchi, inchikey or formula.
	:param searchtype: (optional) The advanced search type, one of substructure, superstructure or similarity.
	:param as_dataframe: (optional) Automatically extract the :class:`~pubchempy.Compound` properties into a pandas
						 :class:`~pandas.DataFrame` and return that.
	"""

	results = get_json(identifier, namespace, searchtype=searchtype, **kwargs)
	compounds = [Compound(r) for r in results['PC_Compounds']] if results else []
	if as_dataframe:
		return compounds_to_frame(compounds)
	return compounds


def get_assays(identifier, namespace='aid', **kwargs):
	"""Retrieve the specified assay records from PubChem.

	:param identifier: The assay identifier to use as a search query.
	:param namespace: (optional) The identifier type.
	"""
	results = get_json(identifier, namespace, 'assay', 'description', **kwargs)
	return [Assay(r) for r in results['PC_AssayContainer']] if results else []


def get_substances(identifier, namespace='sid', as_dataframe=False, **kwargs):
	"""Retrieve the specified substance records from PubChem.

	:param identifier: The substance identifier to use as a search query.
	:param namespace: (optional) The identifier type, one of sid, name or sourceid/<source name>.
	:param as_dataframe: (optional) Automatically extract the :class:`~pubchempy.Substance` properties into a pandas
						 :class:`~pandas.DataFrame` and return that.
	"""
	results = get_json(identifier, namespace, 'substance', **kwargs)
	substances = [Substance(r) for r in results['PC_Substances']] if results else []
	if as_dataframe:
		return substances_to_frame(substances)
	return substances
