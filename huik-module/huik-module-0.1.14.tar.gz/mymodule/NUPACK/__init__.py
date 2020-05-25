"""
How to use NUPACK - Hui 5/8
from mymodule import mymodule as NPK

# To predict mfe structure:
# pseudo: pseudo knot , sodium and magnesium in M,
NPK.mfe(['GGGGATACCCC'],dangles='some',T=37,material='dna',pseudo=False,sodium=0.05,magnesium=0.005)
>>> [('(((....))).', '-2.685')]

"""
from ._NUPACK import *
