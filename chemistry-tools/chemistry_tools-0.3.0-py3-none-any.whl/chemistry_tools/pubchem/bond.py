#!/usr/bin/env python
#
#  bond.py
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
from domdf_python_tools.enums import IntEnum

# this package
from chemistry_tools.pubchem.errors import ResponseParseError


class BondType(IntEnum):
	SINGLE = 1
	DOUBLE = 2
	TRIPLE = 3
	QUADRUPLE = 4
	DATIVE = 5
	COMPLEX = 6
	IONIC = 7
	UNKNOWN = 255


class Bond:
	"""
	Class to represent a bond between two atoms in a :class:`~pubchempy.Compound`.
	"""

	def __init__(self, aid1, aid2, order=BondType.SINGLE, style=None):
		"""
		Initialize with begin and end atom IDs, bond order and bond style.

		:param aid1: ID of the begin atom of this bond
		:type aid1: int
		:param aid2: ID of the end atom of this bond
		:type aid2: int
		:param order: Bond order.
		:type order: :class:`chemistry_tools.pubchem.bond.BondType`
		:param style: Bond style annotation.
		:type style:
		"""

		self.aid1 = aid1
		self.aid2 = aid2
		self.order = BondType(order)
		self.style = style

	def __repr__(self):
		return 'Bond({}, {}, {})'.format(self.aid1, self.aid2, self.order)

	def __eq__(self, other):
		return (
				isinstance(other, type(self))
				and self.aid1 == other.aid1
				and self.aid2 == other.aid2
				and self.order == other.order
				and self.style == other.style
				)

	def to_dict(self):
		"""
		Return a dictionary containing Bond data.
		"""

		data = {'aid1': self.aid1, 'aid2': self.aid2, 'order': self.order}

		if self.style is not None:
			data['style'] = self.style

		return data



def parse_bonds(bonds_dict, coords_dict=None):
	"""

	:param bonds_dict:
	:type bonds_dict: dict
	:param coords_dict:
	:type coords_dict: dict or None

	:return:
	:rtype: dict
	"""

	bonds = {}

	if not bonds_dict:
		return bonds

	# Create bonds
	aid1s = bonds_dict['aid1']
	aid2s = bonds_dict['aid2']
	orders = bonds_dict['order']

	if not len(aid1s) == len(aid2s) == len(orders):
		raise ResponseParseError('Error parsing bonds')

	for aid1, aid2, order in zip(aid1s, aid2s, orders):
		bonds[frozenset((aid1, aid2))] = Bond(aid1=aid1, aid2=aid2, order=order)

	# Add styles
	if coords_dict and 'style' in coords_dict[0]['conformers'][0]:
		aid1s = coords_dict[0]['conformers'][0]['style']['aid1']
		aid2s = coords_dict[0]['conformers'][0]['style']['aid2']
		styles = coords_dict[0]['conformers'][0]['style']['annotation']
		for aid1, aid2, style in zip(aid1s, aid2s, styles):
			bonds[frozenset((aid1, aid2))].style = style

	return bonds
