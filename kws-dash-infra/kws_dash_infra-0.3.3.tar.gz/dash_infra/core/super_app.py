import json
from collections import defaultdict
from typing import Dict

import click

from flask import Blueprint, Flask, jsonify, render_template, request
from slugify import slugify
from werkzeug.middleware.dispatcher import DispatcherMiddleware


class KWSSuperApp:
    def __init__(
        self,
        dash_router: Dict[str, "KWSDashApp"],
        *args,
        name="Default Application",
        **kwargs,
    ):
        self.app = Flask(__name__, *args, **kwargs)
        self.name = name
        self.api = Blueprint("API", __name__, url_prefix="/api/")
        self.router = dash_router
        self.api_endpoints = defaultdict(dict)

        self.register_callbacks_as_api()

    def register_slug(self, name):
        slug = slugify(name)
        return f"/{slug}/"

    def register_callbacks_as_api(self):
        for app in self.router.values():
            for callback in app.callbacks:
                self.register_api(callback)

    def register_api(self, callback):
        if not hasattr(callback, "_json") or not callback.to_api:
            return

        slug = slugify(callback.func.__name__)
        route = self.register_slug(callback.func.__name__)

        def wrapped_function():
            payload = request.form or json.loads(request.json)
            result = callback.json(**payload)
            return jsonify(result), 200

        def wrapped_doc():
            doc = {"docstring": callback.func.__doc__}

            return jsonify(doc), 200

        wrapped_function.__name__ = f"{slug}_worker"
        wrapped_doc.__name__ = f"{slug}_doc"
        self.api.route(route, methods=("POST",))(wrapped_function)
        self.api.route(route, methods=("GET",))(wrapped_doc)
        self.api_endpoints[slugify(callback.name)] = callback.description

        return callback

    def create_app(self):
        import math

        def slice_array(array, length):
            return [
                array[i * length : (i * length) + length]
                for i in range(math.ceil(len(array) / length))
            ]

        self.app.register_blueprint(self.api)

        reshaped_endpoints = []
        for row in slice_array(list(self.api_endpoints.keys()), 3):
            reshaped_endpoints.append({n: self.api_endpoints[n] for n in row})

        @self.app.route("/endpoints/")
        def endpoints():
            return render_template("endpoints.html", endpoints=reshaped_endpoints,)

        @self.app.route("/")
        def index():

            return render_template(
                "index.html",
                name=self.name,
                router=self.router,
                endpoints=reshaped_endpoints,
            )

        for route, dash_app in self.router.items():
            dash_app.instanciate(
                server=self.app, routes_pathname_prefix=f"/{route}/",
            )
        return self.app

    @property
    def cli(self):
        @click.command()
        @click.option(
            "--name", "-n", required=True, type=click.Choice(self.router.keys())
        )
        @click.option("--debug", "-d", is_flag=True)
        def run_app(name, debug):
            app = self.router[name].instanciate()
            app.run_server(debug=debug)

        @click.command()
        @click.option("--debug", "-d", is_flag=True)
        def run(debug):
            app = self.create_app()
            app.run(debug=debug)

        return click.Group("run", {"run_app": run_app, "run": run})
