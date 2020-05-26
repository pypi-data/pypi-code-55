#!/usr/bin/env python3
#
#  test_formula.py
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
#  Based on Pyteomics (https://github.com/levitsky/pyteomics)
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
#  Also based on ChemPy (https://github.com/bjodah/chempy)
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
#


# stdlib
import decimal

# 3rd party
import pytest
from mathematical.utils import rounders

from chemistry_tools.formulae import Formula, Species
from chemistry_tools.elements import isotope_data, D, O


def test_formula():
	# From string
	f1 = Formula.from_string("(C6H5)2NH")
	f2 = Formula.from_string("C12H11N")
	assert f1 == f2

	# from dict
	f3 = Formula({"C": 12, "H": 11, "N": 1})
	assert f1 == f3
	assert f2 == f3

	# from kwargs
	f4 = Formula.from_kwargs(C=12, H=11, N=1)
	assert f1 == f4
	assert f2 == f4
	assert f3 == f4

	# from composition
	f5 = Formula(f1)
	assert f5 == f1
	assert f5 == f2

	s = Formula.from_string('H+')
	assert s.charge == 1
	assert s.mass == 1.007941


def test_charged_formula():
	# From string
	f1 = Formula.from_string("(C6H5)2NH+")
	f2 = Formula.from_string("C12H11N", charge=1)
	assert f1 == f2

	# from dict
	f3 = Formula({"C": 12, "H": 11, "N": 1}, charge=1)
	assert f3 == {"C": 12, "H": 11, "N": 1}
	assert f1 == f3
	assert f2 == f3

	# from kwargs
	f4 = Formula.from_kwargs(C=12, H=11, N=1, charge=1)
	assert f1 == f4
	assert f2 == f4
	assert f3 == f4

	# from composition
	f5 = Formula(f1)
	assert f5 == f1
	assert f5 == f2

	for charge in [1, 2, 3]:
		with pytest.raises(ValueError):
			Formula.from_string(f'BCHFKOH+{charge:d}', charge + 1)


def test_isotope_formula():
	# from dict
	f3 = Formula({"C[12]": 10, "C[13]": 2, "H": 11, "N": 1})
	assert dict(f3) == {"[12C]": 10, "[13C]": 2, "H": 11, "N": 1}

	# from composition
	f5 = Formula(f3)
	assert f5 == f3


def test_formula_sum():
	# Test sum of Formula objects.
	assert Formula.from_string('C6H12O6') + Formula.from_string('H2O') == {"C": 6, "H": 14, "O": 7}


def test_Composition_sub():
	# Test subtraction of Composition objects
	assert {} - Formula.from_string('C6H12O6') == {"C": -6, "H": -12, "O": -6}


def test_Composition_mul():
	# Test multiplication of Composition by integers
	f1 = Formula.from_string("H2O2")
	assert f1 == {"H": 2, "O": 2}
	assert 2 * f1 == {"H": 4, "O": 4}
	assert f1 * 2 == {"H": 4, "O": 4}


def test_calculate_mass():
	# Calculate mass by a formula.
	assert rounders(Formula.from_string('(C6H5)2NH').monoisotopic_mass, "0.000000") == decimal.Decimal("169.089149")

	# Calculate average mass / molecular weight by a formula.
	assert rounders(Formula.from_string('(C6H5)2NH').average_mass, "0.00") == decimal.Decimal("169.22")
	assert rounders(Formula.from_string('(C6H5)2NH').average_mass, "0.00") == decimal.Decimal("169.22")
	assert Formula.from_string('(C6H5)2NH').average_mass == Formula.from_string('(C6H5)2NH').average_mass

	# mz
	assert Formula.from_string('C12H13N+').get_mz() == Formula.from_string('C12H13N', charge=1).average_mass


@pytest.mark.parametrize("charge", [1, 2, 3, 4])
def test_calculate_mz(charge):
	# Calculate m/z of an ion.
	assert Formula.from_string('C12H13N+').exact_mass == Formula.from_string('C12H13N', charge=1).exact_mass
	# perhaps math.isclose()
	# assert Formula.from_string('C12H13N+').mass == Formula.from_string('C12H13N', charge=1).exact_mass
	# assert Formula.from_string('C12H13N+').exact_mass == Formula.from_string('C12H13N', charge=1).mass
	# assert Formula.from_string('C12H13N+').mass == Formula.from_string('C12H13N', charge=1).mass

	assert Formula.from_string('C12H13N+').get_mz() == Formula.from_string('C12H13N', charge=1).get_mz()
	assert Formula.from_string('C12H13N+').mz == Formula.from_string('C12H13N', charge=1).get_mz()
	assert Formula.from_string('C12H13N+').get_mz() == Formula.from_string('C12H13N', charge=1).mz


