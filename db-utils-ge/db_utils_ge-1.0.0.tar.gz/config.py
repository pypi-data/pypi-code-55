#!/usr/bin/python
from configparser import ConfigParser
from typing import Dict


def get_config_from(filename: str = 'database_default.ini', section: str = 'postgresql') -> Dict:
    """Return a config dict from a given INI file and given section.
    If a param name starts with 'is_' -> set it as boolean.
    In any case the function will try to assign int to the value. If impossible (or <> float(x)), leave as str.

    Parameters
    ----------
    filename
        Input INI file held in the root.
    section
        Section of the INI file.

    Returns
    -------
    Dict
        Configuration dictionary {'param0': 'value0', 'param1': 'value1', ...}

    """
    # create a parser
    parser = ConfigParser(allow_no_value=True)
    # read config_ file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            try:
                if param[0].lower().startswith('is_'):
                    # Get it as boolean if param name starts with "is_".
                    db[param[0]] = parser.getboolean(section, param[0])
                else:
                    # Make it integer if possible.
                    if abs(int(param[1]) - float(param[1])) < 1e-5:
                        db[param[0]] = int(param[1])
            except (ValueError, TypeError):
                db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db
