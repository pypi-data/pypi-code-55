#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  elements.py
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
#  Based on molmass (https://github.com/cgohlke/molmass)
#  |  Copyright (c) 1990-2020, Christoph Gohlke
#  |  All rights reserved.
#  |  Licensed under the BSD 3-Clause License
#  |  Redistribution and use in source and binary forms, with or without
#  |  modification, are permitted provided that the following conditions are met:
#  |
#  |  1. Redistributions of source code must retain the above copyright notice,
#  |     this list of conditions and the following disclaimer.
#  |
#  |  2. Redistributions in binary form must reproduce the above copyright notice,
#  |     this list of conditions and the following disclaimer in the documentation
#  |     and/or other materials provided with the distribution.
#  |
#  |  3. Neither the name of the copyright holder nor the names of its
#  |     contributors may be used to endorse or promote products derived from
#  |     this software without specific prior written permission.
#  |
#  |  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  |  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  |  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  |  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
#  |  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#  |  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#  |  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#  |  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#  |  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  |  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  |  POSSIBILITY OF SUCH DAMAGE.
#  |
#


# stdlib
from functools import lru_cache

# 3rd party
from domdf_python_tools import doctools
from domdf_python_tools.bases import Dictable
from memoized_property import memoized_property

# this package
from . import _table