def test_most_probable_isotopic_composition():
	assert (
			Formula.from_string('F').most_probable_isotopic_composition()
			== (Formula({'F[19]': 1, 'F[18]': 0}), 1.0)
			)

	Br2 = Formula.from_string('Br2')
	assert Br2.most_probable_isotopic_composition()[0] == Formula({'Br[79]': 1, 'Br[81]': 1})
	assert rounders(Br2.most_probable_isotopic_composition()[1], "0.000") == decimal.Decimal("0.5")

	C6Br6 = Formula.from_string('C6Br6')
	assert C6Br6.most_probable_isotopic_composition()[0] == Formula({'C[12]': 6, 'C[13]': 0, 'Br[79]': 3, 'Br[81]': 3})
	assert rounders(C6Br6.most_probable_isotopic_composition()[1], "0.000") == decimal.Decimal("0.293")

	assert (
			Formula.from_string('F10').most_probable_isotopic_composition()
			== (Formula({'F[19]': 10, }), 1.0)
			)

	assert Formula.from_string('CF4').most_probable_isotopic_composition(
			elements_with_isotopes=['F']) == (Formula({'C': 1, 'F[19]': 4}), 1.0)


def test_isotope_data():
	print(list(type((g[0][1]) - 1) for g in isotope_data.values()))
	assert all(abs(g[0][1] - 1) < 1e-6 for g in isotope_data.values())
	for g in isotope_data.values():
		s = sum(p[1] for num, p in g.items() if num)
		assert abs(s - 1) < 1e-6 or abs(s) < 1e-6


def test_iter_isotopologues():

	iter_isotopologues = Formula.from_string("C6Br6").iter_isotopologues()
	assert len(list(iter_isotopologues)) == 49

	iter_isotopologues = Formula.from_string("C6Br6").iter_isotopologues(
			elements_with_isotopes='Br')
	assert len(list(iter_isotopologues)) == 7


# TODO:
def test_iter_isotopologues_with_abundances():

	for state, abundance in Formula.from_string("BCHFKO").iter_isotopologues(
			elements_with_isotopes='F', report_abundance=True):
		assert state
		assert abundance


@pytest.fixture(scope="module")
def Br2():
	return Formula.from_string('Br2')


@pytest.fixture(scope="module")
def C6Br6():
	return Formula.from_string('C6Br6')


def test___str__(Br2, C6Br6):
	assert str(Br2) == "Formula({'Br': 2})"
	assert str(C6Br6) == "Formula({'C': 6, 'Br': 6})"


def test___repr__(Br2, C6Br6):
	assert repr(Br2) == "Formula({'Br': 2})"
	assert repr(C6Br6) == "Formula({'C': 6, 'Br': 6})"


@pytest.mark.parametrize("other", ["Br2", "abc", 123, 12, 34, [1, 2, 3]])
def test_unsupported_equals(Br2, other):
	assert Br2 != other


def test_Species():
	s = Species.from_string('H2O')
	assert s.phase is None
	assert Species.from_string('CO2(g)').phase == "g"
	assert Species.from_string('CO2(aq)').phase == "aq"
	assert Species.from_string('NaCl(s)').phase == "s"
	assert Species.from_string('H2O(l)').phase == "l"


def test_properties():
	f = Formula.from_string('C6H12O6')  # Sugar
	assert f.hill_formula == "C6H12O6"
	assert f.empirical_formula == "CH2O"
	assert f.n_atoms == 24
	assert f.n_elements == 3

	f = Formula.from_string('D2O')  # heavy water
	assert f.hill_formula == "D2O"
	assert f.empirical_formula == "D2O"
	assert f.monoisotopic_mass == 20.02311817516
	assert f.mass == 20.0276085556
	assert f.n_atoms == 3
	assert f.n_elements == 2
	assert D.nominalmass == 2
	assert O.nominalmass == 16


