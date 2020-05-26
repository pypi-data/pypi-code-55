#!/usr/bin/env python3
#
#  description.py
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
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


# this package
from chemistry_tools.pubchem.enums import PubChemNamespace
from chemistry_tools.pubchem.properties import rest_get_properties_json
from chemistry_tools.pubchem.pug_rest import _do_rest_get


def get_iupac_name(name):
	"""
	Returns the systematic IUPAC name for the compound with the given name

	:param name:
	:type name:

	:return:
	:rtype:
	"""

	data = rest_get_properties_json(name, "name", properties="IUPACName")
	iupac_name = data["PropertyTable"]["Properties"][0]["IUPACName"]
	return str(iupac_name)


def get_description(name):
	"""
	Returns the description compound with the given name

	:param name:
	:type name:

	:return:
	:rtype: str
	"""

	data = rest_get_description(name, "name")
	parsed_data = parse_description(data)
	return parsed_data[0]["Description"]


def get_common_name(name):
	"""
	Returns the common name for the compound with the given name

	:param name:
	:type name:

	:return:
	:rtype: str
	"""

	data = rest_get_description(name, "name")
	parsed_data = parse_description(data)
	return parsed_data[0]["Title"]


def get_compound_id(name):
	"""
	Returns the compound ID (CID) for the compound with the given name

	:param name:
	:type name:

	:return:
	:rtype: str
	"""

	data = rest_get_description(name, "name")
	parsed_data = parse_description(data)
	return parsed_data[0]["CID"]


def rest_get_description(identifier, namespace=PubChemNamespace.name, **kwargs):
	"""
	:param identifier: Identifiers (e.g. name, CID) for the compound to look up.
		When using the CID namespace data for multiple compounds can be retrieved at once by
		supplying either a comma-separated string or a list.
	:type identifier: str, Sequence[str]
	:param namespace: The type of identifier to look up. Valid values are in :class:`PubChemNamespace`
	:type namespace: PubChemNamespace, optional
	:param **kwargs: Optional arguments that ``json.loads`` takes.
	:raises ValueError: If the response body does not contain valid json.

	:return: Parsed json data
	:rtype: dict
	"""

	return _do_rest_get(namespace, identifier, domain="description").json(**kwargs)


def parse_description(description_data):
	"""
	Parse raw data from the ``description`` endpoint of the REST API

	:param description_data:
	:type description_data: dict

	:return: A list of dictionaries containing the CID, Title and Description for each compound
	:rtype: list[dict]
	"""

	compounds = {}
	fields = {"Title", "Description"}

	for entry in description_data["InformationList"]["Information"]:

		cid = entry["CID"]

		if cid not in compounds:
			compounds[cid] = {var: None for var in fields}
			compounds[cid]["CID"] = cid

		for var in fields:
			if var in entry:
				compounds[cid][var] = entry[var]

	return list(compounds.values())
