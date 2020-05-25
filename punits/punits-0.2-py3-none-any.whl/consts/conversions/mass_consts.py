"""
Mass constants

Base unit: Gram
"""

from fractions import Fraction

# US customary (mass in g) (avoirdupois - avdp)
OZ = Fraction(28.349523125)  # ounce
GR = Fraction(2/875) * OZ    # grain (16/7000)
DR = Fraction(1/16) * OZ     # dram
LB = 16 * OZ                 # pound
CWT = 100 * 16 * OZ           # US hundredweight(=100 lb)
