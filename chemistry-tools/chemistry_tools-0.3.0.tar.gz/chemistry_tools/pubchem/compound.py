#!/usr/bin/env python
#
#  compound.py
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
#  Based on PubChemPy https://github.com/mcs07/PubChemPy/blob/master/LICENSE
#  |  Copyright 2014 Matt Swain <m.swain@me.com>
#  |  Licensed under the MIT License
#  |
#  |  Permission is hereby granted, free of charge, to any person obtaining a copy
#  |  of this software and associated documentation files (the "Software"), to deal
#  |  in the Software without restriction, including without limitation the rights
#  |  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  |  copies of the Software, and to permit persons to whom the Software is
#  |  furnished to do so, subject to the following conditions:
#
#  |  The above copyright notice and this permission notice shall be included in
#  |  all copies or substantial portions of the Software.
#
#  |  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  |  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  |  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  |  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  |  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  |  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  |  THE SOFTWARE.
#

# 3rd party
from domdf_python_tools.bases import Dictable
from memoized_property import memoized_property

# this package
from chemistry_tools.pubchem.atom import parse_atoms
from chemistry_tools.pubchem.bond import parse_bonds
from chemistry_tools.pubchem.enums import CoordinateType
from chemistry_tools.pubchem.full_record import parse_full_record, rest_get_full_record
from chemistry_tools.pubchem.properties import (
	_force_valid_properties, insert_valid_properties_table, parse_properties,
	rest_get_properties_json, valid_properties,
	)
from chemistry_tools.pubchem.synonyms import get_synonyms


