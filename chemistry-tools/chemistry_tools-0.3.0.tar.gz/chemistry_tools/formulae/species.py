#!/usr/bin/env python3
#
#  species.py
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
#  Based on ChemPy (https://github.com/bjodah/chempy)
#  |  Copyright (c) 2015-2018, Björn Dahlgren
#  |  All rights reserved.
#  |
#  |  Redistribution and use in source and binary forms, with or without modification,
#  |  are permitted provided that the following conditions are met:
#  |
#  |    Redistributions of source code must retain the above copyright notice, this
#  |    list of conditions and the following disclaimer.
#  |
#  |    Redistributions in binary form must reproduce the above copyright notice, this
#  |    list of conditions and the following disclaimer in the documentation and/or
#  |    other materials provided with the distribution.
#  |
#  |  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  |  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  |  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  |  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
#  |  ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  |  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  |  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
#  |  ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  |  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  |  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#  Also based on Pyteomics (https://github.com/levitsky/pyteomics)
#  |  Copyright (c) 2011-2015, Anton Goloborodko & Lev Levitsky
#  |  Licensed under the Apache License, Version 2.0 (the "License");
#  |  you may not use this file except in compliance with the License.
#  |  You may obtain a copy of the License at
#  |
#  |    http://www.apache.org/licenses/LICENSE-2.0
#  |
#  |  Unless required by applicable law or agreed to in writing, software
#  |  distributed under the License is distributed on an "AS IS" BASIS,
#  |  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  |  See the License for the specific language governing permissions and
#  |  limitations under the License.
#  |
#  |  See also:
#  |  Goloborodko, A.A.; Levitsky, L.I.; Ivanov, M.V.; and Gorshkov, M.V. (2013)
#  |  "Pyteomics - a Python Framework for Exploratory Data Analysis and Rapid Software
#  |  Prototyping in Proteomics", Journal of The American Society for Mass Spectrometry,
#  |  24(2), 301–304. DOI: `10.1007/s13361-012-0516-6 <http://dx.doi.org/10.1007/s13361-012-0516-6>`_
#  |
#  |  Levitsky, L.I.; Klein, J.; Ivanov, M.V.; and Gorshkov, M.V. (2018)
#  |  "Pyteomics 4.0: five years of development of a Python proteomics framework",
#  |  Journal of Proteome Research.
#  |  DOI: `10.1021/acs.jproteome.8b00717 <http://dx.doi.org/10.1021/acs.jproteome.8b00717>`_
#
#  Also based on molmass (https://github.com/cgohlke/molmass)
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


#  3rd party
from cawdrey import frozendict

# this package
from .formula import Formula


class Species(Formula):
	"""
	Formula with phase information (e.g. solid, liquid, gas, or aqueous)

	Species extends :class:`Formula` with the new attribute :attr:`phase`

	Attributes
	----------
	phase: Either "s", "l", "g", or "aq". ``None`` represents an unknown phase.
	"""

	_phases = frozendict(s="Solid", l="Liquid", g="Gas", aq="Aqueous")

	def __init__(self, composition=None, charge=0, phase=None):
		"""
		:param composition: A :py:class:`Formula` or :py:class:`Species` object with the elemental composition of a substance,
			or a :class:`python:dict` representing the same.
			If ``None`` an empty object is created
		:type composition: :py:class:`Formula`, optional
		:param charge:
		:type charge: int, optional
		:param phase: Either "s", "l", "g", or "aq". ``None`` represents an unknown phase.
		:type phase: str or None

		"""

		super().__init__(composition, charge)

		self.phase = phase

	@classmethod
	def from_kwargs(cls, *, charge=0, phase=None, **kwargs):
		"""
		Create a new :class:`Species` object from keyword arguments representing the elements in the compound

		:param charge:
		:type charge: int, optional

		:rtype: :class:`Formula`
		"""

		return cls(kwargs, charge=charge, phase=phase)

	@classmethod
	def from_string(
			cls, formula, phase=None, charge=0):
		"""
		Create a new :class:`Species` object by parsing a string

		Analogous to :meth:`Formula.from_string` but with the addition that
		the phase is determined from the formula.

		Parameters
		----------
		formula: str
			e.g. 'H2O', 'NaCl(s)', 'CO2(aq)', 'CO2(g)'
		phase: Either "s", "l", "g", or "aq". ``None`` represents an unknown phase.

		Examples
		--------
		>>> water = Species.from_string('H2O')
		>>> water.phase
		None
		>>> NaCl = Species.from_string('NaCl(s)')
		>>> NaCl.phase
		s
		>>> Hg_l = Species.from_string('Hg(l)')
		>>> Hg_l.phase
		l
		>>> CO2g = Species.from_string('CO2(g)')
		>>> CO2g.phase
		g
		>>> CO2aq = Species.from_string('CO2(aq)')
		>>> CO2aq.phase
		aq
		"""

		if phase is None:
			for p in cls._phases:
				if formula.endswith(f"({p})"):
					phase = p
					break

		f = super().from_string(formula, charge)
		f.phase = phase
		return f

	def copy(self):
		return self.__class__(self, charge=self.charge, phase=self.phase)

	def __eq__(self, other):
		if isinstance(other, Species):
			if super().__eq__(other):
				return self.phase == other.phase
		else:
			return super().__eq__(other)

	def _repr_elements(self):
		elements = super()._repr_elements()

		if self.phase:
			elements.append(f"phase={self.phase}")

		return elements

	@property
	def hill_formula(self):
		"""

		:return:
		:rtype: str
		"""

		hill = super().hill_formula

		if self.phase:
			return f"{hill}({self.phase})"
		else:
			return hill

	@property
	def empirical_formula(self):
		"""

		:return:
		:rtype: str
		"""

		hill = super().empirical_formula

		if self.phase:
			return f"{hill}({self.phase})"
		else:
			return hill
