#!/usr/bin/env python
# -*- coding: utf-8 -*-
from math import pi

"""Speed of light in m/s"""
c = 299792458

"""Standard Earth gravity in m/s²"""
g0 = 9.80665

"""Gravitational constant in m³/(kg.s²)"""
G = 6.6740831e-11

AU = 149597870700.0

DAYSEC = 86400.0

"""Arcseconds to radians"""
ARCSEC_TO_RAD = pi / (180.0 * 3600.0)

"""Milliarcseconds to radians"""
MILLI_ARCSEC_TO_RAD = ARCSEC_TO_RAD / 1000.

JULIAN_CENTURY = 36525.0

"""Offset between JD and MJD"""
JD_MJD = 2400000.5

"""Offset between JD and J2000"""
JD_J2000 = 2451545.0

"""Reference epoch (J2000.0), Modified Julian Date"""
MJD2000_MJD = 51544.5


TWO_PI = 2.0 * pi
