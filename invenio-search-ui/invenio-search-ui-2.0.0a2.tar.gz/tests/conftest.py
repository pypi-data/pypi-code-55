# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2020 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Pytest configuration."""

from __future__ import absolute_import, print_function

import os
import shutil
import tempfile

import jinja2
import pytest
from flask import Flask
from flask_babelex import Babel
from invenio_assets import InvenioAssets

from invenio_search_ui import InvenioSearchUI
from invenio_search_ui.views import blueprint


@pytest.yield_fixture()
def instance_path():
    """Temporary instance path."""
    path = tempfile.mkdtemp()
    yield path
    shutil.rmtree(path)


@pytest.fixture()
def app():
    """Flask application fixture."""
    app = Flask('testapp')
    app.config.update(
        TESTING=True,
        SEARCH_UI_SEARCH_API='api',
        BASE_TEMPLATE='invenio_search_ui/base.html',
        HEADER_TEMPLATE='invenio_search_ui/base_header.html',
    )
    Babel(app)
    InvenioAssets(app)
    InvenioSearchUI(app)

    @app.route('/api')
    def api():
        return {}

    app.register_blueprint(blueprint)
    # add extra test templates to the search app blueprint, to fake the
    # existence of `invenio-theme` base templates.
    test_templates_path = os.path.join(os.path.dirname(__file__), "templates")
    enhanced_jinja_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader(test_templates_path),
    ])
    # override default app jinja_loader to add the new path
    app.jinja_loader = enhanced_jinja_loader
    return app