class Element(Dictable):
	"""Chemical element.

	Attributes
	----------
	number : int
		Atomic number.
	symbol : str of length 1 or 2
		Chemical symbol.
	name : str
		Name in English.
	group : int
		Group in periodic table.
	period : int
		Period in periodic table.
	block : int
		Block in periodic table.
	series : int
		Index to chemical series.
	protons : int
		Number of protons.
	neutrons : int
		Number of neutrons in the most abundant naturally occurring stable.
		isotope
	nominalmass : int
		Mass number of the most abundant naturally occurring stable isotope.
	electrons : int
		Number of electrons.
	mass : float
		Relative atomic mass. Ratio of the average mass of atoms
		of the element to 1/12 of the mass of an atom of 12C.
	exactmass : float
		Relative atomic mass calculated from the isotopic composition.
	eleneg : float
		Electronegativity (Pauling scale).
	covrad : float
		Covalent radius in Angstrom.
	atmrad :
		Atomic radius in Angstrom.
	vdwrad : float
		Van der Waals radius in Angstrom.
	tboil : float
		Boiling temperature in K.
	tmelt : float
		Melting temperature in K.
	density : float
		Density at 295K in g/cm3 respectively g/L.
	oxistates : str
		Oxidation states.
	eleaffin : float
		Electron affinity in eV.
	eleconfig : str
		Ground state electron configuration.
	eleconfig_dict : dict
		Ground state electron configuration (shell, subshell): electrons.
	eleshells : int
		Number of electrons per shell.
	ionenergy : tuple
		Ionization energies in eV
	isotopes : dict
		Isotopic composition.
		keys: isotope mass number
		values: Isotope(relative atomic mass, abundance)

	"""

	def __init__(
			self, number, symbol, name,
			group=0, period=0, block='', series=0, mass=0.0, eleneg=0.0,
			eleaffin=0.0, covrad=0.0, atmrad=0.0, vdwrad=0.0, tboil=0.0,
			tmelt=0.0, density=0.0, eleconfig='', oxistates='',
			ionenergy=None, isotopes=None, description='',
			):

		super().__init__()

		self._number = number
		self._symbol = symbol
		self._name = name
		self._electrons = number
		self._protons = number
		self._group = group
		self._period = period
		self._block = block
		self._series = series
		self._mass = mass
		self._eleneg = eleneg
		self._eleaffin = eleaffin
		self._covrad = covrad
		self._atmrad = atmrad
		self._vdwrad = vdwrad
		self._tboil = tboil
		self._tmelt = tmelt
		self._density = density
		self._eleconfig = eleconfig
		self._oxistates = oxistates
		self._description = description

		if ionenergy is None:
			self._ionenergy = tuple()
		else:
			self._ionenergy = ionenergy

		self._isotopes = {}

		if isotopes is not None:
			for massnumber, isotope in isotopes.items():
				if isinstance(isotope, Isotope):
					self._isotopes[int(massnumber)] = isotope
				elif isinstance(isotope, (list, tuple)):
					self._isotopes[int(massnumber)] = Isotope(*isotope, massnumber)

	@property
	def __dict__(self):
		return dict(
				number=self._number,
				symbol=self._symbol,
				name=self._name,
				group=self._group,
				period=self._period,
				block=self._block,
				series=self._series,
				mass=self._mass,
				eleneg=self._eleneg,
				eleaffin=self._eleaffin,
				covrad=self._covrad,
				atmrad=self._atmrad,
				vdwrad=self._vdwrad,
				tboil=self._tboil,
				tmelt=self._tmelt,
				density=self._density,
				eleconfig=self._eleconfig,
				oxistates=self._oxistates,
				ionenergy=self._ionenergy,
				isotopes=self._isotopes,
				description=self._description
				)

	@memoized_property
	def number(self):
		return self._number

	@memoized_property
	def symbol(self):
		return self._symbol

	@memoized_property
	def name(self):
		return self._name

	@memoized_property
	def electrons(self):
		return self._electrons

	@memoized_property
	def protons(self):
		return self._protons

	@memoized_property
	def group(self):
		return self._group

	@memoized_property
	def period(self):
		return self._period

	@memoized_property
	def block(self):
		return self._block

	@memoized_property
	def series(self):
		return self._series

	@memoized_property
	def mass(self):
		return self._mass

	@memoized_property
	def molecular_weight(self):
		return self._mass

	@memoized_property
	def eleneg(self):
		return self._eleneg

	@memoized_property
	def eleaffin(self):
		return self._eleaffin

	@memoized_property
	def covrad(self):
		return self._covrad

	@memoized_property
	def atmrad(self):
		return self._atmrad

	@memoized_property
	def vdwrad(self):
		return self._vdwrad

	@memoized_property
	def tboil(self):
		return self._tboil

	@memoized_property
	def tmelt(self):
		return self._tmelt

	@memoized_property
	def density(self):
		return self._density

	@memoized_property
	def eleconfig(self):
		return self._eleconfig

	@memoized_property
	def oxistates(self):
		return self._oxistates

	@memoized_property
	def ionenergy(self):
		return self._ionenergy

	@memoized_property
	def isotopes(self):
		return self._isotopes

	@memoized_property
	def description(self):
		return self._description

	def __str__(self):
		return self.name

	def __repr__(self):
		ionenergy = []
		for i, j in enumerate(self.ionenergy):
			if i and (i % 5 == 0):
				ionenergy.append(f'\n        {j}')
			else:
				ionenergy.append(f'{j}')
		ionenergy = ', '.join(ionenergy)
		if len(self.ionenergy) > 5:
			ionenergy = f'(\n        {ionenergy},\n    )'
		elif len(self.ionenergy) == 1:
			ionenergy = f'({ionenergy},)'
		else:
			ionenergy = f'({ionenergy})'

		isotopes = []
		for massnum in sorted(self.isotopes):
			iso = self.isotopes[massnum]
			isotopes.append(
					'{0}: Isotope({1}, {2}, {0})'.format(
							massnum, iso.mass, iso.abundance
							)
					)
		isotopes = ',\n        '.join(isotopes)
		if len(self.isotopes) > 1:
			isotopes = f'{{\n        {isotopes},\n    }},'
		else:
			isotopes = f'{{{isotopes}}},'

		return ',\n    '.join((
				f"Element(\n    {self.number}, '{self.symbol}', '{self.name}'",
				f"group={self.group}, period={self.period},"
				f" block='{self.block}', series={self.series}",
				f"mass={self.mass}, eleneg={self.eleneg},"
				f" eleaffin={self.eleaffin}",
				f"covrad={self.covrad}, atmrad={self.atmrad},"
				f" vdwrad={self.vdwrad}",
				f"tboil={self.tboil}, tmelt={self.tmelt}, density={self.density}",
				f"eleconfig='{self.eleconfig}'",
				f"oxistates='{self.oxistates}'",
				f"ionenergy={ionenergy}",
				f"isotopes={isotopes}\n)"
				))

	@memoized_property
	def nominalmass(self):
		"""
		Return mass number of most abundant natural stable isotope.
		"""

		nominalmass = 0
		maxabundance = 0
		for massnum, iso in self.isotopes.items():
			if iso.abundance > maxabundance:
				maxabundance = iso.abundance
				nominalmass = massnum
		return nominalmass

	@memoized_property
	def neutrons(self):
		"""
		Return number neutrons in most abundant natural stable isotope.
		"""

		return self.nominalmass - self.protons

	@memoized_property
	def exactmass(self):
		"""
		Return relative atomic mass calculated from isotopic composition.
		"""

		return sum(iso.mass * iso.abundance for iso in self.isotopes.values())

	@memoized_property
	def eleconfig_dict(self):
		"""
		Return electron configuration as dict.
		"""

		adict = {}
		if self.eleconfig.startswith('['):
			base = self.eleconfig.split(' ', 1)[0][1:-1]
			adict.update(_table.ELEMENTS[base].eleconfig_dict)
		for e in self.eleconfig.split()[bool(adict):]:
			adict[(int(e[0]), e[1])] = int(e[2:]) if len(e) > 2 else 1
		return adict

	@memoized_property
	def eleshells(self):
		"""
		Return number of electrons in shell as tuple.
		"""

		eleshells = [0, 0, 0, 0, 0, 0, 0]
		for key, val in self.eleconfig_dict.items():
			eleshells[key[0] - 1] += val
		return tuple(ele for ele in eleshells if ele)

	def validate(self):
		"""Check consistency of data. Raise Error on failure."""
		assert self.period in _table.PERIODS
		assert self.group in _table.GROUPS
		assert self.block in _table.BLOCKS
		assert self.series in _table.SERIES

		if self.number != self.protons:
			raise ValueError(
					f'{self.symbol} - atomic number must equal proton number'
					)
		if self.protons != sum(self.eleshells):
			raise ValueError(
					f'{self.symbol} - number of protons must equal electrons'
					)
		if len(self.ionenergy) > 1:
			ionev_ = self.ionenergy[0]
			for ionev in self.ionenergy[1:]:
				if ionev <= ionev_:
					raise ValueError(
							f'{self.symbol} - ionenergy not increasing'
							)
				ionev_ = ionev

		mass = 0.0
		frac = 0.0
		for iso in self.isotopes.values():
			mass += iso.abundance * iso.mass
			frac += iso.abundance
		if abs(mass - self.mass) > 0.03:
			raise ValueError(
					f'{self.symbol} - average of isotope masses '
					f'({mass:.4f}) != mass ({self.mass:.4f})'
					)
		if abs(frac - 1.0) > 1e-9:
			raise ValueError(
					f'{self.symbol} - sum of isotope abundances != 1.0'
					)


