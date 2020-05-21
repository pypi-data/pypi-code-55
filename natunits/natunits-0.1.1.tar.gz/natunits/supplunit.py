from .unit import *

# barn
add_subunits('b', 1e-28, 'm', 2, suffixes="afpnum ", namespace=__name__)
# parsec
add_subunits('pc', 3.085677581 * 10**16, 'm', suffixes=" kMG", namespace=__name__)
# Litter
add_subunits('L', 10**-3, 'm', 3, suffixes="um kM", namespace=__name__)

cm = Unit(1e-2, subunit='cm', m=1)
cc = Unit(1e-6, subunit='cc', m=3)

minute = Unit(60, subunit='minute', s=1)
hour = Unit(60 * 60, subunit='hour', s=1)
day = Unit(60 * 60 * 24, subunit='day', s=1)
year = Unit(60 * 60 * 24 * 365, subunit='year', s=1)

au = Unit(149597870700.0, subunit='au', m=1)
