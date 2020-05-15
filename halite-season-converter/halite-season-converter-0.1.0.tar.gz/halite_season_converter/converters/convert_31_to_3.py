"""
Converts a Halite 3.1 game into the 3 format.
"""
from typing import Any, List, Dict, Iterator, Tuple, Optional

from halite_season_converter.schemas import Game_3, Game_31
from halite_season_converter.schemas.halite_31 import Observation
from halite_season_converter import utils


def _yield_player_rewards(game: Game_31, player_id: int) -> Iterator[Optional[int]]:
    for step in game.steps:
        yield step[player_id].reward


def _player_ltar(rewards: Iterator[Optional[int]]) -> Tuple[Optional[int]]:
    """
    LTAR = Last Turn Alive and Reward.
    """
    step, reward = None, None
    for step, reward in enumerate(rewards):
        if reward is None:
            return step - 1, reward
    return step, reward


def _is_loss(ltar_1: Tuple[Optional[int]], ltar_2: Tuple[Optional[int]]) -> bool:
    lta_1, r_1 = ltar_1
    lta_2, r_2 = ltar_2

    r_1 = -1 if r_1 is None else r_1
    r_2 = -1 if r_2 is None else r_2

    if (lta_1 < lta_2) or (r_1 < r_2):
        return True
    return False


def _player_rank(ltar: Tuple[Optional[int]], ltars: List[Tuple[Optional[int]]]) -> int:
    return sum([_is_loss(ltar, ltar_2) for ltar_2 in ltars]) + 1


def _rank(game: Game_31) -> List[int]:
    num_players = len(game.steps[0])
    ltars = [
        _player_ltar(_yield_player_rewards(game, player_id))
        for player_id in range(num_players)
    ]
    return [_player_rank(ltar, ltars) for ltar in ltars]


def _last_turn_alive(game: Game_31) -> List[int]:
    num_players = len(game.steps[0])
    return [
        _player_ltar(_yield_player_rewards(game, player_id))[0]
        for player_id in range(num_players)
    ]


def _final_production(game: Game_31) -> List[int]:
    return [player[0] for player in game.steps[-1][0].observation.players]


def _number_dropoffs(game: Game_31) -> List[int]:
    ltas = _last_turn_alive(game)
    number_dropoffs_func = lambda lta, player_id: len(
        game.steps[lta][0].observation.players[player_id][1]
    )
    return [number_dropoffs_func(lta, player_id) for player_id, lta in enumerate(ltas)]


def _game_constants(game: Game_31) -> Dict[str, Any]:
    return dict(
        CAPTURE_ENABLED=False,
        CAPTURE_RADIUS=3,
        DEFAULT_MAP_HEIGHT=game.configuration.size,
        DEFAULT_MAP_WIDTH=game.configuration.size,
        DROPOFF_COST=game.configuration.convertCost,
        DROPOFF_PENALTY_RATIO=4,
        EXTRACT_RATIO=1 / game.configuration.collectRate,
        FACTOR_EXP_1=2.0,
        FACTOR_EXP_2=2.0,
        INITIAL_ENERGY=5000,
        INSPIRATION_ENABLED=False,
        INSPIRATION_RADIUS=4,
        INSPIRATION_SHIP_COUNT=2,
        INSPIRED_BONUS_MULTIPLIER=2.0,
        INSPIRED_EXTRACT_RATIO=1 / game.configuration.collectRate,
        MAX_CELL_PRODUCTION=1_000_000,
        MAX_ENERGY=1_000_000,
        MAX_PLAYERS=4,
        MAX_TURNS=game.configuration.episodeSteps,
        MAX_TURN_THRESHOLD=64,
        MIN_CELL_PRODUCTION=0,
        MIN_TURNS=0,
        MIN_TURN_THRESHOLD=32,
        MOVE_COST_RATIO=1 / game.configuration.moveCost,
        NEW_ENTITY_ENERGY_COST=game.configuration.spawnCost,
        PERSISTENCE=0.7,
        SHIPS_ABOVE_FOR_CAPTURE=3,
        STRICT_ERRORS=False,
    )


def _yield_observation(game_to_observe: Game_31) -> Iterator[Observation]:
    # Yield first observation twice because observation referes to state after
    # actions in same step are applied.
    yield game_to_observe.steps[0][0].observation
    for step in game_to_observe.steps:
        yield step[0].observation


def _yield_halite(game_to_observe: Game_31) -> Iterator[List[float]]:
    for observation in _yield_observation(game_to_observe):
        yield observation.halite


def _pos_to_xy(size: int, pos: int) -> Tuple[int]:
    return pos % size, pos // size


def _yield_cells(game_to_observe: Game_31) -> Iterator[List[Dict[str, Any]]]:
    size = game_to_observe.configuration.size
    old_halite = game_to_observe.steps[0][0].observation.halite
    for new_halite in _yield_halite(game_to_observe):
        cells = []
        for pos, (old_production, new_production) in enumerate(
            zip(old_halite, new_halite)
        ):
            if old_production != new_production:
                x, y = _pos_to_xy(size, pos)
                cells.append(dict(x=x, y=y, production=new_production))
        yield cells
        old_halite = new_halite


