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

"""Command line interfaces to access different Argentina-Related databases of
COVID-19 data from the Arcovid19 group.

"""

__all__ = ["main", "cases", "webserver"]


# =============================================================================
# IMPORTS
# =============================================================================

import sys

from .cases import load_cases, CASES_URL
from . import web


# =============================================================================
# CONSTANTS
# =============================================================================

DESCRIPTION = __doc__

FOOTNOTES = """This software is under the BSD 3-Clause License.
Copyright (c) 2020, IATE COVID-19 Task Force.
For bug reporting or other instructions please check:
https://github.com/ivco19/libs"""


# =============================================================================
# MAIN_
# =============================================================================

def cases(*, url=CASES_URL, force=False, out=None):
    """Retrieve and store the cases database in CSV format.

    url: str
        The url for the excel table to parse. Default is ivco19 team table.

    out: PATH (default=stdout)
        The output path to the CSV file. If it's not provided the
        data is printed in the stdout.

    force:
        If you want to ignore the local cache or retrieve a new value.

    """
    cases = load_cases(cases_url=url, force=force)
    if out is not None:
        cases.to_csv(out)
    else:
        cases.to_csv(sys.stdout)


def webserver(
    *,
    host=None, port=None, nodebug=False,
    reload=False, load_dotenv=True
):
    """Run a development server for arcovid19 utilities.

    host: str
        the hostname to listen on. Set this to '0.0.0.0' to
        have the server available externally as well. Defaults to
        '127.0.0.1' or the host in the SERVER_NAME config variable
        if present.

    port: int
        the port of the webserver. Defaults to 5000 or the
        port defined in the SERVER_NAME config variable if present.

    nodebug: bool
        if given, disable debug mode.

    reload: bool
        If its True any change of the code will restart the webserver.

    load_dotenv:
        Load the nearest '.env' and '.flaskenv'
        files to set environment variables. Will also change the working
        directory to the directory containing the first file found.

    """
    app = web.create_app()
    app.run(
        host=host, port=port,
        use_reloader=True,
        debug=(not nodebug),
        load_dotenv=load_dotenv)


def main():
    """Run the arcovid19 command line interface."""
    from clize import run

    run(
        cases, webserver,
        description=DESCRIPTION, footnotes=FOOTNOTES)
