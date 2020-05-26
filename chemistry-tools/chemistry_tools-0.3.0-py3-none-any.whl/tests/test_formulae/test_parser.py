#!/usr/bin/env python3
#
#  test_parser.py
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


import decimal

import pytest
from mathematical.utils import rounders

from chemistry_tools.formulae.html import string_to_html
from chemistry_tools.formulae.latex import string_to_latex
from chemistry_tools.formulae.parser import string_to_composition, mass_from_composition, relative_atomic_masses
from chemistry_tools.formulae.unicode import string_to_unicode


def test_formula_to_composition():
	assert string_to_composition('H2O') == {"H": 2, "O": 1}
	assert string_to_composition('Fe+3') == {0: 3, "Fe": 1}
	assert string_to_composition('Na+1') == {0: 1, "Na": 1}
	assert string_to_composition('Na+') == {0: 1, "Na": 1}
	assert string_to_composition('Cl-') == {0: -1, "Cl": 1}
	assert string_to_composition('NaCl') == {"Na": 1, "Cl": 1}
	assert string_to_composition('NaCl(s)') == {"Na": 1, "Cl": 1}
	assert string_to_composition('Fe(SCN)2+') == {
			0: 1, "C": 2, "N": 2, "S": 2, "Fe": 1}
	assert string_to_composition('Fe(SCN)2+1') == {
			0: 1, "C": 2, "N": 2, "S": 2, "Fe": 1}
	assert string_to_composition('((H2O)2OH)12') == {"H": 60, "O": 36}

	# Special case: solvated electron:
	assert string_to_composition('e-') == {0: -1}
	assert string_to_composition('e-1') == {0: -1}
	assert string_to_composition('e-(aq)') == {0: -1}
	assert string_to_composition('SO4-2(aq)') == {0: -2, "O": 4, "S": 1}

	# prefixes and suffixes
	assert string_to_composition('.NO2(g)') == {"N": 1, "O": 2}
	assert string_to_composition('.NH2') == {"H": 2, "N": 1}
	assert string_to_composition('ONOOH') == {"H": 1, "N": 1, "O": 3}
	assert string_to_composition('.ONOO') == {"N": 1, "O": 3}
	assert string_to_composition('.NO3-2') == {0: -2, "N": 1, "O": 3}

	with pytest.raises(ValueError):
		string_to_composition('F-F')

	# TODO: parse greek prefixes
	# assert string_to_composition('alpha-FeOOH(s)') == {"H": 1, "O": 2, "Fe": 1}
	# assert string_to_composition('epsilon-Zn(OH)2(s)') == {"H": 2, "O": 2, "Zn": 1}

	assert string_to_composition('Na2CO3.7H2O(s)') == {"Na": 2, "C": 1, "O": 10, "H": 14}


def test_formula_to_latex():
	assert string_to_latex('H2O') == 'H_{2}O'
	assert string_to_latex('C6H6+') == 'C_{6}H_{6}^{+}'
	assert string_to_latex('Fe(CN)6-3') == 'Fe(CN)_{6}^{3-}'
	assert string_to_latex('C18H38+2') == 'C_{18}H_{38}^{2+}'
	assert string_to_latex('((H2O)2OH)12') == '((H_{2}O)_{2}OH)_{12}'
	assert string_to_latex('NaCl') == 'NaCl'
	assert string_to_latex('NaCl(s)') == 'NaCl(s)'
	assert string_to_latex('e-(aq)') == 'e^{-}(aq)'
	assert string_to_latex('Ca+2(aq)') == 'Ca^{2+}(aq)'
	assert string_to_latex('.NO2(g)') == r'^\bullet NO_{2}(g)'
	assert string_to_latex('.NH2') == r'^\bullet NH_{2}'
	assert string_to_latex('ONOOH') == 'ONOOH'
	assert string_to_latex('.ONOO') == r'^\bullet ONOO'
	assert string_to_latex('.NO3-2') == r'^\bullet NO_{3}^{2-}'
	assert string_to_latex('alpha-FeOOH(s)') == r'\alpha-FeOOH(s)'
	assert string_to_latex('epsilon-Zn(OH)2(s)') == (
			r'\varepsilon-Zn(OH)_{2}(s)')
	assert string_to_latex('Na2CO3.7H2O(s)') == r'Na_{2}CO_{3}\cdot 7H_{2}O(s)'
	assert string_to_latex('Na2CO3.1H2O(s)') == r'Na_{2}CO_{3}\cdot H_{2}O(s)'