def _yield_energy(game_to_observe: Game_31) -> Iterator[Dict[str, float]]:
    for observation in _yield_observation(game_to_observe):
        yield {
            str(player_id): player[0]
            for player_id, player in enumerate(observation.players)
        }


def _yield_entities(game_to_observe: Game_31) -> Iterator[Dict[str, Dict[str, Any]]]:
    size = game_to_observe.configuration.size
    for observation in _yield_observation(game_to_observe):
        entities = {}
        for player_id, player in enumerate(observation.players):
            player_entities = {}
            for key, value in player[2].items():
                x, y = _pos_to_xy(size, value[0])
                player_entities[key] = dict(
                    energy=value[1], x=x, y=y, is_inspired=False
                )
            entities[str(player_id)] = player_entities
        yield entities


def _yield_moves(game: Game_31) -> Iterator[Dict[str, List[Dict[str, str]]]]:
    def _move(key: str, value: str) -> Dict[str, str]:
        if value in ("NORTH", "SOUTH", "EAST", "WEST"):
            return dict(type="m", direction=value.lower()[0], id=key)
        if value == "SPAWN":
            return dict(type="g", direction=None, id=None)
        if value == "CONVERT":
            return dict(type="c", direction=None, id=key)
        if value == "NOOP":
            return dict(type="m", direction="o", id=key)
        raise NotImplementedError(value)

    for step in game.steps:
        moves = {}
        players = step[0].observation.players
        for player_id, player in enumerate(step):
            action = player.action or {}
            player_moves = [_move(key, value) for key, value in action.items()]
            ships = players[player_id][2]
            for key, _ in ships.items():
                if key not in action.keys():
                    player_moves.append(_move(key, "NOOP"))
            moves[str(player_id)] = player_moves
        yield moves


def _yield_events(game: Game_31) -> Iterator[Dict[str, Any]]:
    entities_generator = _yield_entities(game)
    moves_generator = _yield_moves(game)

    for entities, moves in zip(entities_generator, moves_generator):
        events = []
        for player_id, player_moves in moves.items():
            for move in player_moves:
                if move["type"] == "c":
                    ship = entities[player_id][move["id"]]
                    events.append(
                        dict(
                            location=dict(x=ship["x"], y=ship["y"]),
                            type="construct",
                            id=move["id"],
                            energy=None,
                            owner_id=player_id,
                        )
                    )
        yield events


def _full_frames(game: Game_31) -> List[Dict[str, Any]]:
    cells_generator = _yield_cells(game)
    energy_generator = _yield_energy(game)
    entities_generator = _yield_entities(game)
    moves_generator = _yield_moves(game)
    event_generator = _yield_events(game)

    full_frames = []
    for cells, energy, entities, moves, events in zip(
        cells_generator,
        energy_generator,
        entities_generator,
        moves_generator,
        event_generator,
    ):
        full_frames.append(
            dict(
                cells=cells,
                deposited={},
                energy=energy,
                entities=entities,
                events=events,
                moves=moves,
            )
        )
    return full_frames


def _player_statistics(game: Game_31, player_id: int) -> Dict[str, Any]:
    return dict(
        all_collisions=0,
        average_entity_distance=0,
        final_production=_final_production(game)[player_id],
        halite_per_dropoff={},
        interaction_opportunities=0,
        last_turn_alive=_last_turn_alive(game)[player_id],
        max_entity_distance=0,
        mining_efficiency=0,
        number_dropoffs=_number_dropoffs(game)[player_id],
        player_id=player_id,
        random_id=0,
        rank=_rank(game)[player_id],
        self_collisions=0,
        ships_captured=0,
        ships_given=0,
        total_bonus=0,
        total_mined=0,
        total_mined_from_captured=0,
        total_production=0,
    )


def _game_statistics(game: Game_31) -> Dict[str, Any]:
    n_players = len(game.steps[0][0].observation.players)
    return dict(
        number_turns=len(game.steps),
        player_statistics=[
            _player_statistics(game, player_id) for player_id in range(n_players)
        ],
    )


def _production_map(game: Game_31) -> Dict[str, int]:
    size = game.configuration.size
    grid_cells = [dict(energy=energy) for energy in game.steps[0][0].observation.halite]
    grid = list(utils.chunks(grid_cells, size))
    return dict(grid=grid, height=size, width=size)


def _player(player: List[Any], player_id: int, name: str = None) -> Dict[str, Any]:
    name = name or f"player {player_id}"
    return dict(
        energy=player[0],
        entities=[],
        factory_location=None,
        name=name,
        player_id=player_id,
    )


def _players(game: Game_31) -> List[Dict[str, Any]]:
    players = []
    for player_id, player in enumerate(game.steps[0][0].observation.players):
        players.append(_player(player, player_id))
    return players


def _game(game: Game_31) -> Game_3:
    n_players = len(game.steps[0][0].observation.players)
    return Game_3.from_dict(
        dict(
            ENGINE_VERSION="3.1.0",
            GAME_CONSTANTS=_game_constants(game),
            REPLAY_FILE_VERSION=3,
            full_frames=_full_frames(game),
            game_statistics=_game_statistics(game),
            map_generator_seed=0,
            number_of_players=n_players,
            players=_players(game),
            production_map=_production_map(game),
        )
    )


def convert(game: Game_31) -> Game_3:
    """
    Converts a Halite 3.1 game into the 3 format.
    """
    return _game(game)
