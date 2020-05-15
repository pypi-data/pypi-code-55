"""
This module provides a function to convert a Halite games to formats of different
seasons.
"""

from ..schemas import Game_2, Game_3, Game_31
from .convert_31_to_3 import convert as c_31_3
from .convert_3_to_31 import convert as c_3_31


_SEASON_CONVERTER_MAP = {
    (Game_3, Game_31): c_3_31,
    (Game_31, Game_3): c_31_3,
}


def convert(from_game, from_format, to_format):
    """
    Converts a game from its origin format to a new format.
    """
    converter = _SEASON_CONVERTER_MAP.get((from_format, to_format))
    if converter:
        return converter(from_game)
    raise NotImplementedError
