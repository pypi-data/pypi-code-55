# SPDX-License-Identifer: MPL-2.0
# Copyright © 2020 Andreas Stenberg
from typing import Tuple


def levenshtein_distance(str1: str, str2: str) -> int:
    """
    Based on https://en.wikipedia.org/wiki/Levenshtein_distance this function
    calculates how many operations are required to modify str1 into str2. In
    conjunction with other methods it can be used to check for string similarity.
    This is helpfull when finding an open ended reference by a typo or the likes.

    :param str1:
    :param str2:
    :return: The number of operations needed to convert str1 into str2
    """
    d = [[0 for _ in range(len(str2))] for _ in range(len(str1))]

    for i, _ in enumerate(str1):
        d[i][0] = i
    for j, _ in enumerate(str2):
        d[0][j] = j

    for j, c2 in enumerate(str2):
        for i, c1 in enumerate(str1):
            substitution_cost = 0 if c1 == c2 else 1

            deletion = d[i - 1][j] + 1
            insertion = d[i][j - 1] + 1
            substitution = d[i - 1][j - 1] + substitution_cost

            d[i][j] = min(deletion, insertion, substitution)
    return d[len(str1) - 1][len(str2) - 1]


def similarity(str1: str, str2: str) -> float:
    """
    Calculates a similarity coefficient for two strings.
    :param str1:
    :param str2:
    :return: Similarity coefficient for the two strings
    """
    return 1 - (levenshtein_distance(str1, str2) / max(len(str1), len(str2)))


def most_similar(search_string: str, *strings: Tuple[str, ...]) -> str:
    """

    :param search_string:
    :param strings:
    :return: The most similar string in strings to search_string
    """
    return max(strings, key=lambda x: similarity(search_string, x))
