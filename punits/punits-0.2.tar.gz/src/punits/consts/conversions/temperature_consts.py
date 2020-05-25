"""
Temperature constants

Base unit: Kelvin
"""

from fractions import Fraction

# Temperature (in Kelvin) (K)
K = 1   # Kelvin
C = {"to": lambda x: x + 273.15, "from": lambda x: x - 273.15}  # Celsius
F = {   # Fahrenheit
    "to": lambda x: (x + 459.67) * Fraction(5 / 9),
    "from": lambda x: (x * Fraction(9 / 5)) - 459.67,
}
Ro = {  # Rømer
    "to": lambda x: (x - 7.5) * Fraction(40/21) + 273.15,
    "from": lambda x: (x - 273.15) * Fraction(21/40) + 7.5
}
Re = {  # Réaumur
    "to": lambda x: x * Fraction(5/4) + 273.15,
    "from": lambda x: (x - 273.15) * Fraction(4/5)
}
De = {  # Delisle
    "to": lambda x: 373.15 - (x * Fraction(2/3)),
    "from": lambda x: (373.15 - x) * Fraction(3/2)
}
Ra = {  # Rankine
    "to": lambda x: x * Fraction(5/9),
    "from": lambda x: x * Fraction(9/5)
}
N = {   # Newton
    "to": lambda x: (x * Fraction(100/33)) + 273.15,
    "from": lambda x: (x - 273.15) * Fraction(33/100)
}
