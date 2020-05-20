from data import constants, small_info
import numpy as np


class Game:
    """Object for a game from the data/games.json database"""

    def __init__(self, game_dct):
        """
        Initializes the Game object with some parameters.
        The input must be a game type dictionary returned by the IGDB API.
        :param game_dct:
        """
        # Individual attributes
        self.name = game_dct["name"]
        self.id = game_dct["id"]
        self.summary = game_dct["summary"]
        self.age_floor = game_dct["age_ratings"]
        self.rating = game_dct["aggregated_rating"]
        self.release_date = game_dct["first_release_date"]
        self.slug = game_dct["slug"]
        self.cover = "static/" + self.slug + ".jpg"

        # Lists of attributes
        self.genres = set(game_dct["genres"])
        self.themes = set(game_dct["themes"])
        self.game_modes = set(game_dct["game_modes"])
        self.platforms = set(game_dct["platforms"])
        self.companies = game_dct["involved_companies"]

        # Score for the current user's recommendation, None by default
        self.local_score = None

    def __str__(self):
        """
        Returns the name of the game.
        :return: str
        """
        return self.name

    def score(self, genres, themes, game_modes, platform_families, year_range, age):
        """
        Scores the game based on the parameters given by a user.
        :param genres: list
        :param themes: list
        :param game_modes: list
        :param platform_families: list
        :param year_range: tuple
        :param age: int
        :return: None
        """
        # Don't allow any games that have an age rating higher than user's age.
        if self.age_floor != "Rating Pending" and age < self.age_floor:
            return

        # Initialize a score.
        score = 0

        # Include the game's rating, multiplied by a certain factor.
        score += constants.rating_factor * self.rating

        # The closer to the given year range the game's release is, the more points.
        time_score = 35
        year = int(self.release_date.split('.')[2])

        # Consider all three positions of the game's release year
        # in regard to the year range
        if year < year_range[0]:
            time_score -= year_range[0] - year
        elif year > year_range[1]:
            time_score -= year - year_range[1]
        else:
            pass

        # Multiply the time score by a scaling constant, then add it to the total score.
        time_score *= constants.time_factor

        # Now onto the groups of game preferences.

        # Starting with platforms.------------------------------------------------------------
        platform_score = 0

        # First revert platform families back to all platforms.
        platforms = []
        for family in platform_families:
            plt = small_info.platform_families[family]
            platforms.extend(plt)

        # Default platform score is the amount of user's preferred platforms.
        platform_score += len(platforms)

        # Process platform differences of the game and the user's preference.
        platforms = set(platforms)
        combined_platforms = platforms.intersection(self.platforms)
        diff = len(platforms) - len(combined_platforms)
        platform_score -= diff

        # Add to total score
        score += platform_score * constants.platform_factor

        # Onto themes.----------------------------------------------------------------------
        theme_score = 0

        # Default theme score is the amount of user's preferred theme.
        theme_score += len(themes)

        # Process platform differences of the game and the user's preference.
        themes = set(themes)
        combined_themes = themes.intersection(self.themes)
        diff = len(themes) - len(combined_themes)
        theme_score -= diff

        # Add to total score
        score += theme_score * constants.theme_factor

        # Then genres.-----------------------------------------------------------
        genre_score = 0

        # Default platform score is the amount of user's preferred platforms.
        genre_score += len(genres)

        # Process platform differences of the game and the user's preference.
        genres = set(genres)
        combined_genres = genres.intersection(self.genres)
        diff = len(genres) - len(combined_genres)
        genre_score -= diff

        # Add to total score
        score += genre_score * constants.genre_factor

        # Finally, game modes.--------------------------------------------------
        game_mode_score = 0

        # Default platform score is the amount of user's preferred platforms.
        game_mode_score += len(game_modes)

        # Process platform differences of the game and the user's preference.
        game_modes = set(game_modes)
        combined_game_modes = game_modes.intersection(self.game_modes)
        diff = len(game_modes) - len(combined_game_modes)
        game_mode_score -= diff

        # Add to total score
        score += game_mode_score * constants.game_mode_factor

        # Finally, set the self.score to the resulting score.
        self.local_score = score


class GameList:
    """ADT for a container of games from the data/games.json database"""

    def __init__(self, game_lst):
        """
        Initializes a GameList object with a tuple of games,
        which are the Game class objects from this module.
        :param game_lst: list
        """
        if isinstance(game_lst[0], Game):
            self.games = game_lst
        else:
            self.games = list(map(lambda game: Game(game), game_lst))
        self.ids = (game.id for game in self.games)
        self.length = len(self.games)

    def __len__(self):
        return self.length

    def __getitem__(self, idx):
        """
        Implements the bracket notation to the GameList ADT.
        :return: Game
        """
        if 0 <= idx <= len(self) - 1:
            return self.games[idx]
        else:
            raise IndexError("Index must be between 0 and length of container")

    def __iter__(self):
        """
        Part of the iterator protocol.
        This, together with __next__, allow a user to iterate over the GameList.
        """
        self.n = 0
        return self

    def __next__(self):
        """
        Part of the iterator protocol.
        This, together with __iter__, allow a user to iterate over the GameList.
        """
        if self.n < len(self):
            result = self[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration

    def iloc(self, game_id):
        """
        Returns a Game object based on its id.
        :param game_id: int
        :return: Game
        """
        return list(filter(lambda game: game.id == game_id, self.games))[0]

    def loc(self, game_name):
        """
        Returns a Game object based on its name.
        :param game_name: str
        :return: Game
        """
        return list(filter(lambda game: game.name == game_name, self.games))[0]

    def score(self, genres, themes, game_modes, platform_families, year_range, age):
        """
        Scores all games in the GameList based on the parameters given by a user.
        Then changes the list to only include the Top 50 games.
        :param genres: list
        :param themes: list
        :param game_modes: list
        :param platform_families: list
        :param year_range: tuple
        :param age: int
        :return: list
        """
        for game in self:
            game.score(genres, themes, game_modes, platform_families, year_range, age)
        self.games = list(filter(lambda x: x.local_score is not None, self.games))
        self.games.sort(key=lambda x: x.local_score, reverse=True)
        self.games = self.games[:30]

        probs = [game.local_score for game in self.games]
        sum_probs = sum(probs)
        probs = list(map(lambda x: x / sum_probs, probs))
        probs[-1] = 1 - sum(probs[:-1])

        new_games = np.random.choice(self.games, size=5, replace=False, p=probs)
        return GameList(new_games)

    def __str__(self):
        """
        Returns a tuple-like representation of all the game names in the GameList.
        :return: str
        """
        return str(tuple(map(str, self.games)))
