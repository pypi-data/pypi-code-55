#  !/usr/bin/env python
#
#  assay.py
#
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

# stdlib
import json

# this package
from .utils import request


class Assay:

	@classmethod
	def from_aid(cls, aid):
		"""
		Retrieve the Assay record for the specified AID.

		:param int aid: The PubChem Assay Identifier (AID).
		"""

		record = json.loads(request(aid, 'aid', 'assay', 'description').content.decode())['PC_AssayContainer'][0]
		return cls(record)

	def __init__(self, record):
		"""
		:param record: A dictionary containing the full Assay record that all other properties are obtained from.
		:type record: dict
		"""
		self.record = record

	def __repr__(self):
		return 'Assay(%s)' % self.aid if self.aid else 'Assay()'

	def __eq__(self, other):
		return isinstance(other, type(self)) and self.record == other.record

	def to_dict(self, properties=None):
		"""
		Return a dictionary containing Assay data.

		If the properties parameter is not specified, everything is included.

		:param properties: (optional) A list of the desired properties.
		"""

		if not properties:
			properties = [p for p in dir(Assay) if isinstance(getattr(Assay, p), property)]
		return {p: getattr(self, p) for p in properties}

	@property
	def aid(self):
		"""The PubChem Substance Identifier (SID)."""
		return self.record['assay']['descr']['aid']['id']

	@property
	def name(self):
		"""The short assay name, used for display purposes."""
		return self.record['assay']['descr']['name']

	@property
	def description(self):
		"""Description"""
		return self.record['assay']['descr']['description']

	@property
	def project_category(self):
		"""A category to distinguish projects funded through MLSCN, MLPCN or from literature.

		Possible values include mlscn, mlpcn, mlscn-ap, mlpcn-ap, literature-extracted, literature-author,
		literature-publisher, rnaigi.
		"""
		if 'project_category' in self.record['assay']['descr']:
			return self.record['assay']['descr']['project_category']

	@property
	def comments(self):
		"""Comments and additional information."""
		return [comment for comment in self.record['assay']['descr']['comment'] if comment]

	@property
	def results(self):
		"""A list of dictionaries containing details of the results from this Assay."""
		return self.record['assay']['descr']['results']

	@property
	def target(self):
		"""A list of dictionaries containing details of the Assay targets."""
		if 'target' in self.record['assay']['descr']:
			return self.record['assay']['descr']['target']
		else:
			return [{}]

	@property
	def revision(self):
		"""Revision identifier for textual description."""
		return self.record['assay']['descr']['revision']

	@property
	def aid_version(self):
		"""Incremented when the original depositor updates the record."""
		return self.record['assay']['descr']['aid']['version']
