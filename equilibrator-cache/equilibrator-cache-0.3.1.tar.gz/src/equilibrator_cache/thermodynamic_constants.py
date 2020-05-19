"""A module for all thermodynamic constants and general calculations."""
# The MIT License (MIT)
#
# Copyright (c) 2018 Institute for Molecular Systems Biology, ETH Zurich.
# Copyright (c) 2019 Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import warnings  # Silence NEP 18 warning

import numpy as np
import pint


# Disable Pint's old fallback behavior (must come before importing Pint)
os.environ["PINT_ARRAY_PROTOCOL_FALLBACK"] = "0"

ureg = pint.UnitRegistry(system="mks")
Q_ = ureg.Quantity

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    Q_([])


R = Q_(8.31e-3, "kJ / mol / K")
LOG10 = np.log(10)
FARADAY = Q_(96.485, "kC / mol")
default_T = Q_(298.15, "K")
default_I = Q_(0.25, "M")
default_pH = Q_(7.0)
default_pMg = Q_(10)
default_RT = R * default_T
default_c_mid = Q_(1e-3, "M")
default_c_range = (Q_(1e-6, "M"), Q_(1e-2, "M"))
standard_dg_formation_mg = Q_(-455.3, "kJ/mol")  # ΔGf(Mg2+) at 298.15K
standard_dh_formation_mg = Q_(-467.00, "kJ/mol")  # ΔHf(Mg2+) at 298.15K

standard_concentration = Q_(1.0, "M")
physiological_concentration = Q_(1.0e-3, "M")


@ureg.check("[concentration]", "[temperature]")
def debye_hueckel(ionic_strength: Q_, temperature: Q_) -> Q_:
    """Compute the ionic-strength-dependent transformation coefficient.

    For the Legendre transform to convert between chemical and biochemical
    Gibbs energies, we use the extended Debye-Hueckel theory to calculate the
    dependence on ionic strength and temperature.

    Parameters
    ----------
    ionic_strength : Quantity
        The ionic-strength
    temperature : Quantity
        The temperature


    Returns
    -------
    Quantity
        The unitless DH factor associated with the ionic strength at this
        temperature.

    """
    if ionic_strength <= 0.0:
        return Q_(0.0, "kJ/mol")

    _a1 = Q_(9.20483e-3, "kJ / mol / M**0.5 / K")
    _a2 = Q_(1.284668e-5, "kJ / mol / M**0.5 / K**2")
    _a3 = Q_(4.95199e-8, "kJ / mol / M**0.5 / K**3")
    alpha = _a1 * temperature - _a2 * temperature ** 2 + _a3 * temperature ** 3
    B = Q_(1.6, "1 / M**0.5")

    dh_factor = (
        alpha * ionic_strength ** 0.5 / (1.0 + B * ionic_strength ** 0.5)
    )
    assert dh_factor.check("[energy]/[substance]")
    return dh_factor


@ureg.check("", "[concentration]", "[temperature]", None, None, "", None)
def legendre_transform(
    p_h: Q_,
    ionic_strength: Q_,
    temperature: Q_,
    num_protons: float,
    charge: float,
    p_mg: Q_ = default_pMg,
    num_magnesiums: float = 0.0,
) -> Q_:
    r"""Calculate the Legendre Transform value for a certain microspecies.

    at a certain pH, I, T, pMg

    Parameters
    ----------
    p_h : Quantity
        The pH value, i.e., the logarithmic scale for the molar
        concentration of hydrogen ions :math:`-log10([H+])`.
    ionic_strength : Quantity
        The ionic-strength.
    temperature : Quantity
        The temperature.
    num_protons : float
        The number of protons.
    charge : float
        The electric charge of the microspecies.
    p_mg : Quantity
        The logarithmic molar concentration of magnesium ions
        :math:`-log10([Mg2+])`, (Default value = default_pMg).
    num_magnesiums : float, optional
        The number of magnesium ions associated to the
        microspecies (Default value = 0.0).


    Returns
    -------
    Quantity
        The transformed relative :math:`\Delta G` (in units of RT).

    """
    # all terms are calculated in kJ/mol
    RT = R * temperature

    proton_term = num_protons * RT * LOG10 * p_h

    _dg_mg = (temperature / default_T) * standard_dg_formation_mg + (
        1.0 - temperature / default_T
    ) * standard_dh_formation_mg
    magnesium_term = num_magnesiums * (RT * LOG10 * p_mg - _dg_mg)
    dh_factor = debye_hueckel(ionic_strength, temperature)
    is_term = dh_factor * (charge ** 2 - num_protons - 4 * num_magnesiums)

    assert proton_term.check("[energy]/[substance]")
    assert magnesium_term.check("[energy]/[substance]")
    assert is_term.check("[energy]/[substance]")
    return proton_term + magnesium_term - is_term
