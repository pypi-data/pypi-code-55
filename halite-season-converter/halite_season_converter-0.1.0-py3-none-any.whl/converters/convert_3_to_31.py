"""
Converts a Halite 3 game into the 3.1 format.
"""

from collections import ChainMap
from copy import copy, deepcopy
from typing import List, Dict, Any, Iterator

from kaggle_environments import make

from halite_season_converter.schemas import Game_3, Game_31
from halite_season_converter.schemas.halite_3 import Move, Frame


def _configuration(game: Game_3, env) -> dict:
    return dict(
        episodeSteps=game.GAME_CONSTANTS.MAX_TURNS,
        agentExec=env.configuration.agentExec,
        agentTimeout=env.configuration.agentTimeout,
        actTimeout=env.configuration.actTimeout,
        runTimeout=env.configuration.runTimeout,
        halite=game.GAME_CONSTANTS.INITIAL_ENERGY,
        size=game.GAME_CONSTANTS.DEFAULT_MAP_HEIGHT,
        spawnCost=game.GAME_CONSTANTS.NEW_ENTITY_ENERGY_COST,
        convertCost=game.GAME_CONSTANTS.DROPOFF_COST,
        moveCost=game.GAME_CONSTANTS.MOVE_COST_RATIO,
        collectRate=game.GAME_CONSTANTS.EXTRACT_RATIO,
        regenRate=0,
    )


def _yield_halite_board(game: Game_3) -> Iterator[List[int]]:
    def flatten(grid):
        return [grid_cell.energy for row in grid for grid_cell in row]

    halite = deepcopy(game.production_map.grid)
    yield flatten(halite)

    for frame in game.full_frames:
        for cell in frame.cells:
            halite[cell.y][cell.x].energy = cell.production
        yield flatten(halite)


def _actions(moves: List[Move]) -> Dict[str, str]:
    def action(move):
        direction_map = {"n": "NORTH", "s": "SOUTH", "e": "EAST", "w": "WEST"}
        return {str(move.id): direction_map[move.direction]}

    return dict(
        ChainMap(
            *[
                action(move)
                for move in moves
                if move.type == "m" and move.direction != "o"
            ]
        )
    )


def _pos(size: int, x: int, y: int) -> int:
    return x + y * size


def _yield_shipyards(game: Game_3, player_id: int) -> Iterator[Dict[str, int]]:
    size = game.GAME_CONSTANTS.DEFAULT_MAP_HEIGHT
    first_shipyard = game.players[int(player_id)].factory_location
    shipyards = {
        f"{first_shipyard.x}-{first_shipyard.y}": _pos(
            size, first_shipyard.x, first_shipyard.y
        )
    }
    for frame in game.full_frames:
        for event in frame.events:
            if event.owner_id == int(player_id) and event.type == "construct":
                shipyards[f"{event.location.x}-{event.location.y}"] = _pos(
                    size, event.location.x, event.location.y
                )
        yield copy(shipyards)


def _yield_ships(game: Game_3, player_id: int) -> Iterator[Dict[str, List[int]]]:
    size = game.GAME_CONSTANTS.DEFAULT_MAP_HEIGHT
    for frame in game.full_frames:
        yield {
            key: [_pos(size, value.x, value.y), value.energy]
            for key, value in frame.entities.get(player_id, {}).items()
        }


def _yield_units(game: Game_3, player_id: int) -> Iterator[List[Dict[str, Any]]]:
    for shipyards, ships in zip(
        _yield_shipyards(game, player_id), _yield_ships(game, player_id),
    ):
        yield [shipyards, ships]


def _yield_player_halite(game: Game_3, player_id: int) -> Iterator[int]:
    for frame in game.full_frames:
        yield frame.energy[player_id]


def _yield_player(game: Game_3, player_id: int) -> Iterator[List[Any]]:
    for halite, units in zip(
        _yield_player_halite(game, player_id), _yield_units(game, player_id),
    ):
        yield [halite, *units]


def _observation(
    player_id: int, step: int, halite: List[int], players: List[List[Any]],
) -> Dict[str, Any]:
    if player_id == "0":
        return dict(player=int(player_id), step=step, halite=halite, players=players)
    return dict(player=int(player_id))


def _player_step(
    player_id: int, frame: Frame, step: int, halite: List[int], players: List[List[Any]]
) -> Dict[str, Any]:
    return dict(
        action=_actions(frame.moves.get(player_id, [])),
        reward=frame.energy[player_id],
        info={},
        observation=_observation(player_id, step, halite, players),
        status="ACTIVE",
    )


def _steps(game: Game_3) -> List[List[Dict[str, Any]]]:
    steps = []
    halite_generator = _yield_halite_board(game)
    players_generator = zip(
        *[
            _yield_player(game, str(player_id))
            for player_id in range(game.number_of_players)
        ]
    )

    for step, (halite, players, frame) in enumerate(
        zip(halite_generator, players_generator, game.full_frames)
    ):
        steps.append(
            [
                _player_step(str(player_id), frame, step, halite, players)
                for player_id in range(game.number_of_players)
            ]
        )

    return steps


def _game(game: Game_3) -> Game_31:
    env = make("halite")
    return Game_31.from_dict(
        dict(
            id="0",
            name=env.name,
            title=env.specification.title,
            description=env.specification.description,
            version=env.version,
            configuration=_configuration(game, env),
            specification=env.specification,
            steps=_steps(game),
            rewards=None,
            statuses=None,
            schema_version=env.toJSON()["schema_version"],
        )
    )


def convert(game: Game_3) -> Game_31:
    """
    Converts a Halite 3 game into the 3.1 format.
    """
    return _game(game)
