import json
from scripts.game_adt import GameList


if __name__ == '__main__':
    with open("../data/games.json") as f:
        game_json = json.load(f)
    game_list = GameList(game_json)
    game_list.score(['Adventure'], ['Fantasy'], ['Single player'], ['PC (Microsoft Windows)'], (1995, 2017), 17)
    print(game_list)
    fibb = game_list.loc("Final Fantasy VI")
    print(fibb.local_score, fibb.rating, fibb.age_floor, fibb.release_date, fibb.themes, fibb.genres, fibb.game_modes,
          fibb.platforms)
