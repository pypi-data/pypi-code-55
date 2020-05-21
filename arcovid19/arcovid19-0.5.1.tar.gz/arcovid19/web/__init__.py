#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Bruno Sanchez, Vanessa Daza,
#                     Juan B Cabral, Marcelo Lares,
#                     Nadia Luczywo, Dante Paz, Rodrigo Quiroga,
#                     Martín de los Ríos, Federico Stasyszyn
#                     Cristian Giuppone.
# License: BSD-3-Clause
#   Full Text: https://raw.githubusercontent.com/ivco19/libs/master/LICENSE


# =============================================================================
# DOCS
# =============================================================================

"""This package contains the entire flask app logic to run a web server.

This file contain the get_app method, but you can access directly the
implementation of all the project with the blueprint
``arcovid19.web.bp.wavid19``.

"""


# =============================================================================
# IMPORTS
# =============================================================================

import os
import pathlib

import flask
from flask_babel import Babel

from . import bp


# =============================================================================
# CONSTANTS
# =============================================================================

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

DEBUG = os.environ.get("ARCOVID19_DEBUG", "true").lower() == "true"

TESTING = DEBUG

SECRET_KEY = os.environ.get("ARCOVID19_SECRET_KEY")

DEFAULT_LOCALE = os.environ.get("ARCOVID19_DEFAULT_LOCALE")

TRANSLATION_DIRECTORY = str(PATH / "translations")


# =============================================================================
# PUBLIC API
# =============================================================================

def create_app(**kwargs):
    """Retrieve a flask app for arcovid 19 using the internal blueprint.

    """
    kwargs.setdefault("DEBUG", DEBUG)
    kwargs.setdefault("TESTING", TESTING)
    kwargs.setdefault("SECRET_KEY", SECRET_KEY or os.urandom(16))

    kwargs.setdefault('BABEL_DEFAULT_LOCALE', DEFAULT_LOCALE)
    kwargs.setdefault('BABEL_TRANSLATION_DIRECTORIES', TRANSLATION_DIRECTORY)

    app = flask.Flask("arcovid19.web")
    app.register_blueprint(bp.wavid19)

    app.config.update(kwargs)

    babel = Babel(app)  # noqa

    # ========== RETURN
    return app
