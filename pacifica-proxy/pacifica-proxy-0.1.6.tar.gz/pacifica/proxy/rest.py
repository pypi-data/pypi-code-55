#!/usr/bin/python
# -*- coding: utf-8 -*-
"""CherryPy root object."""
import json
import cherrypy
from .files import Files


def error_page_default(**kwargs):
    """The default error page should always enforce json."""
    cherrypy.response.headers['Content-Type'] = 'application/json'
    return json.dumps({
        'status': kwargs['status'],
        'message': kwargs['message'],
        'traceback': kwargs['traceback'],
        'version': kwargs['version']
    })

# pylint: disable=too-few-public-methods


class Root:
    """
    CherryPy root object class.

    not exposed by default the base objects are exposed
    """

    exposed = True

    def __init__(self):
        """Create the local objects we need."""
        self.files = Files()

    @staticmethod
    @cherrypy.tools.json_out()
    # pylint: disable=invalid-name
    def GET():
        """Return happy message about functioning service."""
        return {'message': 'Pacifica Proxy Up and Running'}
    # pylint: enable=invalid-name
# pylint: enable=too-few-public-methods
