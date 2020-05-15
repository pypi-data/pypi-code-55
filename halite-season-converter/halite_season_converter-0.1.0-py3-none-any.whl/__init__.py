"""
This module contains the base class for all games.
"""

import json

from dataclasses_json import DataClassJsonMixin
import zstd

from .schemas import Game_2, Game_3, Game_31
from .converters import convert


_SEASON_GAME_CLS_MAP = {
    "halite_2": Game_2,
    "halite_3": Game_3,
    "halite_31": Game_31,
}


class Converter:
    """
    Converter.
    """

    def __init__(self, game: DataClassJsonMixin):
        self.game = game

    @classmethod
    def _game_cls(cls, season: str):
        game_cls = _SEASON_GAME_CLS_MAP.get(season)
        if not game_cls:
            raise NotImplementedError(season)
        return game_cls

    @classmethod
    def from_hlt_file(cls, filename: str, season: str):
        """
        Reads a .hlt file and returns a Game object.
        """
        game_cls = cls._game_cls(season)
        with open(filename, mode="rb") as file_pointer:
            # pylint: disable=c-extension-no-member
            return cls(game_cls.from_json(zstd.loads(file_pointer.read())))
            # pylint: enable=c-extension-no-member

    def to_hlt_file(self, filename: str):
        """
        Writes the object into a .hlt file.
        """
        with open(filename, mode="wb") as file_pointer:
            # pylint: disable=c-extension-no-member
            file_pointer.write(zstd.dumps(self.game.to_json().encode("ascii")))
            # pylint: enable=c-extension-no-member

    @classmethod
    def from_json_file(cls, filename: str, season: str):
        """
        Reads a .json file and returns a Game object.
        """
        game_cls = cls._game_cls(season)
        with open(filename, mode="r") as file_pointer:
            return cls(game_cls.from_json(file_pointer.read()))

    def to_json_file(self, filename: str):
        """
        Writes the object into a .json file.
        """
        with open(filename, mode="w") as file_pointer:
            json.dump(self.game.to_dict(), file_pointer, indent=2, sort_keys=True)

    def convert(self, season: str):
        """
        Converts the game into the format of a different season.
        Returns a new object of class Converter.
        """
        game_cls = self._game_cls(season)
        game_converted = convert(self.game, self.game.__class__, game_cls)
        return type(self)(game_converted)
