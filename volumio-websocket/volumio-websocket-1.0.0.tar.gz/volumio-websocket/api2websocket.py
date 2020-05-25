"""Transforms any http api request to a websocket call."""

from .websocket import Websocket
from functools import wraps
from asyncio import sleep


def api2websocket(method, params, **kwargs):
    """Transform method and params from api to websocket calls."""
    if method == "commands":
        method = params["cmd"]

        if method in params:
            params = params[method]
        elif "value" in params:
            params = params["value"]
        elif "name" in params:
            params = params["name"]
        else:
            params = params["cmd"]

    if method == params:
        params = None

    return method, params, kwargs


def patch_api(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return f(api2websocket(args, kwargs))

    return wrapper


patch_api(Websocket.emit)


def request(host, port, method, params=None, path=None, max=2):
    """Handles api methods to make sync websocket requests."""

    state_name = Websocket.get_answer_name(method)
    socket = Websocket(host, port, path)
    socket.connect()

    sleeptimer = 0.1

    sleep(sleeptimer)
    socket.call(method, params)

    counter = 0

    while counter < max and socket.get(state_name) is None:
        sleep(sleeptimer)
        counter += sleeptimer

    socket.disconnect()

    return socket.get(state_name)
