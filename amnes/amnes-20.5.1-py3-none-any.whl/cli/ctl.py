"""This module contains all necessary definitions for ctl subcommand."""

import os.path as path
from contextlib import contextmanager
from typing import Iterator

import click
import Pyro5.api as Pyro5
import yaml
from Pyro5.errors import PyroError
from Pyro5.serializers import SerializerBase

from ..exec.app import AmnesRemoteException
from ..exec.controller.app import RemoteControllerManager
from ..utils.config import ConfigurationError, load_configuration
from . import utils
from .config import ControlCommandConfiguration

__HELP = """Running an AMNES Control Command.

            By default, the AMNES Control Command invocation will use the
            'ctl.yml' configuration inside the base directory.
            If the config parameter is specified, its value will be used
            as the config file path, ignoring the base directory.

            Nevertheless, a valid base directory is needed as it is used
            as the parent directory for persistent storage.

            Default base directory: ~/.amnes
         """


@click.group(help="")
def group() -> None:
    """Command Group for CTL."""


@group.group(name="ctl", help=__HELP)
@click.option(
    "--base", default="~/.amnes/", help="AMNES base directory.", envvar="AMNES_BASE"
)
@click.option("--config", default="", help="Control command configuration file.")
@click.pass_context
def command(ctx: click.Context, base: str, config: str) -> None:
    """AMNES CTL.

    Args:
        ctx (Context): Click context.
        base (str): The path to the AMNES base directory.
        config (str): The path to the control command configuration file.
                      If None or an empty string is passed, the default config
                      path relative to the AMNES base directory is used.
    """
    if not base.endswith("/"):
        base = base + "/"
    if (not config) or (config.isspace()):
        config = base + "ctl.yml"
    base = path.abspath(path.expanduser(base))
    config = path.abspath(path.expanduser(config))
    click.secho("AMNES Base Directory: " + base, fg="yellow")
    click.secho("AMNES CTL Configuration: " + config, fg="yellow")
    try:
        cfg: ControlCommandConfiguration = load_configuration(
            config, ControlCommandConfiguration
        )
    except ConfigurationError as cerr:
        click.secho(f"Could not load command control configuration: {cerr}", fg="red")
        utils.click_traceback(1)
    click.secho(
        "Executing AMNES Control Command for "
        + f"'{cfg.ctl.controller_address}:{cfg.ctl.controller_port}' ...",
        fg="green",
    )
    SerializerBase.register_dict_to_class(
        f"{AmnesRemoteException.__module__}.{AmnesRemoteException.__name__}",
        AmnesRemoteException.deserialize,
    )
    try:
        remote: RemoteControllerManager = Pyro5.Proxy(
            f"PYRO:{RemoteControllerManager.PYROID}"
            + f"@{cfg.ctl.controller_address}:{cfg.ctl.controller_port}"
        )
    except PyroError as perr:
        click.secho(f"Connection setup failed: {perr}", fg="red")
        utils.click_traceback(1)
    ctx.obj = remote


@command.command(name="import", help="Import AMNES Project into AMNES Controller.")
@click.argument("config", type=click.File("rt"))
@click.pass_context
def action_import(ctx: click.Context, config: click.File) -> None:
    """Import AMNES Project into AMNES Controller.

    Args:
        ctx (Context): Click context.
        config (click.File): Project configuration file which should be imported.
    """
    remote: RemoteControllerManager = ctx.obj
    with __connection_handling():
        try:
            yamldict = yaml.safe_load(config)  # type: ignore
        except yaml.YAMLError as yerr:
            click.secho(f"Could not load YAML file: {yerr}", fg="red")
            utils.click_traceback(1)
        remote.import_project(yamldict)


@command.command(
    name="start", help="Start AMNES Project execution on AMNES Controller."
)
@click.argument("project")
@click.pass_context
def action_start(ctx: click.Context, project: str) -> None:
    """Start AMNES Project execution on AMNES Controller.

    Args:
        ctx (Context): Click context.
        project (str): Slug of imported project which should be started.
    """
    remote: RemoteControllerManager = ctx.obj
    with __connection_handling():
        remote.start_project(project)


@command.command(name="stop", help="Stop AMNES Project execution on AMNES Controller.")
@click.pass_context
def action_stop(ctx: click.Context) -> None:
    """Stop AMNES Project execution on AMNES Controller.

    Args:
        ctx (Context): Click context.
    """
    remote: RemoteControllerManager = ctx.obj
    with __connection_handling():
        remote.stop_project()


@command.command(name="shutdown", help="Shutdown linked AMNES Controller.")
@click.confirmation_option(
    prompt="Are you sure you want to SHUTDOWN your AMNES Controller?",
)
@click.pass_context
def action_shutdown(ctx: click.Context) -> None:
    """Shutdown linked AMNES Controller.

    Args:
        ctx (Context): Click context.
    """
    remote: RemoteControllerManager = ctx.obj
    click.secho("Sending SHUTDOWN to AMNES Controller!", fg="green")
    remote.shutdown()


@command.command(name="kill", help="Kill linked AMNES Controller.")
@click.confirmation_option(
    prompt="Are you sure you want to KILL your AMNES Controller?",
)
@click.pass_context
def action_kill(ctx: click.Context) -> None:
    """Kill linked AMNES Controller.

    Args:
        ctx (Context): Click context.
    """
    remote: RemoteControllerManager = ctx.obj
    click.secho("Sending KILL to AMNES Controller!", fg="green")
    remote.kill()


@contextmanager
def __connection_handling() -> Iterator[None]:
    """Handle connection error on remote command execution.

    Yields:
        None: No yield value available.
    """
    try:
        yield
    except ConnectionError as cerr:
        click.secho(f"Could not execute command: {cerr}", fg="bright_red")
    except PyroError as perr:
        click.secho(f"Execution failed: {perr}", fg="red")
        utils.click_traceback(1)
    except AmnesRemoteException as amnesexc:
        click.secho(f"Exception occurred on controller: {amnesexc}", fg="red")
        utils.click_traceback(1)
