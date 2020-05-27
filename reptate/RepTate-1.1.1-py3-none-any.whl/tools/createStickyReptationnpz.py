# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# --------------------------------------------------------------------------------------------------------
#
# Authors:
#     Jorge Ramirez, jorge.ramirez@upm.es
#     Victor Boudara, victor.boudara@gmail.com
#
# Useful links:
#     http://blogs.upm.es/compsoftmatter/software/reptate/
#     https://github.com/jorge-ramirez-upm/RepTate
#     http://reptate.readthedocs.io
#
# --------------------------------------------------------------------------------------------------------
#
# Copyright (2017-2020): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
#
# This file is part of RepTate.
#
# RepTate is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RepTate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RepTate.  If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------------------------------------------
"""Module createStickyReptationnpz

Precalculates the Sticky Reptation theory and saves all datain a more compact *.npz format

"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate


def g_descloizeaux(x, tol):
    N = len(x)
    gx = np.zeros(len(x))  # output array
    for n in range(0, N):
        err = 2 * tol  # initialise error
        m = 0
        while err > tol:
            m += 1
            m2 = m * m
            dgx = (1 - np.exp(-m2 * x[n])) / m2
            gx[n] += dgx
            err = dgx / gx[n]
    return gx


ZeMAX = 10
ZsMAX = 10
tau_s = 1
Ge = 1
alpha = 10
ZE = np.linspace(1, ZeMAX, ZeMAX, dtype=np.int16)
ZS = np.linspace(2, ZsMAX, ZsMAX, dtype=np.int16)

for Ze in ZE:
    for Zs in ZS:
        print(Ze, Zs)

        wrange = [1e-6, 1e5]
        # ---------------------------------------------
        # NUMERICAL SETTINGS
        # 1. Double reptation
        tol = 1e-6  # tolerance to truncate infinite sums
        # 2. Transform of G(t) to G'(w) and G''(w)
        tmin = 0.1 / max(wrange)  # shortest time outside omega interval
        tmax = 10 / min(wrange)  # largest  time outside omega interval
        ntime = 100  # number of time points
        # END NUMERICAL SETTINGS
        # ---------------------------------------------

        # ---------------------------------------------
        # CALCULATE RELAXATION MODULUS
        # time range [s] to calculate relaxation modulus G(t)
        t = np.logspace(np.log10(tmin), np.log10(tmax), ntime)
        warray = np.logspace(np.log10(min(wrange)), np.log10(max(wrange)), ntime)

        # - - - - - - - - - - - - - - - - - - - - - - -
        # CALCULATE STICKY-ROUSE RELAXATION MODULUS
        GSR = 0  # initialise output
        tau_srouse = (
            tau_s * (0.5 * Zs) ** 2
        )  # Sticky-Rouse time of the strand that relaxes after sticker dissociation. The factor 0.5 arises because the length of this strand is twice the length of a strand between stickers.
        tS = t / tau_srouse
        dsum = 0.0
        for q in range(1, int(0.5 * Zs) + 1):
            if q < Ze:
                GSR += 0.2 * np.exp(-tS * q ** 2)
                dsum += 0.2
            else:
                GSR += np.exp(-tS * q ** 2)
                dsum += 1

        # Normalise (verified using the asymptotic value of G(t)
        #            for short times, t->0.)
        GSR *= 0.5 * Zs / (dsum * Ze)

        # - - - - - - - - - - - - - - - - - - - - - - -
        # CALCULATE DOUBLE-REPTATION RELAXATION MODULUS
        GREP = np.zeros(len(t))  # initialise output
        tau_rep = Ze * tau_srouse  # sticky-reptation time
        tR = t / tau_rep  # Time in units of reptation time
        H = Ze / alpha  # Prefactor in des Cloizeaux model
        Ut = tR + g_descloizeaux(H * tR, tol) / H

        for n in range(0, len(Ut)):
            err = 2 * tol
            q = -1
            while err > tol:  # truncate infinite sum when tolerance is met
                q += 2  # sum only over odd values of q
                q2 = q * q
                dGrep = np.exp(-q2 * Ut[n]) / q2
                GREP[n] += dGrep
                err = dGrep / GREP[n]
        GREP = (GREP * 8 / np.pi ** 2) ** 2

        # Relaxation modulus G(t) = sum of Sticky Rouse and Reptation
        G = Ge * (GSR + GREP)
        # END CALCULATE RELAXATION MODULUS
        # ---------------------------------------------

        # ---------------------------------------------
        # GET DYNAMIC MODULI G(w) from G(t)
        f = interpolate.interp1d(
            t, G, kind="cubic", assume_sorted=True, fill_value="extrapolate"
        )
        g0 = f(0)
        ind1 = np.argmax(t > 0)
        t1 = t[ind1]
        g1 = G[ind1]
        tinf = np.max(t)
        wp = np.logspace(np.log10(1 / tinf), np.log10(1 / t1), ntime)
        G1G2 = np.zeros((ntime, 3))
        G1G2[:, 0] = wp[:]

        coeff = (G[ind1 + 1 :] - G[ind1:-1]) / (t[ind1 + 1 :] - t[ind1:-1])
        for i, w in enumerate(wp):

            G1G2[i, 1] = (
                g0
                + np.sin(w * t1) * (g1 - g0) / w / t1
                + np.dot(coeff, -np.sin(w * t[ind1:-1]) + np.sin(w * t[ind1 + 1 :])) / w
            )

            G1G2[i, 2] = (
                -(1 - np.cos(w * t1)) * (g1 - g0) / w / t1
                - np.dot(coeff, np.cos(w * t[ind1:-1]) - np.cos(w * t[ind1 + 1 :])) / w
            )

        # STORE THE FUNCTION IN SOME OTHER TEMPORARY ARRAY
        # INTERPOLATE IT SO THAT THE OMEGA RANGE AND POINTS ARE THE SAME AS IN THE EXPERIMENTAL DATA
        f1 = interpolate.interp1d(
            wp, G1G2[:, 1], kind="cubic", assume_sorted=True, fill_value="extrapolate"
        )
        f2 = interpolate.interp1d(
            wp, G1G2[:, 2], kind="cubic", assume_sorted=True, fill_value="extrapolate"
        )

        plt.loglog(warray, f1(warray), label="G1")
        plt.loglog(warray, f2(warray), label="G2")
        print(warray)
        print(f1(warray))
        print(f2(warray))
        plt.show()


data = []
# for k in p:
#    data.append(np.loadtxt(flist[k]))

# np.savez_compressed("linlin.npz",Z=Z, cnu=cnu, data=data)
