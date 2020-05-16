from configparser import RawConfigParser


def parse_config(configfile):
    """
    Parses a configfile in to a ConfigParser object.

    Parameters
    ----------
    configfile : str
        The configfile to parse.

    Returns
    -------
    ConfigParser
        The parsed ConfigParser instance.
    """
    config = RawConfigParser(allow_no_value=True)
    config.optionxform = str
    config.read(configfile)
    return config
