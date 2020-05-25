"""
Alternate names for all supported units
"""

from typing import Dict, List

_mass_labels: Dict[str, List[str]] = {
    # US customary
    'oz': ['ounce', 'ounces'],
    'gr': ['grain', 'grains'],
    'dr': ['dram', 'drams'],
    'lb': ['pound', 'pounds', 'lbs'],
    'cwt': ['hundredweight'],

    't': ['tonne', 'tonnes'],    # Same as Mg

    # SI
    'g': ['gram', 'grams'],
    'Yg': ['yottagram'],
    'Zg': ['zettagram'],
    'Eg': ['exagram'],
    'Pg': ['petagram'],
    'Tg': ['tetragram'],
    'Gg': ['gigagram'],
    'Mg': ['megagram'],
    'kg': ['kilogram'],
    'hg': ['hectogram'],
    'dag': ['decagram'],
    'dg': ['decigram'],
    'cg': ['centigram'],
    'mg': ['milligram'],
    'ug': ['microgram', 'μg'],
    'ng': ['nanogram'],
    'pg': ['picogram'],
    'fg': ['femtogram'],
    'ag': ['attogram'],
    'zg': ['zeptogram'],
    'yg': ['yoctogram'],
}

_volume_labels: Dict[str, List[str]] = {
    # US customary
    'oz': ['fluid ounce', 'ounce',
           'ounces', 'fl oz', 'oz fl'],    # Remove dots
    'gill': ['gill'],
    'cup': ['cup', 'cups'],
    'pt': ['pint'],
    'qt': ['quarter'],
    'gal': ['gallon', 'gallons'],
    'tsp': ['teaspoon'],
    'tbsp': ['tablespoon'],
    'dr': ['fluid dram', 'dram', 'drachm',
           'fluid drachm', 'fluidram', 'fluidrachm'],

    # Imperial
    'imp oz': ['imperial fluid ounce', 'imp_oz', 'imp fl oz', 'imp oz fl'],
    'imp gill': ['imperial gill', 'imp_gill'],
    'imp cup': ['imperial cup', 'imp_cup', 'imp cups'],
    'imp pt': ['imperial pint', 'imp_pt', 'imp pint'],
    'imp qt': ['imperial quarter', 'imp_qt', 'imp quarter'],
    'imp gal': ['imperial gallon', 'imp_gal',
                'imp gallon', 'imp gallons'],
    'imp dr': ['imperial fluid dram', 'imp_dr', 'imp dram',
               'imp drachm', 'imp fluid dram', 'imp fluid drachm',
               'imp fluidram', 'imp fluidrachm'],

    # SI
    'l': ['litre', 'litres'],
    'Yl': ['yottalitre'],
    'Zl': ['zettalitre'],
    'El': ['exalitre'],
    'Pl': ['petalitre'],
    'Tl': ['tetralitre'],
    'Gl': ['gigalitre'],
    'Ml': ['megalitre'],
    'kl': ['kilolitre'],
    'hl': ['hectolitre'],
    'dal': ['decalitre'],
    'dl': ['decilitre'],
    'cl': ['centilitre'],
    'ml': ['millilitre'],
    'ul': ['microlitre', 'μl'],
    'nl': ['nanolitre'],
    'pl': ['picolitre'],
    'fl': ['femtolitre'],
    'al': ['attolitre'],
    'zl': ['zeptolitre'],
    'yl': ['yoctolitre'],
}

_length_labels: Dict[str, List[str]] = {
    # US customary
    'in': ['inch', 'inches', '"'],
    'ft': ['feet', 'foot', "'"],
    'yd': ['yard', 'yards'],
    'mi': ['mile', 'miles'],
    'nmi': ['nautical mile', 'nautical miles'],

    # Web
    'px': ['pixel', 'pixels'],
    'pt': ['point', 'points'],
    'pc': ['pica', 'picas'],

    # SI
    'm': ['metre', 'metres',    # Commonwealth spelling
          'meter', 'meters'],   # US spelling
    'Ym': ['yottametre'],
    'Zm': ['zettametre'],
    'Em': ['exametre'],
    'Pm': ['petametre'],
    'Tm': ['tetrametre'],
    'Gm': ['gigametre'],
    'Mm': ['megametre'],
    'km': ['kilometre'],
    'hm': ['hectometre'],
    'dam': ['decametre'],
    'dm': ['decimetre'],
    'cm': ['centimetre'],
    'mm': ['millimetre'],
    'um': ['micrometre', 'μm'],
    'nm': ['nanometre'],
    'pm': ['picometre'],
    'fm': ['femtometre'],
    'am': ['attometre'],
    'zm': ['zeptometre'],
    'ym': ['yoctometre'],
}

_data_labels: Dict[str, List[str]] = {
    # Byte
    'B': ['byte', 'bytes'],
    'YB': ['yottabyte'],
    'ZB': ['zettabyte'],
    'EB': ['exabyte'],
    'PB': ['petabyte'],
    'TB': ['tetrabyte'],
    'GB': ['gigabyte'],
    'MB': ['megabyte'],
    'kB': ['kilobyte'],
    'YiB': ['yobibyte'],
    'ZiB': ['zebibyte'],
    'EiB': ['exbibyte'],
    'PiB': ['pebibyte'],
    'TiB': ['tebibyte'],
    'GiB': ['gibibyte'],
    'MiB': ['mebibyte'],
    'KiB': ['kebibyte'],

    'nibble': ['nibble'],

    # bit
    'b': ['bit', 'bits'],
    'Yb': ['yottabit'],
    'Zb': ['zettabit'],
    'Eb': ['exabit'],
    'Pb': ['petabit'],
    'Tb': ['tetrabit'],
    'Gb': ['gigabit'],
    'Mb': ['megabit'],
    'kb': ['kilobit'],
    'Yib': ['yobibit'],
    'Zib': ['zebibit'],
    'Eib': ['exbibit'],
    'Pib': ['pebibit'],
    'Tib': ['tebibit'],
    'Gib': ['gibibit'],
    'Mib': ['mebibit'],
    'Kib': ['kebibit'],
}

_temperature_labels: Dict[str, List[str]] = {
    'K': ['Kelvin', 'kelvin'],
    'C': ['Celsius', '°C', 'centigrade'],
    'F': ['Fahrenheit', '°F'],
    'N': ['Newton', 'N', '°N'],
    'Ro': ['Rømer', 'Rø', '°Rø', 'Ro',
           '°Ro', 'Romer'],  # 'R' is ignored to avoid conflict
    'Re': ['Réaumur', 'Ré', '°Re', '°r', 'r', 'Reaumur'],
    'De': ['Delisle', 'D', '°D', 'De', '°De'],
    'Ra': ['Rankine', '°Ra', 'Ra'],   # 'R' is ignored to avoid conflict
}

LABELS: Dict[str, Dict[str, List[str]]] = {
    'length': _length_labels,
    'mass': _mass_labels,
    'volume': _volume_labels,
    'data': _data_labels,
    'temperature': _temperature_labels,
}
