#!/usr/bin/env python
#
#  atom.py
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

# stdlib
from itertools import zip_longest

# this package
from chemistry_tools.elements import ELEMENTS
from chemistry_tools.pubchem.errors import ResponseParseError


class Atom:
	"""Class to represent an atom in a :class:`~pubchempy.Compound`."""

	def __init__(self, aid, number, x=None, y=None, z=None, charge=0):
		"""Initialize with an atom ID, atomic number, coordinates and optional change.

		:param int aid: Atom ID
		:param int number: Atomic number
		:param float x: X coordinate.
		:param float y: Y coordinate.
		:param float z: (optional) Z coordinate.
		:param int charge: (optional) Formal charge on atom.
		"""

		self.aid = aid
		# The atom ID within the owning Compound.
		self.number = number
		# The atomic number for this atom.
		self.x = x
		# The x coordinate for this atom.
		self.y = y
		# The y coordinate for this atom.
		self.z = z
		# The z coordinate for this atom. Will be ``None`` in 2D Compound records.
		self.charge = charge
		# The formal charge on this atom.

	def __repr__(self):
		return f'Atom({self.aid}, {self.element})'

	def __eq__(self, other):
		return (
				isinstance(other, type(self))
				and self.aid == other.aid
				and self.element == other.element
				and self.x == other.x
				and self.y == other.y
				and self.z == other.z
				and self.charge == other.charge
				)

	@property
	def element(self):
		"""
		The element symbol for this atom.
		"""

		return ELEMENTS[self.number].symbol

	def to_dict(self):
		"""
		Return a dictionary containing Atom data.
		"""

		data = {'aid': self.aid, 'number': self.number, 'element': self.element}

		for coord in {'x', 'y', 'z'}:
			if getattr(self, coord) is not None:
				data[coord] = getattr(self, coord)

		if self.charge != 0:
			data['charge'] = self.charge

		return data

	def set_coordinates(self, x, y, z=None):
		"""
		Set all coordinate dimensions at once.
		"""

		self.x = x
		self.y = y
		self.z = z

	@property
	def coordinate_type(self):
		"""
		Returns whether this atom has 2D or 3D coordinates.

		:rtype: str
		"""

		if self.z is None:
			return '2d'
		else:
			return '3d'


def parse_atoms(atoms_dict, coords_dict=None):
	"""

	:param atoms_dict:
	:type atoms_dict: dict
	:param coords_dict:
	:type coords_dict: dict or None

	:return:
	:rtype: dict
	"""

	atoms = {}

	# Create atoms
	aids = atoms_dict['aid']
	elements = atoms_dict['element']

	if not len(aids) == len(elements):
		raise ResponseParseError('Error parsing atom elements')

	for aid, element in zip(aids, elements):
		atoms[aid] = Atom(aid=aid, number=element)

	# Add coordinates
	if coords_dict:
		coord_ids = coords_dict[0]['aid']

		xs = coords_dict[0]['conformers'][0]['x']
		ys = coords_dict[0]['conformers'][0]['y']
		zs = coords_dict[0]['conformers'][0].get('z', [])

		if not len(coord_ids) == len(xs) == len(ys) == len(atoms) or (zs and not len(zs) == len(coord_ids)):
			raise ResponseParseError('Error parsing atom coordinates')

		for aid, x, y, z in zip_longest(coord_ids, xs, ys, zs):
			atoms[aid].set_coordinates(x, y, z)

	# Add charges
	if 'charge' in atoms_dict:
		for charge in atoms_dict['charge']:
			atoms[charge['aid']].charge = charge['value']

	return atoms
