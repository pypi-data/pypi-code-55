# -*- coding: utf-8 -*-
""" glimmer package.

"""

from flask import Flask

from glimmer.container import Container
from glimmer.gateways.flask import FlaskGateway


class Glimmer(Container):

    def __init__(self, content_path: str, default_language: str = "en", app=None, gateway_token=None):
        super().__init__(content_path, default_language)
        self.gateway = None
        if app is not None:
            self.initialize_app_gateway(app, gateway_token)

    def initialize_app_gateway(self, app, gateway_token: str = None):
        if isinstance(app, Flask):
            self.gateway = FlaskGateway(app, self, gateway_token)
            with app.app_context():
                # add the glimmer object the app's request context
                app.app_ctx_globals_class.glimmer = self
        else:
            raise TypeError("Provided app class '{}' is not supported.".format(type(app)))