class Compound(Dictable):
	"""
	Corresponds to a single record from the PubChem Compound database.

	The PubChem Compound database is constructed from the Substance database
	using a standardization and deduplication process.
	Each Compound is uniquely identified by a CID.
	"""

	def __init__(self, title, CID, description, **_):
		"""
		Initialize with a record dict from the PubChem PUG REST service.
		"""

		super().__init__()

		self.title = str(title)
		self.CID = int(CID)
		self.description = str(description)
		self._properties = {prop: None for prop in valid_properties}
		self.record_type = "2d"
		self._synonyms = None

		# Pre-cache all properties
		# self.get_properties("all")

		self._has_full_record = False

	@property
	def __dict__(self):
		return dict(
				title=self.title,
				CID=self.CID,
				description=self.description,
				properties=self._properties,
				record_type=self.record_type,
				counts=self._record["counts"],
				atoms=self._atoms,
				bonds=self._bonds,
				)

	def __repr__(self):
		return f'Compound({self.cid})' if self.cid else 'Compound()'

	def to_series(self):
		"""
		Return a pandas :class:`~pandas.Series` containing Compound data.
		"""

		import pandas as pd
		return pd.Series(dict(self))

	@property
	def cid(self):
		return self.CID

	@property
	def has_full_record(self):
		return self._has_full_record

	@memoized_property
	def _record(self):

		# Only requested when required
		record = parse_full_record(rest_get_full_record(self.CID, "cid", self.record_type))[0]
		self._has_full_record = True

		for prop in record["properties"]:
			if not self._properties["CanonicalSMILES"]:
				if prop.label == "SMILES" and prop.name == "Canonical":
					self._properties["CanonicalSMILES"] = prop.value

			if not self._properties["IsomericSMILES"]:
				if prop.label == "SMILES" and prop.name == "Isomeric":
					self._properties["IsomericSMILES"] = prop.value

			if not self._properties["TPSA"]:
				if prop.label == "Topological" and prop.name == "Polar Surface Area":
					self._properties["TPSA"] = prop.value

			if not self._properties["InChIKey"]:
				if prop.label == "InChIKey" and prop.name == "Standard":
					self._properties["InChIKey"] = prop.value

			if not self._properties["InChI"]:
				if prop.label == "InChI" and prop.name == "Standard":
					self._properties["InChI"] = prop.value

			if not self._properties["HBondAcceptorCount"]:
				if prop.label == "Count" and prop.name == "Hydrogen Bond Acceptor":
					self._properties["HBondAcceptorCount"] = prop.value

			if not self._properties["HBondDonorCount"]:
				if prop.label == "Count" and prop.name == "Hydrogen Bond Donor":
					self._properties["HBondDonorCount"] = prop.value

			if not self._properties["RotatableBondCount"]:
				if prop.label == "Count" and prop.name == "Rotatable Bond":
					self._properties["RotatableBondCount"] = prop.value

			if not self._properties["MolecularWeight"]:
				if prop.label == "Molecular Weight" and prop.name is None:
					self._properties["MolecularWeight"] = prop.value

			# TODO: label='Weight', name='MonoIsotopic',
				#label='Molecular Formula', name=None,
				#label='Mass', name='Exact',
				# label='Log P', name='XLogP3'
				#
		return record

	@memoized_property
	def _atoms(self):
		"""
		Derive Atom objects from the record.
		"""

		if 'atoms' not in self._record:
			return

		atoms_dict = self._record['atoms']
		coords_dict = self._record.get('coords', None)
		return parse_atoms(atoms_dict, coords_dict)

	@memoized_property
	def _bonds(self):
		"""
		Derive Bond objects from the record.
		"""


		if 'bonds' not in self._record:
			return

		bonds_dict = self._record['bonds']
		coords_dict = self._record.get('coords', None)
		return parse_bonds(bonds_dict, coords_dict)

	def precache(self):
		self.get_properties("all")
		_ = self._atoms
		_ = self._bonds

	@property
	def atoms(self):
		"""
		List of :class:`Atoms <chemistry_tools.pubchem.atom.Atom>`
		in this Compound.
		"""

		return sorted(self._atoms.values(), key=lambda x: x.aid)

	@property
	def bonds(self):
		"""
		List of :class:`Bonds <chemistry_tools.pubchem.bond.Bond>`
		between :class:`Atoms <chemistry_tools.pubchem.atom.Atom>`
		in this Compound.
		"""

		return sorted(self._bonds.values(), key=lambda x: (x.aid1, x.aid2))

	@property
	def coordinate_type(self):
		if CoordinateType.TWO_D in self._record['coords'][0]['type']:
			return '2d'
		elif CoordinateType.THREE_D in self._record['coords'][0]['type']:
			return '3d'

	@property
	def elements(self):
		"""List of element symbols for atoms in this Compound."""
		return [a.element for a in self.atoms]

	@insert_valid_properties_table()
	def get_properties(self, properties):
		"""
		Returns the requested properties for the Compound

		:param properties: The properties to retrieve for the compound. See the table below. Can be either a comma-separated string or a list.

		:: See chemistry_tools.pubchem.properties.valid_property_descriptions for a list of valid properties ::

		:type properties: str, Sequence[str]

		:return:
		:rtype:
		"""

		if isinstance(properties, str) and properties.lower() == "all":
			properties = list(valid_properties.keys())

		properties = _force_valid_properties(properties)

		cached_properties = []
		properties_to_get = []

		for prop in properties:
			if self._properties[prop] is not None:
				cached_properties.append(prop)
			else:
				properties_to_get.append(prop)

		output = {}

		if properties_to_get:
			print("Getting from API")
			data = rest_get_properties_json(self.CID, "cid", properties)
			new_properties = parse_properties(data)[0]

			for prop in properties_to_get:
				self._properties[prop] = new_properties[prop]
				output[prop] = new_properties[prop]

		for prop in cached_properties:
			print("Getting from cache")
			output[prop] = self._properties[prop]

		return output

	@insert_valid_properties_table()
	def get_property(self, prop):
		"""
		Get a single property for the compound

		:param prop: The property to retrieve for the compound. See the table below.

		:: See chemistry_tools.pubchem.properties.valid_property_descriptions for a list of valid properties ::

		:type prop: str

		:return:
		:rtype:
		"""

		prop = str(prop)

		if prop not in self._properties:
			raise ValueError(f"Unknown property '{prop}'")

		if self._properties[prop] is not None:
			print("Getting from cache")
			return self._properties[prop]
		else:
			print("Getting from API")
			data = rest_get_properties_json(self.CID, "cid", prop)
			new_properties = parse_properties(data)[0]

			self._properties[prop] = new_properties[prop]
			return new_properties[prop]

	@property
	def synonyms(self):
		"""
		Returns a list of synonyms for the Compound.

		:rtype: List[str]
		"""

		if not self._synonyms:
			data = get_synonyms(self.CID, "cid")[0]

			if not data["CID"] == self.CID:
				raise ValueError("Wrong compound returned")

			else:
				self._synonyms = data["synonyms"]

		return self._synonyms

	@classmethod
	def from_cid(cls, cid, record_type="2d"):
		"""
		Returns the Compound objects for the compound with the given CID

		:return:
		:rtype:
		"""

		from chemistry_tools.pubchem.lookup import get_compounds

		comp = get_compounds(cid, "cid")[0]

		if comp.CID != int(cid):
			raise ValueError("Wrong compound returned")

		comp.record_type = record_type

		return comp

	# Convenience attributes for some properties

	@property
	def molecular_formula(self):
		"""
		Molecular formula.
		"""

		return self.get_property("MolecularFormula")

	@property
	def canonical_smiles(self):
		"""
		Canonical SMILES, with no stereochemistry information.
		"""

		return self.get_property("CanonicalSMILES")

	smiles = canonical_smiles

	@property
	def charge(self):
		return self.get_property("Charge")


	@property
	def molecular_weight(self):
		"""
		Molecular Weight.
		"""

		return self.get_property("MolecularWeight")

	molecular_mass = molecular_weight

	@memoized_property
	def canonicalized(self):
		for prop in self._record["properties"]:
			if prop.label == "Compound" and prop.name == "Canonicalized":
				return bool(prop.value)

		return False

	def get_iupac_name(self, type_="Systematic"):
		# Allowed, CAS-like Style, Markup, Preferred, Systematic, Traditional
		for prop in self._record["properties"]:
			if prop.label == "IUPAC Name" and prop.name == type_.capitalize():
				return prop.value

		return False

	@memoized_property
	def iupac_name(self):
		return self.get_iupac_name("Preferred")

	@memoized_property
	def systematic_name(self):
		return self.get_iupac_name("Systematic")

	@property
	def fingerprint(self):
		"""
		Raw padded and hex-encoded fingerprint, as returned by the PUG REST API.
		"""

		for prop in self._record["properties"]:
			if prop.label == "Fingerprint" and prop.name == "SubStructure Keys":
				return prop.value

	@property
	def cactvs_fingerprint(self):
		"""
		PubChem CACTVS fingerprint.

		Each bit in the fingerprint represents the presence or absence of one of 881 chemical substructures.

		More information at ftp://ftp.ncbi.nlm.nih.gov/pubchem/specifications/pubchem_fingerprints.txt
		"""

		# Skip first 4 bytes (contain length of fingerprint) and last 7 bits (padding) then re-pad to 881 bits

		return '{:020b}'.format(int(self.fingerprint[8:], 16))[:-7].zfill(881)

	# @memoized_property
	# def hill_formula(self):
	# 	element_count = Counter(self.elements)
	# 	hill = []
	#
	# 	alphabet = sorted(ELEMENTS.symbols)
	#
	# 	if "C" in element_count:
	# 		hill.append("C")
	# 		alphabet.remove("C")
	# 		count = element_count["C"]
	# 		if count > 1:
	# 			hill.append(f"<sub>{count}</sub>")
	# 		if "H" in element_count:
	# 			hill.append("H")
	# 			alphabet.remove("H")
	# 			count = element_count["H"]
	# 			if count > 1:
	# 				hill.append(f"<sub>{count}</sub>")
	#
	# 	for element in alphabet:
	# 		if element in element_count:
	# 			hill.append(element)
	# 			count = element_count[element]
	# 			if count > 1:
	# 				hill.append(f"<sub>{count}</sub>")
	#
	# 	return ''.join(hill)

# TODO from record:
	# charge
	# properties
		# label='Compound', name='Canonicalized'
		# label='Compound Complexity', name=None
	# cid
	# counts


# TODO:
def compounds_to_frame(compounds):
	"""
	Construct a pandas :class:`~pandas.DataFrame` from a list of :class:`~pubchempy.Compound` objects.
	"""

	import pandas as pd
	if isinstance(compounds, Compound):
		compounds = [compounds]
	return pd.DataFrame.from_records([dict(c) for c in compounds], index='CID')
