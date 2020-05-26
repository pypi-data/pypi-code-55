import math
import re


def normalize_angle(angle):
    """
    Normalize an angle value in degrees.
    :param angle: an angle value, in degrees
    :return: an angle between 0 included and 360 excluded
    """
    while angle < 0:
        angle = angle + 360
    while angle >= 360:
        angle = angle - 360
    return angle


def cos(deg: float):
    """
    Returns the cosinus of angle in degrees
    :param deg: an angle, in degrees
    :return: a cosine, between 0 and 1
    """
    return math.cos(math.radians(deg))


def sin(deg: float):
    """
    Returns the sinus of an angle in degrees
    :param deg: an angle, in degrees
    :return: a sine, between 0 and 1
    """
    return math.sin(math.radians(deg))


def tan(deg: float):
    """
    Returns the arc tangent of an angle in degrees
    :param deg: an angle, in degrees
    :return: an arc tangent
    """
    return math.tan(math.radians(deg))


def camel_to_snake(name):
    """
    Transform a CamelCase name (like Python class names) into
    a snake_case name (like OpenSCAD object names).
    :param name: a name in CamelCase
    :return: a name in snake_case
    """
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()
