import requests
import json


class IGDBAPI:
    """A micro-shell for the IGDB API service."""

    def __init__(self, api_key):
        """
        Initializes the API object with a key.
        :param api_key: str
        """
        self.base_url = "https://api-v3.igdb.com"
        self.header = {"user-key": api_key}

    def get_games(self, fields, conditions):
        """
        Queries the API for a JSON with a list of games.
        Fields specify the information that is going to be returned.
        Conditions put limitations on how and what information is going to be returned,
        i.e. "sort popularity desc" sorts the games by popularity in descending order.
        :param fields: list
        :param conditions: list
        :return: list
        """
        return self.get_json("/games", fields, conditions)

    def get_themes(self, fields, conditions):
        """
        Queries the API for a JSON with a list of themes.
        Fields specify the information that is going to be returned.
        Conditions put limitations on how and what information is going to be returned,
        i.e. "limit 20" limits the amount of themes returned to 20.
        :param fields: list
        :param conditions: list
        :return: list
        """
        return self.get_json("/themes", fields, conditions)

    def get_genres(self, fields, conditions):
        """
        Queries the API for a JSON with a list of genres.
        Fields specify the information that is going to be returned.
        Conditions put limitations on how and what information is going to be returned,
        i.e. "limit 20" limits the amount of genres returned to 20.
        :param fields: list
        :param conditions: list
        :return: list
        """
        return self.get_json("/genres", fields, conditions)

    def get_game_modes(self, fields, conditions):
        """
        Queries the API for a JSON with a list of game modes.
        Fields specify the information that is going to be returned.
        Conditions put limitations on how and what information is going to be returned,
        i.e. "limit 20" limits the amount of game modes returned to 20.
        :param fields: list
        :param conditions: list
        :return: list
        """
        return self.get_json("/game_modes", fields, conditions)

    def get_platforms(self, fields, conditions):
        """
        Queries the API for a JSON with a list of platforms.
        Fields specify the information that is going to be returned.
        Conditions put limitations on how and what information is going to be returned,
        i.e. "limit 20" limits the amount of platforms returned to 20.
        :param fields: list
        :param conditions: list
        :return: list
        """
        return self.get_json("/platforms", fields, conditions)

    def get_age_ratings(self, fields, conditions):
        """
        Queries the API for a JSON with a list of age ratings.
        Fields specify the information that is going to be returned.
        Conditions put limitations on how and what information is going to be returned,
        i.e. "limit 20" limits the amount of age ratings returned to 20.
        :param fields: list
        :param conditions: list
        :return: list
        """
        return self.get_json("/age_ratings", fields, conditions)

    def get_involved_companies(self, fields, conditions):
        """
        Queries the API for a JSON with a involved companies of them.
        Fields specify the information that is going to be returned.
        Conditions put limitations on how and what information is going to be returned,
        i.e. "limit 20" limits the amount of involved companies returned to 20.
        :param fields: list
        :param conditions: list
        :return: list
        """
        return self.get_json("/involved_companies", fields, conditions)

    def get_companies(self, fields, conditions):
        """
        Queries the API for a JSON with a list of companies.
        Fields specify the information that is going to be returned.
        Conditions put limitations on how and what information is going to be returned,
        i.e. "limit 20" limits the amount of companies returned to 20.
        :param fields: list
        :param conditions: list
        :return: list
        """
        return self.get_json("/companies", fields, conditions)

    def get_cover(self, fields, conditions):
        """
        Queries the API for a JSON with a game cover.
        Fields specify the information that is going to be returned.
        Conditions put limitations on how and what information is going to be returned,
        i.e. "where id=1234" will return only the cover with the id of 1234.
        :param fields: list
        :param conditions: list
        :return: list
        """
        return self.get_json("/covers", fields, conditions)

    def get_json(self, endpoint, fields, conditions):
        """
        Queries the API for a JSON with information.
        Endpoint is the endpoint to which the query should go.
        Fields specify the information that is going to be returned.
        Conditions put limitations on how and what information is going to be returned,
        they are different for each endpoint.
        :param endpoint: str
        :param fields: list
        :param conditions: list
        :return: list
        """
        game_url = self.base_url + endpoint
        r = requests.post(game_url,
                          data="fields " + ', '.join(fields) + "; " + '; '.join(conditions) + ";",
                          headers=self.header)
        return r.json()

    def get_status(self):
        """
        Returns the status of the API for the given user key.
        This is used to check how much queries out of 50,000 do I have left.
        :return: list
        """
        url = self.base_url + "/api_status"
        r = requests.get(url, headers=self.header)
        return r.json()

    @staticmethod
    def dump_json(obj, filename):
        """
        Dumps a list or dictionary which obeys the JSON rules
        into a .json file.
        This is used for dumping the lists returned by "get_" methods
        of this class into files.
        :param obj: (list, dict)
        :param filename: str
        :return: None
        """
        with open(filename, mode="w") as f:
            json.dump(obj, f)
