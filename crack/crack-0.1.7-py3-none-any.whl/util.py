# -*- coding: utf-8 -*-
# @author: leesoar

import copy


__all__ = ["partition", "b64encode", "b64decode"]


def partition(array, size):
    """Equal parts array

    Args:
        array: pending array
        size: list size after split
    """
    array_is_str = False
    if type(array) == str:
        array_is_str = True
        tmp_array = list(array)
    else:
        tmp_array = copy.deepcopy(array)

    for i in range(0, len(tmp_array), size):
        if array_is_str:
            yield ''.join(tmp_array[i: i + size])
        else:
            yield tmp_array[i: i + size]


def b64encode(byte_str: bytes, b64_map="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"):
    """Base64 encode

    Support custom mapping.

    Args:
        byte_str: byte string
        b64_map: default base64 mapping
    Returns:
        string for base64
    """
    bit_str = ''.join(map(lambda x: bin(x).lstrip("0b").zfill(8), byte_str))
    bit_str += (6 - (len(bit_str) % 6 or 6)) * "0"
    pos = [int(x, base=2) for x in partition(bit_str, size=6)]
    return ''.join([b64_map[i] for i in pos]) + "=" * (3 - (len(byte_str) % 3 or 3))


def b64decode(b64_str: str, b64_map="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"):
    """Base64 decode

    Support custom mapping.

    Args:
        b64_str: base64 string
        b64_map: default base64 mapping
    Returns:
        byte string
    """
    nil_count = b64_str.count("=")
    filled_zero_count = (len(b64_str) - nil_count) * 6 % 8
    bit_str = "".join(map(lambda x: bin(x).lstrip("0b").zfill(6),
                          (map(b64_map.find, b64_str[:-nil_count or None]))))[:-filled_zero_count or None]
    return bytes([int(x, base=2) for x in partition(bit_str, size=8)])
