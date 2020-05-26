#!/usr/bin/env python3
#
#  iso_dist.py
"""
Isotope Distributions
"""
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


# stdlib
from collections import OrderedDict
from enum import Enum

# this package
from .dataarray import DataArray
from .unicode import string_to_unicode


class IsoDistSort(Enum):
	"""
	Lookup for sorting isotope distribution output
	"""
	formula = 0
	mass = 1
	abundance = 2
	relative_abundance = 3
	Formula = 0
	Mass = 1
	Abundance = 2
	Relative_abundance = 3
	Relative_Abundance = 3

	def __int__(self):
		return int(self.value)


class IsotopeDistribution(DataArray):
	"""


	Each composition can be accessed with their hill formulae like a dictionary
	(e.g. iso_dict["H[1]2O[16]"]
	"""

	def __init__(self, formula):
		"""

		:param formula: A :class:`Formula` object to create the distribution for
		:type formula: :class:`Formula`
		"""

		iso_compositions = list(formula.iter_isotopologues())
		compositions = OrderedDict()
		max_abundance = 0

		for comp in iso_compositions:
			compositions[comp.hill_formula] = comp
			abundance = comp.isotopic_composition_abundance
			if abundance > max_abundance:
				max_abundance = abundance

		super().__init__(formula=iso_compositions[0].no_isotope_hill_formula, data=compositions)

		self.max_abundance = max_abundance

	_as_array_kwargs = {"sort_by", "reverse", "format_percentage"}
	_as_table_alignment = ["left", "right", "right", "right"]
	_as_table_float_format = [None, ".4f", ".6f", ".6f"]

	def as_array(self, sort_by=IsoDistSort.formula, reverse=False, format_percentage=True):
		"""
		Returns the isotope distribution data as a list of lists

		:param sort_by: The column to sort by.
		:type sort_by: IsoDistSort
		:param: Whether the isotopologues should be sorted in reverse order. Default ``False``.
		:type reverse: bool, optional
		:param: Whether the abundances should be formatted as percentages or not. Default ``False``.
		:type format_percentage: bool, optional

		:rtype: list[list]
		"""

		if sort_by not in IsoDistSort:
			raise ValueError(f"Unrecognised value for 'sort_by': {sort_by}")
		elif sort_by == IsoDistSort.formula:
			sort_key = lambda comp: comp.hill_formula
		elif sort_by == IsoDistSort.mass:
			sort_key = lambda comp: comp.mass
		elif sort_by == IsoDistSort.abundance:
			sort_key = lambda comp: comp.isotopic_composition_abundance
		elif sort_by == IsoDistSort.relative_abundance:
			sort_key = lambda comp: comp.isotopic_composition_abundance / self.max_abundance
		else:
			raise ValueError(f"Unrecognised value for 'sort_by': {sort_by}")

		output = []

		for comp in sorted(self.values(), key=sort_key, reverse=reverse):
			abundance = comp.isotopic_composition_abundance
			rel_abund = abundance / self.max_abundance
			row = [comp.hill_formula, f"{comp.mass:0.4f}"]
			if format_percentage:
				row += [f"{abundance:0.2%}", f"{rel_abund:0.2%}"]
			else:
				row += [f"{abundance:0.6f}", f"{rel_abund:0.6f}"]
			output.append(row)
			# TODO: Unicode, latex, html representations of formulae

		output.insert(0, ["Formula", "Mass", "Abundance", "Relative Abundance"])

		return output

	def __str__(self):
		table = self.as_table(sort_by=IsoDistSort.relative_abundance, reverse=True, tablefmt="fancy_grid")
		return f"\n Isotope Distribution for {string_to_unicode(self.formula)}\n{table}"

# TODO: as_mass_spec
