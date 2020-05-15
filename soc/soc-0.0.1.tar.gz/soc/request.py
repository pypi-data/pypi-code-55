from typing import Optional
from urllib.parse import parse_qs, urlsplit
import json


class Request(object):

    def __init__(self, websocket, full_path: str, data: str):
        self._websocket = websocket
        self._full_path: str = full_path
        self._data: str = data

        url_parts = urlsplit(full_path)
        self._path: str = url_parts.path
        self._query: str = url_parts.query

    @property
    def websocket(self):
        return self._websocket

    @property
    def full_path(self) -> str:
        return self._full_path

    @property
    def path(self) -> str:
        # Separate path from args and return path
        return self._path

    @property
    def data(self) -> str:
        return self._data

    @property
    def query(self) -> dict:
        return {k: v[0] for k, v in parse_qs(self._query).items()}

    @property
    def json(self) -> dict:
        return json.loads(self._data)

    def get_json(self) -> dict:
        return json.loads(self._data)


if __name__ == "__main__":

    r = Request(websocket="foo", full_path="/some/path", data='wawawa')

    print(r.json)