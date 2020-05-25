"""
Conversion data for all supported units
"""

from . import siprefix
from . import volume_consts
from . import mass_consts
from . import length_consts
from . import data_consts
from . import temperature_consts

_volume_conversions = {
    'oz': volume_consts.FL_OZ,    # Remove dots
    'gill': volume_consts.GILL,
    'cup': volume_consts.CUP,
    'pt': volume_consts.PT,
    'qt': volume_consts.QT,
    'gal': volume_consts.GAL,
    'tsp': volume_consts.TSP,
    'tbsp': volume_consts.TBSP,
    'dr': volume_consts.FL_DR,

    'imp oz': volume_consts.IMP_FL_OZ,
    'imp gill': volume_consts.IMP_GILL,
    'imp cup': volume_consts.IMP_CUP,
    'imp pt': volume_consts.IMP_PT,
    'imp qt': volume_consts.IMP_QT,
    'imp gal': volume_consts.IMP_GAL,
    'imp dr': volume_consts.IMP_FL_DR,

    'Yl': siprefix.YOTTA,
    'Zl': siprefix.ZETTA,
    'El': siprefix.EXA,
    'Pl': siprefix.PETA,
    'Tl': siprefix.TETRA,
    'Gl': siprefix.GIGA,
    'Ml': siprefix.MEGA,
    'kl': siprefix.KILO,
    'hl': siprefix.HECTO,
    'dal': siprefix.DECA,
    'l': siprefix.UNITY,
    'dl': siprefix.DECI,
    'cl': siprefix.CENTI,
    'ml': siprefix.MILLI,
    'ul': siprefix.MICRO,
    'nl': siprefix.NANO,
    'pl': siprefix.PICO,
    'fl': siprefix.FEMTO,
    'al': siprefix.ATTO,
    'zl': siprefix.ZEPTO,
    'yl': siprefix.YOCTO
}

_mass_conversions = {
    'oz': mass_consts.OZ,    # Remove dots
    'gr': mass_consts.GR,
    'dr': mass_consts.DR,
    'lb': mass_consts.LB,
    'cwt': mass_consts.CWT,

    'Yg': siprefix.YOTTA,
    'Zg': siprefix.ZETTA,
    'Eg': siprefix.EXA,
    'Pg': siprefix.PETA,
    'Tg': siprefix.TETRA,
    'Gg': siprefix.GIGA,
    'Mg': siprefix.MEGA,
    'kg': siprefix.KILO,
    'hg': siprefix.HECTO,
    'dag': siprefix.DECA,
    'g': siprefix.UNITY,
    'dg': siprefix.DECI,
    'cg': siprefix.CENTI,
    'mg': siprefix.MILLI,
    'ug': siprefix.MICRO,
    'ng': siprefix.NANO,
    'pg': siprefix.PICO,
    'fg': siprefix.FEMTO,
    'ag': siprefix.ATTO,
    'zg': siprefix.ZEPTO,
    'yg': siprefix.YOCTO,

    't': 1e3 * 1e3    # metric ton (ie, tonne = 1000kg)
}

_length_conversions = {
    'in': length_consts.IN,    # Remove dots
    'ft': length_consts.FT,
    'yd': length_consts.YD,
    'mi': length_consts.MI,
    'nmi': length_consts.NMI,

    'px': length_consts.PX,
    'pt': length_consts.PT,
    'pc': length_consts.PC,

    'Ym': siprefix.YOTTA,
    'Zm': siprefix.ZETTA,
    'Em': siprefix.EXA,
    'Pm': siprefix.PETA,
    'Tm': siprefix.TETRA,
    'Gm': siprefix.GIGA,
    'Mm': siprefix.MEGA,
    'km': siprefix.KILO,
    'hm': siprefix.HECTO,
    'dam': siprefix.DECA,
    'm': siprefix.UNITY,
    'dm': siprefix.DECI,
    'cm': siprefix.CENTI,
    'mm': siprefix.MILLI,
    'um': siprefix.MICRO,
    'nm': siprefix.NANO,
    'pm': siprefix.PICO,
    'fm': siprefix.FEMTO,
    'am': siprefix.ATTO,
    'zm': siprefix.ZEPTO,
    'ym': siprefix.YOCTO,
}

_data_conversions = {
    'YB': siprefix.YOTTA,
    'ZB': siprefix.ZETTA,
    'EB': siprefix.EXA,
    'PB': siprefix.PETA,
    'TB': siprefix.TETRA,
    'GB': siprefix.GIGA,
    'MB': siprefix.MEGA,
    'kB': siprefix.KILO,
    'B': siprefix.UNITY,

    'YiB': data_consts.YI,
    'ZiB': data_consts.ZI,
    'EiB': data_consts.EI,
    'PiB': data_consts.PI,
    'TiB': data_consts.TI,
    'GiB': data_consts.GI,
    'MiB': data_consts.MI,
    'KiB': data_consts.KI,

    'nibble': data_consts.NIBBLE,
    'b': data_consts.BIT,
}

_temperature_conversions = {
    'K': siprefix.UNITY,
    'C': temperature_consts.C,
    'F': temperature_consts.F,
    'Ro': temperature_consts.Ro,
    'Re': temperature_consts.Re,
    'De': temperature_consts.De,
    'Ra': temperature_consts.Ra,
    'N': temperature_consts.N,
}

CONVERSIONS = {
    'length': _length_conversions,
    'mass': _mass_conversions,
    'volume': _volume_conversions,
    'data': _data_conversions,
    'temperature': _temperature_conversions,
}

"""
Armstrong
"""