@pytest.mark.parametrize("formula, mass, exact_mass", [
		("C[12]", "12.00000", "12.00000"),
		("[12C]", "12.00000", "12.00000"),
		("[C12]", "12.00000", "12.00000"),
		('C[12]C', "24.01074", "24.00000"),
		('C[C12]', "24.01074", "24.00000"),
		('Co(Bpy)(CO)4', "327.15811", "326.98160"),
		('CH3CH2Cl', "64.51408", "64.00798"),
		('C2H5Cl', "64.51408", "64.00798"),
		('C1000H1000', "13018.68100", "13007.82503"),
		('Ru2(CO)8', "426.22116", "427.76802"),
		('RuClH(CO)(PPh3)3', "952.39958", "952.14935"),
		('PhSiMe3', "150.29333", "150.08648"),
		('C9H14Si', "150.29333", "150.08648"),
		('Ph(CO)C(CH3)3', "162.22872", "162.10447"),
		('C11H14O', "162.22872", "162.10447"),
		('HGlyGluTyrOH', "367.35455", "367.13795"),
		('C16H21N3O7', "367.35455", "367.13795"),
		('HCysTyrIleGlnAsnCysProLeuNH2', "952.15329", "951.43064"),
		('C41H65N11O11S2', "952.15329", "951.43064"),
		('HCysp(Trt)Tyrp(Tbu)IleGlnp(Trt)Asnp(Trt)ProLeuGlyNH2', "1689.11406", "1687.83417"),
		('C101H113N11O11S', "1689.11406", "1687.83417"),
		('C116H148N46O73P12', "3726.37115", "3724.61342"),
		('C47H83N15O16S', "1146.31971", "1145.58629"),
		('CDCl3', "120.38354", "118.92066"),
		('C[2H]Cl3', "120.38354", "118.92066"),
		('[13C]Cl4', "154.81495", "152.87877"),
		('[C13]Cl4', "154.81495", "152.87877"),
		('C5(PhBu(EtCHBr)2)3', "1194.60962", "1188.12038"),
		('C53H78Br6', "1194.60962", "1188.12038"),
		# TODO: ('AgCuRu4(H)2[CO]12{PPh3}2', "1438.4022", "1439.588960"),
		('C48H32AgCuO12P2Ru4', "1438.40422", "1439.58899"),
		('C6H8ClN', "129.58757", "129.03453"),
		('PhNH2.HCl', "129.58757", "129.03453"),
		('NH3.BF3', "84.83674", "85.03106"),
		('BF3H3N', "84.83674", "85.03106"),
		('CuH10O9S', "249.68485", "248.93415"),
		('CuSO4.5H2O', "249.68485", "248.93415"),
		])
def test_masses(formula, mass, exact_mass):
	f = Formula.from_string(formula)
	print(f)
	assert rounders(f.mass, "0.00000") == decimal.Decimal(mass)
	assert rounders(f.exact_mass, "0.00000") == decimal.Decimal(exact_mass)


@pytest.mark.parametrize("formula_1, formula_2", [
		('CH3CH2Cl', 'C2H5Cl'),
		('RuClH(CO)(PPh3)3', 'C55H46ClOP3Ru'),
		('PhSiMe3', 'C9H14Si'),
		('Ph(CO)C(CH3)3', 'C11H14O'),
		('HGlyGluTyrOH', 'C16H21N3O7'),
		('HCysTyrIleGlnAsnCysProLeuNH2', 'C41H65N11O11S2'),
		('HCysp(Trt)Tyrp(Tbu)IleGlnp(Trt)Asnp(Trt)ProLeuGlyNH2', 'C101H113N11O11S'),
		# TODO: ('CDCl3', 'C[2H]Cl3'), needs special case
		('[13C]Cl4', '[13C]Cl4'),
		('C5(PhBu(EtCHBr)2)3', 'C53H78Br6'),
		('PhNH2.HCl', 'C6H8ClN'),
		('NH3.BF3', 'BF3H3N'),
	])
def test_equivalent(formula_1, formula_2):
	f1 = Formula.from_string(formula_1)
	f2 = Formula.from_string(formula_2)
	assert f1 == f2


@pytest.mark.parametrize("formula_1, formula_2", [
		('CuSO4.5H2O', 'CuH10O9S'),
		('C1000H1000', 'CH'),
		('Ru2(CO)8', 'C4O4Ru'),
	])
def test_empirical_formula(formula_1, formula_2):
	f1 = Formula.from_string(formula_1)
	f2 = Formula.from_string(formula_2)
	assert f1.empirical_formula == f2.empirical_formula
	assert f1.empirical_formula == formula_2


@pytest.mark.parametrize("formula", [
		'', '()', '2', 'a', '(a)',
		# TODO: 'C:H', 'H:', 'C[H', 'H)2',  # failing
		'A', 'Aa', '2lC', '1C', '()0',
		'H0', '(H)0C', 'Ox: 0.26, 30Si: 0.74',
		"Hey", "O2Hey", "HeyO2",
	])
def test_invalid_formulae(formula):
	with pytest.raises(ValueError):
		print(Formula.from_string(formula))


@pytest.mark.parametrize("formula, data", [
		("H2O", {"H": 2, "O": 1}),
		("[2H]2O", {"[2H]": 2, "O": 1}),
		("CH3COOH", {"C": 2, "O": 2, "H": 4}),
		("EtOH", {"C": 2, "O": 1, "H": 6}),
		("CuSO4.5H2O", {"Cu": 1, "O": 9, "H": 10, "S": 1}),
		("(COOH)2", {"C": 2, "O": 4, "H": 2}),
		# TODO: ("AgCuRu4(H)2[CO]12{PPh3}2", {}),
		# TODO: ("CGCGAATTCGCG", {}),
		# TODO: ("MDRGEQGLLK", {}),
		])
def test_parsing(formula, data):
	assert Formula.from_string(formula) == data
