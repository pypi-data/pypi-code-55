"""
This module contains the schema for the Halite season 3.1 format.
"""
from typing import Dict, Union, List, Any, Optional
from dataclasses import dataclass, field

from dataclasses_json import DataClassJsonMixin


@dataclass
# pylint: disable=invalid-name
class Configuration:
    """
    Configuration.
    """

    episodeSteps: int = field()
    agentExec: str = field()
    agentTimeout: int = field()
    actTimeout: int = field()
    runTimeout: int = field()
    halite: int = field()
    size: int = field()
    spawnCost: int = field()
    convertCost: int = field()
    moveCost: float = field()
    collectRate: float = field()
    regenRate: float = field()


# pylint: enable=invalid-name


@dataclass
class Observation:
    """
    Observation.
    """

    player: int = field()
    step: Optional[int] = field(default=None)
    halite: Optional[List[float]] = field(default=None)
    players: Optional[List[List[Union[int, Dict[str, Union[int, List[int]]]]]]] = field(
        default=None
    )


@dataclass
class PlayerStep:
    """
    Player step.
    """

    info: Dict[Any, Any] = field()
    observation: Observation = field()
    status: str = field()
    reward: Optional[int] = field(default=None)
    action: Optional[Dict[str, str]] = field(default=None)


@dataclass
# pylint: disable=invalid-name
class Game_31(DataClassJsonMixin):
    """
    Game.
    """

    id: str = field()
    name: str = field()
    title: str = field()
    description: str = field()
    version: str = field()
    configuration: Configuration = field()
    specification: Dict[Any, Any] = field()
    steps: List[List[PlayerStep]] = field()
    rewards: List[int] = field()
    statuses: List[str] = field()
    schema_version: int = field()


# pylint: enable=invalid-name
