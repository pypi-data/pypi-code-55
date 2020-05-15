"""
This module contains the schema for the Halite season 3 format.
"""

from typing import Dict, Union, List, Any, Optional
from dataclasses import dataclass, field

from dataclasses_json import DataClassJsonMixin


@dataclass
# pylint: disable=invalid-name
class _GameConstants(DataClassJsonMixin):
    """
    Game constants.
    """

    CAPTURE_ENABLED: bool = field()
    CAPTURE_RADIUS: int = field()
    DEFAULT_MAP_HEIGHT: int = field()
    DEFAULT_MAP_WIDTH: int = field()
    DROPOFF_COST: int = field()
    DROPOFF_PENALTY_RATIO: int = field()
    EXTRACT_RATIO: int = field()
    FACTOR_EXP_1: float = field()
    FACTOR_EXP_2: float = field()
    INITIAL_ENERGY: int = field()
    INSPIRATION_ENABLED: bool = field()
    INSPIRATION_RADIUS: int = field()
    INSPIRATION_SHIP_COUNT: int = field()
    INSPIRED_BONUS_MULTIPLIER: float = field()
    INSPIRED_EXTRACT_RATIO: int = field()
    MAX_CELL_PRODUCTION: int = field()
    MAX_ENERGY: int = field()
    MAX_PLAYERS: int = field()
    MAX_TURNS: int = field()
    MAX_TURN_THRESHOLD: int = field()
    MIN_CELL_PRODUCTION: int = field()
    MIN_TURNS: int = field()
    MIN_TURN_THRESHOLD: int = field()
    MOVE_COST_RATIO: float = field()
    NEW_ENTITY_ENERGY_COST: int = field()
    PERSISTENCE: float = field()
    SHIPS_ABOVE_FOR_CAPTURE: int = field()
    STRICT_ERRORS: bool = field()


# pylint: enable=invalid-name


@dataclass
class _Entity(DataClassJsonMixin):
    """
    Entity.
    """

    energy: int = field()
    is_inspired: bool = field()
    x: int = field()
    y: int = field()


@dataclass
# pylint: disable=invalid-name
class Move(DataClassJsonMixin):
    """
    Move.
    """

    type: str = field()
    direction: Optional[str] = field(default=None)
    id: Optional[int] = field(default=None)


# pylint: enable=invalid-name


@dataclass
class _Location(DataClassJsonMixin):
    """
    Location.
    """

    x: int = field()
    y: int = field()


@dataclass
class _FrameCell(_Location):
    """
    Frame cell.
    """

    production: int = field()


@dataclass
# pylint: disable=invalid-name
class _Event(DataClassJsonMixin):
    """
    Event.
    """

    location: _Location = field()
    type: str = field()
    id: Optional[int] = field(default=None)
    energy: Optional[int] = field(default=None)
    owner_id: Optional[int] = field(default=None)


# pylint: enable=invalid-name


@dataclass
class Frame(DataClassJsonMixin):
    """
    Frame.
    """

    cells: List[_FrameCell] = field()
    deposited: Dict[str, int] = field()
    energy: Dict[str, int] = field()
    entities: Dict[str, Dict[str, _Entity]] = field()
    events: List[_Event] = field()
    moves: Dict[str, List[Move]] = field()


@dataclass
class _PlayerStatistics(DataClassJsonMixin):
    """
    _Player statistics.
    """

    all_collisions: int = field()
    average_entity_distance: int = field()
    final_production: int = field()
    halite_per_dropoff: List[Union[Dict[str, int], int]]
    interaction_opportunities: int = field()
    last_turn_alive: int = field()
    max_entity_distance: int = field()
    mining_efficiency: float = field()
    number_dropoffs: int = field()
    player_id: int = field()
    random_id: int = field()
    rank: int = field()
    self_collisions: int = field()
    ships_captured: int = field()
    ships_given: int = field()
    total_bonus: int = field()
    total_mined: int = field()
    total_mined_from_captured: int = field()
    total_production: int = field()


@dataclass
class _GameStatistics(DataClassJsonMixin):
    """
    Game statistics.
    """

    number_turns: int = field()
    player_statistics: List[_PlayerStatistics] = field()


@dataclass
class _Player(DataClassJsonMixin):
    """
    Player.
    """

    energy: int = field()
    entities: List[Any] = field()
    factory_location: _Location = field()
    name: str = field()
    player_id: int = field()


@dataclass
class _GridCell(DataClassJsonMixin):
    """
    Grid cell.
    """

    energy: int = field()


@dataclass
class _ProductionMap(DataClassJsonMixin):
    """
    Production map.
    """

    grid: List[List[_GridCell]] = field()
    height: int = field()
    width: int = field()


@dataclass
# pylint: disable=invalid-name
class Game_3(DataClassJsonMixin):
    """
    Game.
    """

    ENGINE_VERSION: str = field()
    GAME_CONSTANTS: _GameConstants = field()
    REPLAY_FILE_VERSION: int = field()
    full_frames: List[Frame] = field()
    game_statistics: _GameStatistics = field()
    map_generator_seed: int = field()
    number_of_players: int = field()
    players: List[_Player] = field()
    production_map: _ProductionMap = field()


# pylint: enable=invalid-name
