#!/usr/bin/env python
#
#  compound.py
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
from collections import Counter
from itertools import zip_longest

# this package
from chemistry_tools.constants import CoordinateType, log
from chemistry_tools.elements import ELEMENTS
from chemistry_tools.property_format import *
from chemistry_tools.toxnet import toxnet
from .atom import Atom
from .bond import Bond
from .errors import ResponseParseError
from .utils import _parse_prop, get_full_json, get_json, memoized_property, request


class Compound:
	"""Corresponds to a single record from the PubChem Compound database.

	The PubChem Compound database is constructed from the Substance database using a standardization and deduplication
	process. Each Compound is uniquely identified by a CID.
	"""

	def __init__(self, record):
		"""Initialize with a record dict from the PubChem PUG REST service.

		For most users, the ``from_cid()`` class method is probably a better way of creating Compounds.

		:param dict record: A compound record returned by the PubChem PUG REST service.
		"""
		self._record = None
		self._atoms = {}
		self._bonds = {}
		self.record = record
		self.hazards = []  # COSHH Hazards
		self.CAS = ''
		self._physical_properties = {}  # Physical Properties (dictionary)
		self._full_record = get_full_json(self.cid)
		self._parse_full_record()

	@property
	def record(self):
		"""The raw compound record returned by the PubChem PUG REST service."""
		return self._record

	@property
	def full_record(self):
		return self._full_record

	@record.setter
	def record(self, record):
		self._record = record
		log.debug('Created %s' % self)
		self._setup_atoms()
		self._setup_bonds()
		self._full_record = get_full_json(self.cid)

	def _parse_full_record(self):
		try:
			for record in self.full_record["Record"]["Section"]:
				if record["TOCHeading"] == "Chemical Safety":
					try:
						for hazard in record["Information"][0]["Value"]["StringWithMarkup"][0]["Markup"]:
							self.hazards.append(hazard["Extra"])
					except KeyError:
						pass

				elif record["TOCHeading"] == "Chemical and Physical Properties":
					for section in record["Section"]:
						if section["TOCHeading"] == "Computed Properties":
							for physical_property in section["Section"]:
								name = physical_property["TOCHeading"]
								self._physical_properties[name] = {}
								self._physical_properties[name]["Description"] = physical_property[
									"Description"]

								try:
									self._physical_properties[name]["Value"] = Decimal(
											str(physical_property["Information"][0]["Value"]["Number"][0]))
								except KeyError:
									value = physical_property["Information"][0]["Value"]["StringWithMarkup"][0][
										"String"]
									if value == "Yes":
										value = True
									elif value == "No":
										value = False

									self._physical_properties[name]["Value"] = value

								try:
									self._physical_properties[name]["Unit"] = \
										physical_property["Information"][0]["Value"]["Unit"]
								except KeyError:
									self._physical_properties[name]["Unit"] = None

						elif section["TOCHeading"] == "Experimental Properties":
							# First Try TOXNET
							try:
								self._physical_properties = {**self._physical_properties, **toxnet(self.CAS)}
							except ValueError:  # Not Found in TOXNET
								# import traceback
								# traceback.print_exc()
								pass
							for physical_property in section["Section"]:
								name = physical_property["TOCHeading"]

								if name == "Other Experimental Properties":
									name = "Other Chemical/Physical Properties"
								elif name == "LogKoa":
									name = "Octanol/Water Partition Coefficient"
								elif name == "Density":
									name = "Density/Specific Gravity"

								if (name in self._physical_properties) or (
										name in ["Molecular Formula", "Molecular Weight", "Physical Description"]):
									continue

								self._physical_properties[name] = {}
								self._physical_properties[name]["Description"] = physical_property[
									"Description"]

								# TODO: Skip Physical Description, :
								try:
									self._physical_properties[name]["Value"] = Decimal(
											str(physical_property["Information"][0]["Value"]["Number"][0]))
								except KeyError:
									value = property_format(
											physical_property["Information"][0]["Value"]["StringWithMarkup"][0][
												"String"])
									if value == "Yes":
										value = True
									elif value == "No":
										value = False

									self._physical_properties[name]["Value"] = value

								try:
									self._physical_properties[name]["Unit"] = \
										physical_property["Information"][0]["Value"]["Unit"]
								except KeyError:
									self._physical_properties[name]["Unit"] = None
							# import pprint
							# pprint.pprint(self._physical_properties)

				elif record["TOCHeading"] == "Names and Identifiers":
					for section in record["Section"]:
						if section["TOCHeading"] == "Record Description":
							for description in section["Information"]:
								try:
									if description["Description"] == "Physical Description":
										self.physical_description = description["Value"]["StringWithMarkup"][0]

									elif description["Description"] == "Ontology Summary":
										self.ontology = description["Value"]["StringWithMarkup"][0]

									elif description["Description"] == "Metabolite Description":
										self.metabolite = description["Value"]["StringWithMarkup"][0]
								except KeyError:
									pass

						elif section["TOCHeading"] == "Computed Descriptors":
							for subsection in section["Section"]:
								if subsection["TOCHeading"] == "IUPAC Name":
									self.IUPAC = subsection["Information"][0]["Value"]["StringWithMarkup"][0]

						elif section["TOCHeading"] == "Molecular Formula":
							self.formula = section["Information"][0]["Value"]["StringWithMarkup"][0]["String"]

						elif section["TOCHeading"] == "Other Identifiers":
							for subsection in section["Section"]:
								if subsection["TOCHeading"] == "CAS":
									self.CAS = subsection["Information"][0]["Value"]["StringWithMarkup"][0]["String"]

						elif section["TOCHeading"] == "Synonyms":
							for subsection in section["Section"]:
								if subsection["TOCHeading"] == "Depositor-Supplied Synonyms":
									self.synonyms = []
									existing_names = [x.lower().replace("-", '') for x in
													  [self.CAS, self.IUPAC["String"]]]
									for synonym in subsection["Information"][0]["Value"]["StringWithMarkup"]:
										if synonym["String"].lower().replace("-", '') not in existing_names:
											self.synonyms.append(synonym["String"])
											if len(self.synonyms) >= 10:
												break
		except KeyError:
			pass

	def _setup_atoms(self):
		"""Derive Atom objects from the record."""
		# Delete existing atoms
		self._atoms = {}
		# Create atoms
		aids = self.record['atoms']['aid']
		elements = self.record['atoms']['element']
		if not len(aids) == len(elements):
			raise ResponseParseError('Error parsing atom elements')
		for aid, element in zip(aids, elements):
			self._atoms[aid] = Atom(aid=aid, number=element)
		# Add coordinates
		if 'coords' in self.record:
			coord_ids = self.record['coords'][0]['aid']
			xs = self.record['coords'][0]['conformers'][0]['x']
			ys = self.record['coords'][0]['conformers'][0]['y']
			zs = self.record['coords'][0]['conformers'][0].get('z', [])
			if not len(coord_ids) == len(xs) == len(ys) == len(self._atoms) or (zs and not len(zs) == len(coord_ids)):
				raise ResponseParseError('Error parsing atom coordinates')
			for aid, x, y, z in zip_longest(coord_ids, xs, ys, zs):
				self._atoms[aid].set_coordinates(x, y, z)
		# Add charges
		if 'charge' in self.record['atoms']:
			for charge in self.record['atoms']['charge']:
				self._atoms[charge['aid']].charge = charge['value']

	def _setup_bonds(self):
		"""Derive Bond objects from the record."""
		self._bonds = {}
		if 'bonds' not in self.record:
			return
		# Create bonds
		aid1s = self.record['bonds']['aid1']
		aid2s = self.record['bonds']['aid2']
		orders = self.record['bonds']['order']
		if not len(aid1s) == len(aid2s) == len(orders):
			raise ResponseParseError('Error parsing bonds')
		for aid1, aid2, order in zip(aid1s, aid2s, orders):
			self._bonds[frozenset((aid1, aid2))] = Bond(aid1=aid1, aid2=aid2, order=order)
		# Add styles
		if 'coords' in self.record and 'style' in self.record['coords'][0]['conformers'][0]:
			aid1s = self.record['coords'][0]['conformers'][0]['style']['aid1']
			aid2s = self.record['coords'][0]['conformers'][0]['style']['aid2']
			styles = self.record['coords'][0]['conformers'][0]['style']['annotation']
			for aid1, aid2, style in zip(aid1s, aid2s, styles):
				self._bonds[frozenset((aid1, aid2))].style = style

	@classmethod
	def from_cid(cls, cid, **kwargs):
		"""Retrieve the Compound record for the specified CID.

		Usage::

			c = Compound.from_cid(6819)

		:param int cid: The PubChem Compound Identifier (CID).
		"""
		record = json.loads(request(cid, **kwargs).content.decode())['PC_Compounds'][0]
		return cls(record)

	def __repr__(self):
		return 'Compound(%s)' % self.cid if self.cid else 'Compound()'

	def __eq__(self, other):
		return isinstance(other, type(self)) and self.record == other.record

	def to_dict(self, properties=None):
		"""Return a dictionary containing Compound data. Optionally specify a list of the desired properties.

		synonyms, aids and sids are not included unless explicitly specified using the properties parameter. This is
		because they each require an extra request.
		"""
		if not properties:
			skip = {'aids', 'sids', 'synonyms'}
			properties = [p for p in dir(Compound) if isinstance(getattr(Compound, p), property) and p not in skip]
		return {p: [i.to_dict() for i in getattr(self, p)] if p in {'atoms', 'bonds'} else getattr(self, p) for p in
				properties}

	def to_series(self, properties=None):
		"""Return a pandas :class:`~pandas.Series` containing Compound data. Optionally specify a list of the desired
		properties.

		synonyms, aids and sids are not included unless explicitly specified using the properties parameter. This is
		because they each require an extra request.
		"""
		import pandas as pd
		return pd.Series(self.to_dict(properties))

	@staticmethod
	def format_string(stringwithmarkup):
		string = list(stringwithmarkup["String"])
		try:
			markup_list = stringwithmarkup["Markup"]
		except KeyError:
			markup_list = []

		for markup in markup_list:
			style = None
			start = markup["Start"]
			end = markup["Length"] + start - 1
			if markup["Type"] == "Italics":
				style = "i"
			# handle Other formats

			if style is None:
				print(markup)
				continue

			string[start] = f"<{style}>{string[start]}"
			string[end] = f"{string[end]}</{style}>"

		string = ''.join(string)

		return string

	"""Structure"""

	@property
	def elements(self):
		"""List of element symbols for atoms in this Compound."""
		return [a.element for a in self.atoms]

	@property
	def atoms(self):
		"""List of :class:`Atoms <pubchempy.Atom>` in this Compound."""
		return sorted(self._atoms.values(), key=lambda x: x.aid)

	@property
	def bonds(self):
		"""List of :class:`Bonds <pubchempy.Bond>` between :class:`Atoms <pubchempy.Atom>` in this Compound."""
		return sorted(self._bonds.values(), key=lambda x: (x.aid1, x.aid2))

	@memoized_property
	def sids(self):
		"""Requires an extra request. Result is cached."""
		if self.cid:
			results = get_json(self.cid, operation='sids')
			return results['InformationList']['Information'][0]['SID'] if results else []

	@memoized_property
	def aids(self):
		"""Requires an extra request. Result is cached."""
		if self.cid:
			results = get_json(self.cid, operation='aids')
			return results['InformationList']['Information'][0]['AID'] if results else []

	@property
	def coordinate_type(self):
		if CoordinateType.TWO_D in self.record['coords'][0]['type']:
			return '2d'
		elif CoordinateType.THREE_D in self.record['coords'][0]['type']:
			return '3d'

	@property
	def molecular_formula(self):
		"""Molecular formula."""
		return _parse_prop({'label': 'Molecular Formula'}, self.record['props'])

	"""Identifiers"""

	@property
	def cid(self):
		"""The PubChem Compound Identifier (CID).

		.. note::

			When searching using a SMILES or InChI query that is not present in the PubChem Compound database, an
			automatically generated record may be returned that contains properties that have been calculated on the
			fly. These records will not have a CID property.
		"""
		if 'id' in self.record and 'id' in self.record['id'] and 'cid' in self.record['id']['id']:
			return self.record['id']['id']['cid']

	@property
	def smiles(self):
		"""Canonical SMILES, with no stereochemistry information."""
		return _parse_prop({'label': 'SMILES', 'name': 'Canonical'}, self.record['props'])

	@property
	def canonical_smiles(self):
		"""Canonical SMILES, with no stereochemistry information."""
		return self.smiles

	@property
	def isomeric_smiles(self):
		"""Isomeric SMILES."""
		return _parse_prop({'label': 'SMILES', 'name': 'Isomeric'}, self.record['props'])

	@property
	def inchi(self):
		"""InChI string."""
		return _parse_prop({'label': 'InChI', 'name': 'Standard'}, self.record['props'])

	@property
	def inchikey(self):
		"""InChIKey."""
		return _parse_prop({'label': 'InChIKey', 'name': 'Standard'}, self.record['props'])

	@property
	def iupac_name(self):
		"""Preferred IUPAC name."""
		# Note: Allowed, CAS-like Style, Preferred, Systematic, Traditional are available in full record
		return _parse_prop({'label': 'IUPAC Name', 'name': 'Preferred'}, self.record['props'])

	@property
	def systematic_name(self):
		"""Systematic IUPAC name."""
		# Note: Allowed, CAS-like Style, Preferred, Systematic, Traditional are available in full record
		return _parse_prop({'label': 'IUPAC Name', 'name': 'Systematic'}, self.record['props'])

	@memoized_property
	def hill_formula(self):
		element_count = Counter(self.elements)
		hill = []

		alphabet = sorted(ELEMENTS.symbols)

		if "C" in element_count:
			hill.append("C")
			alphabet.remove("C")
			count = element_count["C"]
			if count > 1:
				hill.append(f"<sub>{count}</sub>")
			if "H" in element_count:
				hill.append("H")
				alphabet.remove("H")
				count = element_count["H"]
				if count > 1:
					hill.append(f"<sub>{count}</sub>")

		for element in alphabet:
			if element in element_count:
				hill.append(element)
				count = element_count[element]
				if count > 1:
					hill.append(f"<sub>{count}</sub>")

		return ''.join(hill)

	@memoized_property
	def _synonyms(self):
		"""A ranked list of all the names associated with this Compound.

		Requires an extra request. Result is cached.
		"""
		if self.cid:
			results = get_json(self.cid, operation='synonyms')
			return results['InformationList']['Information'][0]['Synonym'] if results else []

	@property
	def fingerprint(self):
		"""Raw padded and hex-encoded fingerprint, as returned by the PUG REST API."""
		return _parse_prop({'implementation': 'E_SCREEN'}, self.record['props'])

	@property
	def cactvs_fingerprint(self):
		"""PubChem CACTVS fingerprint.

		Each bit in the fingerprint represents the presence or absence of one of 881 chemical substructures.

		More information at ftp://ftp.ncbi.nlm.nih.gov/pubchem/specifications/pubchem_fingerprints.txt
		"""
		# Skip first 4 bytes (contain length of fingerprint) and last 7 bits (padding) then re-pad to 881 bits
		return '{:020b}'.format(int(self.fingerprint[8:], 16))[:-7].zfill(881)

	"""Other"""

	@property
	def volume_3d(self):
		conf = self.record['coords'][0]['conformers'][0]
		if 'data' in conf:
			return _parse_prop({'label': 'Shape', 'name': 'Volume'}, conf['data'])

	@property
	def multipoles_3d(self):
		conf = self.record['coords'][0]['conformers'][0]
		if 'data' in conf:
			return _parse_prop({'label': 'Shape', 'name': 'Multipoles'}, conf['data'])

	@property
	def conformer_rmsd_3d(self):
		coords = self.record['coords'][0]
		if 'data' in coords:
			return _parse_prop({'label': 'Conformer', 'name': 'RMSD'}, coords['data'])

	@property
	def effective_rotor_count_3d(self):
		return _parse_prop({'label': 'Count', 'name': 'Effective Rotor'}, self.record['props'])

	@property
	def pharmacophore_features_3d(self):
		return _parse_prop({'label': 'Features', 'name': 'Pharmacophore'}, self.record['props'])

	@property
	def mmff94_partial_charges_3d(self):
		return _parse_prop({'label': 'Charge', 'name': 'MMFF94 Partial'}, self.record['props'])

	@property
	def mmff94_energy_3d(self):
		conf = self.record['coords'][0]['conformers'][0]
		if 'data' in conf:
			return _parse_prop({'label': 'Energy', 'name': 'MMFF94 NoEstat'}, conf['data'])

	@property
	def conformer_id_3d(self):
		conf = self.record['coords'][0]['conformers'][0]
		if 'data' in conf:
			return _parse_prop({'label': 'Conformer', 'name': 'ID'}, conf['data'])

	@property
	def shape_selfoverlap_3d(self):
		conf = self.record['coords'][0]['conformers'][0]
		if 'data' in conf:
			return _parse_prop({'label': 'Shape', 'name': 'Self Overlap'}, conf['data'])

	@property
	def feature_selfoverlap_3d(self):
		conf = self.record['coords'][0]['conformers'][0]
		if 'data' in conf:
			return _parse_prop({'label': 'Feature', 'name': 'Self Overlap'}, conf['data'])

	@property
	def shape_fingerprint_3d(self):
		conf = self.record['coords'][0]['conformers'][0]
		if 'data' in conf:
			return _parse_prop({'label': 'Fingerprint', 'name': 'Shape'}, conf['data'])

	def get_property_description(self, property):
		try:
			return self.get_property(property)["Description"]
		except KeyError:
			return

	def get_property_value(self, property):
		try:
			return self.get_property(property)["Value"]
		except KeyError:
			return "NotFound"

	def get_property_unit(self, property):
		try:
			return self.get_property(property)["Unit"]
		except KeyError:
			return

	def get_property(self, property):
		# TODO Error handling
		try:
			return self._physical_properties[property]
		except KeyError:
			return {"Value": "NotFound", "Unit": None, "Description": None}

	"""PubChem Computed Properties"""

	@property
	def molecular_mass(self):
		"""Molecular Mass."""
		return self.get_property_value("Molecular Weight")

	# return _parse_prop({'label': 'Molecular Weight'}, self.record['props'])

	@property
	def molecular_weight(self):
		"""Molecular Weight."""
		return self.molecular_mass

	@property
	def xlogp(self):
		"""XLogP."""
		return _parse_prop({'label': 'Log P'}, self.record['props'])

	@property
	def h_bond_donor_count(self):
		"""Hydrogen bond donor count."""
		return self.get_property_value("Hydrogen Bond Donor Count")

	# return _parse_prop({'implementation': 'E_NHDONORS'}, self.record['props'])

	@property
	def h_bond_acceptor_count(self):
		"""Hydrogen bond acceptor count."""
		return self.get_property_value("Hydrogen Bond Acceptor Count")

	# return _parse_prop({'implementation': 'E_NHACCEPTORS'}, self.record['props'])

	@property
	def rotatable_bond_count(self):
		"""Rotatable bond count."""
		return self.get_property_value("Rotatable Bond Count")

	# return _parse_prop({'implementation': 'E_NROTBONDS'}, self.record['props'])

	@property
	def exact_mass(self):
		"""Exact mass."""
		return self.get_property_value("Exact Mass")

	# return _parse_prop({'label': 'Mass', 'name': 'Exact'}, self.record['props'])

	@property
	def monoisotopic_mass(self):
		"""Monoisotopic mass."""
		return self.get_property_value("Monoisotopic Mass")

	# return _parse_prop({'label': 'Weight', 'name': 'MonoIsotopic'}, self.record['props'])

	@property
	def tpsa(self):
		"""Topological Polar Surface Area."""
		return self.get_property_value("Topological Polar Surface Area")

	# return _parse_prop({'implementation': 'E_TPSA'}, self.record['props'])

	@property
	def heavy_atom_count(self):
		"""Heavy atom count."""
		return self.get_property_value("Heavy Atom Count")

	# if 'count' in self.record and 'heavy_atom' in self.record['count']:
	#	return self.record['count']['heavy_atom']

	@property
	def charge(self):
		"""Formal charge on this Compound."""
		return self.get_property_value("Formal Charge")

	# return self.record['charge'] if 'charge' in self.record else 0

	@property
	def complexity(self):
		"""Complexity."""
		return self.get_property_value("Complexity")

	# return _parse_prop({'implementation': 'E_COMPLEXITY'}, self.record['props'])

	@property
	def isotope_atom_count(self):
		"""Isotope atom count."""
		return self.get_property_value("Isotope Atom Count")

	# if 'count' in self.record and 'isotope_atom' in self.record['count']:
	#	return self.record['count']['isotope_atom']

	@property
	def defined_atom_stereo_count(self):
		"""Defined atom stereocenter count."""
		return self.get_property_value("Defined Atom Stereocenter Count")

	# if 'count' in self.record and 'atom_chiral_def' in self.record['count']:
	#	return self.record['count']['atom_chiral_def']

	@property
	def undefined_atom_stereo_count(self):
		"""Undefined atom stereocenter count."""
		return self.get_property_value("Undefined Atom Stereocenter Count")

	# if 'count' in self.record and 'atom_chiral_undef' in self.record['count']:
	#	return self.record['count']['atom_chiral_undef']

	@property
	def defined_bond_stereo_count(self):
		"""Defined bond stereocenter count."""
		return self.get_property_value("Defined Bond Stereocenter Count")

	# if 'count' in self.record and 'bond_chiral_def' in self.record['count']:
	#	return self.record['count']['bond_chiral_def']

	@property
	def undefined_bond_stereo_count(self):
		"""Undefined bond stereocenter count."""
		return self.get_property_value("Undefined Bond Stereocenter Count")

	# if 'count' in self.record and 'bond_chiral_undef' in self.record['count']:
	#	return self.record['count']['bond_chiral_undef']

	@property
	def covalent_unit_count(self):
		"""Covalently-bonded unit count."""
		return self.get_property_value("Covalently-Bonded Unit Count")

	# if 'count' in self.record and 'covalent_unit' in self.record['count']:
	#	return self.record['count']['covalent_unit']

	@property
	def is_canonicalized(self):
		"""Compound Is Canonicalized"""
		return self.get_property_value("Compound Is Canonicalized")

	@property
	def atom_stereo_count(self):
		"""Atom stereocenter count."""
		if 'count' in self.record and 'atom_chiral' in self.record['count']:
			return self.record['count']['atom_chiral']

	@property
	def bond_stereo_count(self):
		"""Bond stereocenter count."""
		if 'count' in self.record and 'bond_chiral' in self.record['count']:
			return self.record['count']['bond_chiral']

	"""TOXNET / Experimental Properties"""

	@property
	def boiling_point(self):
		"""Boiling Point"""
		return self.get_property_value("Boiling Point")

	@property
	def color(self):
		"""Color/Form"""
		return self.get_property_value("Color/Form")

	@property
	def density(self):
		"""Density/Specific Gravity"""
		return self.get_property_value("Density/Specific Gravity")

	@property
	def specific_gravity(self):
		"""Density/Specific Gravity"""
		return self.get_property_value("Density/Specific Gravity")

	@property
	def dissociation_constant(self):
		"""Dissociation Constants"""
		return self.get_property_value("Dissociation Constants")

	@property
	def heat_combustion(self):
		"""Heat of Combustion"""
		return self.get_property_value("Heat of Combustion")

	@property
	def melting_point(self):
		"""Melting Point"""
		return self.get_property_value("Melting Point")

	@property
	def partition_coeff(self):
		"""Octanol/Water Partition Coefficient"""
		return self.get_property_value("Octanol/Water Partition Coefficient")

	@property
	def odor(self):
		"""Odor"""
		return self.get_property_value("Odor")

	@property
	def other_props(self):
		"""Other Chemical/Physical Properties"""
		return self.get_property_value("Other Chemical/Physical Properties")

	@property
	def solubility(self):
		"""Solubility"""
		return self.get_property_value("Solubility")

	@property
	def spectral_props(self):
		"""Spectral Properties"""
		return self.get_property_value("Spectral Properties")

	@property
	def surface_tension(self):
		"""Surface Tension"""
		return self.get_property_value("Surface Tension")

	@property
	def vapor_density(self):
		"""Vapor Density"""
		return self.get_property_value("Vapor Density")

	@property
	def vapor_pressure(self):
		"""Vapor Pressure"""
		return self.get_property_value("Vapor Pressure")


class CompoundIdType:
	#: Original Deposited Compound
	DEPOSITED = 0
	#: Standardized Form of the Deposited Compound
	STANDARDIZED = 1
	#: Component of the Standardized Form
	COMPONENT = 2
	#: Neutralized Form of the Standardized Form
	NEUTRALIZED = 3
	#: Deposited Mixture Component
	MIXTURE = 4
	#: Alternate Tautomer Form of the Standardized Form
	TAUTOMER = 5
	#: Ionized pKa Form of the Standardized Form
	IONIZED = 6
	#: Unspecified or Unknown Compound Type
	UNKNOWN = 255


def compounds_to_frame(compounds, properties=None):
	"""
	Construct a pandas :class:`~pandas.DataFrame` from a list of :class:`~pubchempy.Compound` objects.

	Optionally specify a list of the desired :class:`~pubchempy.Compound` properties.
	"""

	import pandas as pd
	if isinstance(compounds, Compound):
		compounds = [compounds]
	properties = set(properties) | {'cid'} if properties else None
	return pd.DataFrame.from_records([c.to_dict(properties) for c in compounds], index='cid')
