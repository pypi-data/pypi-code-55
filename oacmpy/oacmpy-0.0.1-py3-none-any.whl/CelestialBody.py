# -*- coding: utf-8 -*-
from numpy import sqrt

from .constants import G


class CelestialBody:
    def __init__(self, name, equatorial_radius, polar_radius, **kwargs):
        """

        :param name: Name of the celestial body
        :param equatorial_radius: Equatorial radius of the celestial body
        :param polar_radius: Polar radius of the celestial body
        :param kwargs:
        """
        self.name = name
        self.equatorial_radius = equatorial_radius
        """"""
        self.polar_radius = polar_radius
        flattening = 1 - polar_radius / equatorial_radius
        self.flattening = flattening

        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def eccentricity(self):
        """Eccentricity of the body
        """
        return sqrt(self.flattening * 2 - self.flattening ** 2)


"""Earth physical characteristics"""
Earth = CelestialBody(
    name="Earth",
    mass=5.97237e24,
    equatorial_radius=6378137.0,
    polar_radius=6356752.0
)

"""Moon physical characteristics"""
Moon = CelestialBody(name="Moon", equatorial_radius=1738100.0, polar_radius=1736000.0)

"""Mars physical characteristics"""
Mars = CelestialBody(name="Mars", equatorial_radius=3396200.0, polar_radius=3376200.0)
