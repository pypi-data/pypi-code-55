import re

import numpy as np

from . import units


def _decode_kvn(line):
    key_value = line.split("=")
    key = key_value[0].strip()
    value = key_value[1].strip()

    # check if there are units "[unit]"
    out = re.search("([\\-\\+\\d.]*)\\s *\\[(.*)\\]", value)
    if out:
        groups = out.groups()
        value = float(groups[0]) * units.units_dict[groups[1]]
    return key, value


def _decode_xml_value_element(element, key, default_unit):
    value = element.find(key)
    return _decode_xml_value(value, default_unit)


def _decode_xml_value(value, default_unit):
    text = value.text
    unit = value.attrib.get("units", default_unit)
    if unit is None:
        return text
    unit = units.units_dict[unit]
    return float(text) * unit


def _parse_covariance(data_dict, cov_keys):
    covariance = [[0.0] * 6] * 6
    covariance = np.array(covariance)
    for row in range(0, 6):
        for col in range(0, row + 1):
            key = cov_keys[row][col]
            covariance[row][col] = float(data_dict[key])
            covariance[col][row] = covariance[row][col]
    return covariance
