#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click

from ce_cli.cli import cli
from ce_cli.version import __release__, __version__
"""
This module contains project version information.

.. currentmodule:: ce_cli.version
.. moduleauthor:: maiot GmbH <support@maiot.io>
"""


@cli.command()
def version():
    """Version of the Core Engine"""
    click.echo(click.style(r"""      
                     _       _      _____               ______             _
                    (_)     | |    / ____|             |  ____|           (_)
     _ __ ___   __ _ _  ___ | |_  | |     ___  _ __ ___| |__   _ __   __ _ _ _ __   ___
    | '_ ` _ \ / _` | |/ _ \| __| | |    / _ \| '__/ _ \  __| | '_ \ / _` | | '_ \ / _ \
    | | | | | | (_| | | (_) | |_  | |___| (_) | | |  __/ |____| | | | (_| | | | | |  __/
    |_| |_| |_|\__,_|_|\___/ \__|  \_____\___/|_|  \___|______|_| |_|\__, |_|_| |_|\___|
                                                                      __/ |
                                                                     |___/
         """, fg='green'))

    """Get the library version."""
    click.echo(click.style(f"version: {__version__}", bold=True))


if __name__ == '__main__':
    version()