def test_formula_to_unicoce():
	assert string_to_unicode('NH4+') == 'NH₄⁺'
	assert string_to_unicode('H2O') == 'H₂O'
	assert string_to_unicode('C6H6+') == 'C₆H₆⁺'
	assert string_to_unicode('Fe(CN)6-3') == 'Fe(CN)₆³⁻'
	assert string_to_unicode('C18H38+2') == 'C₁₈H₃₈²⁺'
	assert string_to_unicode('((H2O)2OH)12') == '((H₂O)₂OH)₁₂'
	assert string_to_unicode('NaCl') == 'NaCl'
	assert string_to_unicode('NaCl(s)') == 'NaCl(s)'
	assert string_to_unicode('e-(aq)') == 'e⁻(aq)'
	assert string_to_unicode('Ca+2(aq)') == 'Ca²⁺(aq)'
	assert string_to_unicode('.NO2(g)') == '⋅NO₂(g)'
	assert string_to_unicode('.NH2') == '⋅NH₂'
	assert string_to_unicode('ONOOH') == 'ONOOH'
	assert string_to_unicode('.ONOO') == '⋅ONOO'
	assert string_to_unicode('.NO3-2') == '⋅NO₃²⁻'
	assert string_to_unicode('alpha-FeOOH(s)') == 'α-FeOOH(s)'
	assert string_to_unicode('epsilon-Zn(OH)2(s)') == 'ε-Zn(OH)₂(s)'
	assert string_to_unicode('Na2CO3.7H2O(s)') == 'Na₂CO₃·7H₂O(s)'
	assert string_to_unicode('Na2CO3.1H2O(s)') == 'Na₂CO₃·H₂O(s)'


def test_formula_to_html():
	assert string_to_html('H2O') == 'H<sub>2</sub>O'
	assert string_to_html('C6H6+') == 'C<sub>6</sub>H<sub>6</sub><sup>+</sup>'
	assert string_to_html('Fe(CN)6-3') == 'Fe(CN)<sub>6</sub><sup>3-</sup>'
	assert string_to_html('C18H38+2') == 'C<sub>18</sub>H<sub>38</sub><sup>2+</sup>'
	assert string_to_html('((H2O)2OH)12') == '((H<sub>2</sub>O)<sub>2</sub>OH)<sub>12</sub>'
	assert string_to_html('NaCl') == 'NaCl'
	assert string_to_html('NaCl(s)') == 'NaCl(s)'
	assert string_to_html('e-(aq)') == 'e<sup>-</sup>(aq)'
	assert string_to_html('Ca+2(aq)') == 'Ca<sup>2+</sup>(aq)'
	assert string_to_html('.NO2(g)') == r'&sdot;NO<sub>2</sub>(g)'
	assert string_to_html('.NH2') == r'&sdot;NH<sub>2</sub>'
	assert string_to_html('ONOOH') == 'ONOOH'
	assert string_to_html('.ONOO') == r'&sdot;ONOO'
	assert string_to_html('.NO3-2') == r'&sdot;NO<sub>3</sub><sup>2-</sup>'
	assert string_to_html('alpha-FeOOH(s)') == r'&alpha;-FeOOH(s)'
	assert string_to_html('epsilon-Zn(OH)2(s)') == (
			r'&epsilon;-Zn(OH)<sub>2</sub>(s)')
	assert string_to_html('Na2CO3.7H2O(s)') == 'Na<sub>2</sub>CO<sub>3</sub>&sdot;7H<sub>2</sub>O(s)'
	assert string_to_html('Na2CO3.1H2O(s)') == 'Na<sub>2</sub>CO<sub>3</sub>&sdot;H<sub>2</sub>O(s)'


def test_mass_from_composition():
	mass1 = mass_from_composition({11: 1, 9: 1})
	assert rounders(mass1, "0.000000") == decimal.Decimal("41.988172")

	mass2 = mass_from_composition({"Na": 1, "F": 1})
	assert mass1 == mass2
	assert rounders(mass2, "0.000000") == decimal.Decimal("41.988172")


def test_relative_atomic_masses():
	assert rounders(relative_atomic_masses[0], "0.0000") == decimal.Decimal("1.0079")


def test_mass_from_composition__formula():
	mass = mass_from_composition(string_to_composition('NaF'))
	assert rounders(mass, "0.000000") == decimal.Decimal("41.988172")

	Fminus = mass_from_composition(string_to_composition('F/-'))
	assert abs(Fminus - 18.998403163 - 5.489e-4) < 1e-7
