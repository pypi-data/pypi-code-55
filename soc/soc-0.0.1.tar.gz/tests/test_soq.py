from soc import Soc, SocketView, Request

import pytest


test_host: str = "localhost"
test_port: int = 8675


@pytest.fixture
def app():
    return Soq()


def test_add_function_handler(app):

    def handler(request: Request):
        return "foo"

    app.add_route("/name", handler)


def test_add_socketview_handler(app):

    class MyHandler(SocketView):

        def handler(self, request: Request):
            return "foo"

    app.add_route("/socketview", MyHandler)


def test_app_route_decorator(app):

    app.route("/decorator")
    def decorator(request: Request):
        return "decorator"
