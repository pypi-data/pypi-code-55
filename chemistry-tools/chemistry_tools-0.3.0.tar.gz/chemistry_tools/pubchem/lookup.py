#  !/usr/bin/env python
#
#  lookup.py
"""
Lookup properties for compound by name or CAS number
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


from chemistry_tools.pubchem.compound import Compound
from chemistry_tools.pubchem.description import parse_description, rest_get_description


# TODO: xrefs
# TODO: formula search with listkey and pagination 	https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest$_Toc494865589


def get_compounds(identifier, namespace="name"):
	"""
	Returns a list of Compound objects for compounds that match the search criteria
	As more than one compound may be identified the results are returned in a list.

	:param identifier: Identifiers (e.g. name, CID) for the compound to look up.
		When using the CID namespace data for multiple compounds can be retrieved at once by
		supplying either a comma-separated string or a list.
	:type identifier: str, Sequence[str]
	:param namespace: The type of identifier to look up. Valid values are in :class:`PubChemNamespace`. Default "name"
	:type namespace: PubChemNamespace, optional

	:return:
	:rtype:
	"""

	data = rest_get_description(identifier, namespace)

	compounds = []

	for record in parse_description(data):
		compounds.append(Compound(record["Title"], record["CID"], record["Description"]))

	return compounds

