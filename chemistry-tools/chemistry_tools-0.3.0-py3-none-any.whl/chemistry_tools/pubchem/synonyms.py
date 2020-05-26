#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  synonyms.py
#
#  Copyright (c) 2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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


# this package
from chemistry_tools.pubchem.enums import PubChemNamespace
from chemistry_tools.pubchem.pug_rest import _do_rest_get


class Synonyms(list):
	def __init__(self, initlist):
		super().__init__()

		for val in initlist:
			self.append(str(val))

	def __contains__(self, value):
		for v in self:
			if self.__prep_contains(v) == self.__prep_contains(value):
				return True
		return False

	def append(self, item):
		if item not in self:
			super().append(str(item))

	@staticmethod
	def __prep_contains(val):
		val = val.casefold()

		for remove in ["-", "_", " "]:
			val = val.replace(remove, " ")

		return val


def get_synonyms(identifier, namespace="name"):
	"""
	Returns a list of synonyms for the compound with the given identifier.
	As more than one compound may be identified the results are returned in a list.

	:param identifier: Identifiers (e.g. name, CID) for the compound to look up.
		When using the CID namespace data for multiple compounds can be retrieved at once by
		supplying either a comma-separated string or a list.
	:type identifier: str, Sequence[str]
	:param namespace: The type of identifier to look up. Valid values are in :class:`PubChemNamespace`. Default "name"
	:type namespace: PubChemNamespace, optional

	:return: List of dictionaries containing the CID and a list of synonyms for the compounds
	:rtype: List[dict]
	"""

	data = rest_get_synonyms(identifier, namespace)

	results = []

	for compound in data["InformationList"]["Information"]:
		parsed_data = {
				"CID": compound["CID"],
				"synonyms": Synonyms(compound["Synonym"][:20]),
				}

		results.append(parsed_data)

	return results


def rest_get_synonyms(identifier, namespace=PubChemNamespace.name, **kwargs):
	"""
	Get the list of synonyms for the given compound

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

	return _do_rest_get(namespace, identifier, domain="synonyms").json(**kwargs)
