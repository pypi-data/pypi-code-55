"""
Length constants

Base unit: Metre
"""

from fractions import Fraction

# Length (US) (in m)
IN = 0.0254            # inch
FT = 12 * IN           # feet
YD = 36 * IN           # yard
MI = 1760 * (36 * IN)  # mile = 1760 yards
NMI = 1852


# Web
# W3C CSS: 1in = 2.54cm = 25.4mm = 72pt = 6pc
# https://www.w3.org/Style/Examples/007/units.en.html
PT = Fraction(1/72) * IN  # 'point' in typography. For font size, etc.
PC = Fraction(1/6) * IN   # 'pica' in typography. For font size, etc.

# PX = 0.0254 when dpi=1
PX = {"to": lambda x, args: (x * IN) / args['dpi'],
      "from": lambda x, args: (x / IN) * args['dpi']}
