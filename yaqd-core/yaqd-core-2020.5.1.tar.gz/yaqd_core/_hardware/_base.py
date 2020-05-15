#! /usr/bin/env python3

__all__ = ["Hardware"]

import math
import pathlib
from typing import Dict, Any, Union, Optional

from ..__version__ import __branch__
from .._daemon import Base


class Hardware(Base):
    traits = ["has-position"]
    _kind = "hardware"
    _version: Optional[str] = "1.0.0" + f"+{__branch__}" if __branch__ else ""

    def __init__(
        self, name: str, config: Dict[str, Any], config_filepath: pathlib.Path
    ):
        self._units = None
        super().__init__(name, config, config_filepath)

    def get_position(self) -> float:
        return self._position

    def get_units(self) -> Union[str, None]:
        return self._units

    def get_destination(self) -> float:
        return self._destination

    def set_position(self, position: float) -> None:
        self._busy = True
        self._destination = position
        self._set_position(position)

    def _set_position(self, position: float) -> None:
        self._position = position
        self._busy = False

    def set_relative(self, distance: float) -> float:
        new = self._destination + distance
        self.set_position(new)
        return new

    def get_state(self) -> Dict[str, Any]:
        return {"position": self._position, "destination": self._destination}

    def _load_state(self, state: Dict[str, Any]) -> None:
        self._position = state.get("position", math.nan)
        self._destination = state.get("destination", math.nan)


if __name__ == "__main__":
    Hardware.main()
