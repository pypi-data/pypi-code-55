import requests
import logging


class Requester(object):
    _logger_marker = 'whoishistory-requester'

    def __init__(self, user_agent):
        """Initialise an instance of Requester with given api_key and user_agent string

            Keyword arguments:
            :param user_agent: user Agent header
        """

        self.user_agent = user_agent

        self.logger = logging.getLogger(self._logger_marker)

    def request(self, url, method: str = "GET", headers: dict = None, params: dict = None) -> requests.Response:
        """Perform a http(s) request for given parameters to given URL

            :param url: API url
            :param method: http method
            :param params: query parameters
            :param headers: query headers
        """

        if headers is None:
            headers = dict()

        if params is None:
            params = dict()

        headers.update({
            'Accept': 'application/json',
            'User-Agent': self.user_agent,
        })

        return requests.request(method, url, headers=headers, params=params)
