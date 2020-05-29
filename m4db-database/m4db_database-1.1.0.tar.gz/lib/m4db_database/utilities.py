r"""
A set of useful utility functions.

@file utilities.py
@author L. Nagy, W. Williams
"""

import re
import os

HEX_RE_STR = r'[0-9A-Fa-f]'

HEX_REGEX = re.compile(HEX_RE_STR)
UID_REGEX = re.compile(r"{hx:}{{8}}-{hx:}{{4}}-{hx:}{{4}}-{hx:}{{4}}-{hx:}{{12}}".format(hx=HEX_RE_STR))


def split_all(path):
    r"""
    Splits a path in to its constituent parts
    Args:
        path: the path to split.

    Returns:
        the parts of the path as a list.

    """
    all_parts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            all_parts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            all_parts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            all_parts.insert(0, parts[1])
    return all_parts


def uid_to_dir(unique_id):
    r"""
    Converts the input unique_id to a path.
    Args:
        unique_id: a unique id that will be split up in to pairs.

    Returns:
        a path version of unique_id.

    """
    if not UID_REGEX.match(unique_id):
        raise ValueError("'{}' is not a valid unique id".format(unique_id))

    # Remove all '-' characters
    path_str = unique_id.replace("-", "")
    path_spt = [path_str[i:i + 2] for i in range(0, len(path_str), 2)]
    return os.path.join(*path_spt)


def dir_to_uid(path_dir):
    r"""
    Convert a directory to a unique id. Note: this only works if the directory looks like
    (for example) '0f/86/b9/38/15/a3/4f/1e/99/b1/8f/2b/65/b3/7a/03' which would be converted to
    '0f86b938-15a3-4f1e-99b1-8f2b65b37a03'.
    Args:
        path_dir: the directory path to convert to t aunique id.

    Returns:
        the unique id associated with the input path.

    """
    path_spt = split_all(path_dir)
    return hex_pairs_to_uid(*path_spt)


def hex_pairs_to_uid(*pairs):
    r"""
    Converts a list of hexadecimal pairs to a unique_id.
    Args:
        *pairs: the hexadecimal pairs to convert to a unique id.

    Returns:
        a unique id.

    """
    lst_pairs = list(*pairs)
    if not len(lst_pairs) == 16:
        raise ValueError("Paris must have 16 hex pairs to form a valid unique id (length is {})".format(len(lst_pairs)))

    for pair in lst_pairs:
        if not HEX_REGEX.match(pair):
            raise ValueError("The pair '{}' is not a valid hexadecimal".format(pair))

    return '{}{}{}{}-{}{}-{}{}-{}{}-{}{}{}{}{}{}'.format(*lst_pairs)


def string_to_bool(str):
    r"""
    Function to convert boolean strings to Python boolean values.
    Args:
        str: the input string.

    Returns: the boolean version of str

    """
    if str.lower() in ["true", "t"]:
        return True
    elif str.lower() in ["false", "f"]:
        return False
    else:
        raise ValueError("Can't interpret '{}' as boolean".format(str))


