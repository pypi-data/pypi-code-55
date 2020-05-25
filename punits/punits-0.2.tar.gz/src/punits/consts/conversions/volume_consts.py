"""
Volume constants

Base unit: Litre
"""

from fractions import Fraction

# US liquid/fluid (volume in L) customary
# Note: US food labeling nutrition => oz = 30mL
FL_OZ = Fraction(0.0295735295625)  # ounce
GILL = 4 * FL_OZ                   # gill, teacup
CUP = 8 * FL_OZ                    # cup
PT = 16 * FL_OZ                    # pint
QT = 32 * FL_OZ                    # quart
GAL = 128 * FL_OZ                  # gallon
TBSP = Fraction(1/2) * FL_OZ       # tablespoon
TSP = Fraction(1/6) * FL_OZ        # teaspoon
FL_DR = Fraction(1/8) * FL_OZ      # fluid dram

# Imperial
IMP_FL_OZ = Fraction(0.0284130625)      # ounce
IMP_GILL = 5 * IMP_FL_OZ                # gill,teacup
IMP_CUP = 10 * IMP_FL_OZ                # cup
IMP_PT = 20 * IMP_FL_OZ                 # pint
IMP_QT = 40 * IMP_FL_OZ                 # quart
IMP_GAL = 160 * IMP_FL_OZ               # gallon
IMP_FL_DR = Fraction(1/8) * IMP_FL_OZ   # imperial fluid dram