class Isotope(Dictable):
	"""Isotope massnumber, relative atomic mass, and abundance."""

	def __init__(self, mass=0.0, abundance=1.0, massnumber=0):
		super().__init__()

		self._mass = mass
		self._abundance = abundance
		self._massnumber = massnumber

	@memoized_property
	def mass(self):
		return self._mass

	@memoized_property
	def abundance(self):
		return self._abundance

	@memoized_property
	def massnumber(self):
		return self._massnumber

	def __str__(self):
		return '{}, {:.4f}, {:.6f}%'.format(
				self.massnumber, self.mass, self.abundance * 100
				)

	def __repr__(self):
		return 'Isotope({}, {}, {})'.format(
				repr(self.mass), repr(self.abundance), repr(self.massnumber)
				)

	@property
	def __dict__(self):
		return dict(
				mass=self.mass,
				abundance=self.abundance,
				massnumber=self.massnumber,
				)


# Isotope 0 Key:
# mass of the most abundant isotope and 1.0 abundance.


# TODO: make frozen
class Elements:
	"""
	Ordered dict of Elements with lookup by number, symbol, and name.
	"""

	def __init__(self, *elements):
		self._list = []
		self._dict = {}
		for element in elements:
			if element.number > len(self._list) + 1:
				raise ValueError('Elements must be added in order')
			if element.number <= len(self._list):
				self._list[element.number - 1] = element
			else:
				self._list.append(element)
			self._dict[element.number] = element
			self._dict[element.symbol] = element
			self.add_alternate_spelling(element, element.name)

	def __str__(self):
		return f'[{", ".join(ele.symbol for ele in self._list)}]'

	def __repr__(self):
		elements = ',\n    '.join(
				'\n    '.join(line for line in repr(element).splitlines())
				for element in self._list
				)
		elements = f'Elements(\n    {elements},\n)'
		return elements

	def __contains__(self, item):
		return item in self._dict

	def __iter__(self):
		return iter(self._list)

	def __len__(self):
		return len(self._list)

	def __getitem__(self, key):
		if isinstance(key, str):
			try:
				return self._dict[key.casefold()]
			except KeyError:
				return self._dict[key]
		elif isinstance(key, int):
			return self._dict[key]
		elif isinstance(key, float):
			return self._dict[int(key)]
		elif isinstance(key, slice):
			start, stop, step = key.indices(len(self._list))
			return self._list[slice(start - 1, stop - 1, step)]
		else:
			try:
				symbol, isotope = self.split_isotope(key)
				return self._dict[symbol.capitalize()]
			except:
				raise KeyError(f"Unknown key: '{key}'")

	@lru_cache()
	def split_isotope(self, string):
		from chemistry_tools.formulae.formula import _split_isotope
		return _split_isotope(string)

	def add_alternate_spelling(self, element, spelling):
		self._dict[spelling] = element
		self._dict[spelling.lower()] = element
		self._dict[spelling.casefold()] = element

	@memoized_property
	def symbols(self):
		return [element.symbol for element in sorted(self._list, key=lambda e: e.number)]

	@memoized_property
	def names(self):
		return [str(element) for element in sorted(self._list, key=lambda e: e.number)]

	@memoized_property
	def lower_names(self):
		return [str(element).lower() for element in sorted(self._list, key=lambda e: e.number)]


@doctools.append_docstring_from(Element)
class HeavyHydrogen(Element):
	"""
	Subclass of Element to handle the Heavy Hydrogen isotopes Deuterium and Tritium
	"""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		if self.symbol not in {"D", "T"}:
			raise ValueError("'HeavyHydrogen' can only be used for Deuterium and Tritium")

	@memoized_property
	def nominalmass(self):
		"""
		Return mass number of most abundant natural stable isotope.
		"""

		if self.symbol == "D":
			return 2
		elif self.symbol == "T":
			return 3

	@memoized_property
	def as_isotope(self):
		"""
		Return the isotope in H[X] format

		:rtype: str
		"""

		return f'H[{self.nominalmass}]'
