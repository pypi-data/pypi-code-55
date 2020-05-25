"""
punits
"""

from typing import List, Optional
from fractions import Fraction

from punits.consts import LABELS, CONVERSIONS


def find_unit_code(measure: str,
                   unit_name: str) -> str:
    """
    Finds unit code for further processing

    Raises UnknownUnitException if the unit is unknown
    """
    unit_name = unit_name.replace(".", "")
    for label in LABELS[measure]:
        if (unit_name == label) or (unit_name in LABELS[measure][label]):
            # if label == 'NO_SHORT_CODE':
            #    return unit_name
            return label
    raise ValueError(f"Gee.. I don't know about '{unit_name}'..")


def to_from_base(measure: str,
                 unit_code: str,
                 to_from: str,
                 value: float,
                 params: dict) -> float:
    """
    measure: The type of units being converted
    unit_code: Code of unit
    to_from: Value of "to" indicates whether conversion
    is to take place from specified unit to base unit.
    Otherwise conversion is done from base unit to given
    unit.
     - "to": convert to base
     - "from": convert from base
    value: Value to be converted
    params: Any special parameters that will be needed
    for conversion. Like dpi for conversion involving
    pixels

    Converts a unit to or from the base unit of the
    unit's measure.

    Returns equivalent base unit value when to_from is
    "to" and equivalent unit value otherwise.
    """
    result: float
    conv = CONVERSIONS[measure][unit_code]
    if isinstance(conv, (int, float, Fraction)):
        # Linear units
        if to_from == 'to':
            # Convert to base unit
            result = value * conv
        else:
            # Convert from base unit
            result = value / conv
    else:
        # Non-linear units
        if params:
            result = conv[to_from](value, params)
        else:
            result = conv[to_from](value)
    return result


def punits(measure: str,
           src_unit: str,
           target_unit: str,
           values: List[float],
           params: Optional[dict] = None) -> List[float]:
    """
    measure: The type of units being converted
    src_unit: code of unit from which conversion
    is to take place
    target_unit: code of unit to which conversion
    is to take place
    values: List of values to be converted
    params: Any special parameters that will be needed
    for conversion. Like dpi for conversion involving
    pixels

    Returns converted values as a list
    """
    if params is None:
        params = {}

    results = []

    if ('dpi' not in params
            and (src_unit == 'px' or target_unit == 'px')):
        raise ValueError("Missing parameter: dpi")

    for value in values:
        base_value = to_from_base(measure, src_unit, "to", value, params)
        target_value = to_from_base(measure, target_unit,
                                    "from", base_value, params)
        results.append(target_value)
    return results


def get_factor(measure: str,
               src_unit_code: str,
               target_unit_code: str) -> Optional[float]:
    """
    src_unit: code of unit from which conversion is to take place
    target_unit: code of unit to which conversion is to take place
    conv_dict: CONVERSIONS[measure]

    Returns the factor of source unit by which target unit grows
    if source-target unit pair has a linear relationship, otherwise
    None is returned.

    To be used when --verbose option is used.
    """
    if(isinstance(CONVERSIONS[measure][src_unit_code], (int, float, Fraction))
       and isinstance(CONVERSIONS[measure][target_unit_code],
                      (int, float, Fraction))):
        target_factor = CONVERSIONS[measure][target_unit_code]
        src_factor = CONVERSIONS[measure][src_unit_code]
        factor = target_factor / src_factor
        return factor
    return None
