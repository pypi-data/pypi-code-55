"""This module contains all necessary definitions for worker subcommand."""

import os.path as path

import click

from ..exec.worker.app import Worker
from ..exec.worker.config import WorkerConfiguration
from ..utils.config import ConfigurationError, load_configuration
from . import utils

__HELP = """Starting Worker Component for AMNES.

            By default, the AMNES Worker will be started with the
            'worker.yml' configuration inside the base directory.
            If the config parameter is specified, its value will be used
            as the config file path, ignoring the base directory.

            Nevertheless, a valid base directory is needed as it is used
            as the parent directory for persistent storage.

            Default base directory: ~/.amnes
         """


@click.group(help="")
def group() -> None:
    """Command Group for Worker."""


@group.command(name="worker", help=__HELP)
@click.option(
    "--base", default="~/.amnes/", help="AMNES base directory.", envvar="AMNES_BASE"
)
@click.option("--config", default="", help="Worker configuration file.")
@click.option("--debug", default=False, is_flag=True, help="Enable debug log messages.")
def command(base: str, config: str, debug: bool) -> None:
    """Starting Worker Component for AMNES.

    Args:
        base (str): The path to the AMNES base directory.
        config (str): The path to the worker configuration file.
                      If None or an empty string is passed, the default config
                      path relative to the AMNES base directory is used.
        debug (bool): If debug messages should be logged.
    """
    if not base.endswith("/"):
        base = base + "/"
    if (not config) or (config.isspace()):
        config = base + "worker.yml"
    base = path.abspath(path.expanduser(base))
    config = path.abspath(path.expanduser(config))
    click.secho("AMNES Base Directory: " + base, fg="yellow")
    click.secho("AMNES Worker Configuration: " + config, fg="yellow")
    try:
        cfg = load_configuration(config, WorkerConfiguration)
    except ConfigurationError as cerr:
        click.secho(f"Could not load worker configuration: {cerr}", fg="red")
        utils.click_traceback(1)
    click.secho("Starting AMNES Worker, switching to dedicated logger ...", fg="green")
    app = Worker(cfg, base, debug)
    app.execute()
