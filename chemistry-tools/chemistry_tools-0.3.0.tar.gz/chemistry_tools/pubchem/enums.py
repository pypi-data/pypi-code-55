#!/usr/bin/env python3
#
#  enums.py
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

from domdf_python_tools.enums import StrEnum


class PubChemNamespace(StrEnum):
	cid = "cid"
	name = "name"
	smiles = "smiles"
	# inchi = "inchi"# TODO: requires argument
	# sdf = "sdf"
	inchikey = "inchikey"
	# formula = "formula"
	Cid = "cid"
	Name = "name"
	Smiles = "smiles"
	# Inchi = "inchi"# TODO: requires argument
	# Sdf = "sdf"
	Inchikey = "inchikey"
	# Formula = "formula"
	CID = "cid"
	NAME = "name"
	SMILES = "smiles"
	# INCHI = "inchi"# TODO: requires argument
	# SDF = "sdf"
	INCHIKEY = "inchikey"
	# FORMULA = "formula"

	# TODO: listkey for formula lookup https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest$_Toc494865583

	@classmethod
	def is_valid_value(cls, value):
		return str(value) in set(str(item) for item in PubChemNamespace)


class PubChemFormats(StrEnum):
	JSON = "JSON"
	Json = "JSON"
	json = "JSON"
	XML = "XML"
	Xml = "XML"
	xml = "XML"
	CSV = "CSV"
	csv = "CSV"
	Csv = "CSV"
	PNG = "PNG"
	png = "PNG"
	Png = "PNG"

	@classmethod
	def is_valid_value(cls, value):
		return str(value).upper() in set(str(item) for item in PubChemFormats)


class CoordinateType:
	TWO_D = 1
	THREE_D = 2
	SUBMITTED = 3
	EXPERIMENTAL = 4
	COMPUTED = 5
	STANDARDIZED = 6
	AUGMENTED = 7
	ALIGNED = 8
	COMPACT = 9
	UNITS_ANGSTROMS = 10
	UNITS_NANOMETERS = 11
	UNITS_PIXEL = 12
	UNITS_POINTS = 13
	UNITS_STDBONDS = 14
	UNITS_UNKNOWN = 255