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


async def request(host, port, method, params=None, path=None):
    """Handles api methods to make sync websocket requests."""

    ws = Websocket(host, port, path=path)
    await ws.connect()
    data = await ws.call(method, params)
    await ws.disconnect()

    return data
