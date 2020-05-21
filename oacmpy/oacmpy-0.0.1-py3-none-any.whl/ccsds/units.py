from math import pi

# Distance
m = 1.0
km = 1000.0

day = 86400
percent = 100.0

# dictionnary for conversion to SI units
units_dict = {
    "m": 1,
    "m**2": 1,
    "km": km,
    "km/s": km,
    "m/s": 1,
    "m/s**2": 1,
    "m**2/s": 1,
    "m**2/s**2": 1,
    "m**2/s**3": 1,
    "m**2/s**4": 1,
    "s": 1,
    "d": day,
    "deg": pi / 180.0,
    "deg/s": pi / 180.0,
    "rev/day": 2 * pi / day,
    "rev/day**2": 1,
    "rev/day**3": 1,
    "1/ER": 1,
    "km**3/s**2": km ** 3,
    "kg": 1,
    "m**2/kg": 1,
    "m**3/kg": 1,
    "m**3/(kg*s)": 1,
    "m**3/(kg*s**2)": 1,
    "W/kg": 1,
    "%": percent,
}


def unit_convert(value, unit, unit_out):
    """Conversion between units. Does NOT check the physical consistency"""
    return value * units_dict[unit_out] / units_dict[unit]
