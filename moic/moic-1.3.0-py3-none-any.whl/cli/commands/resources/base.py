"""
Module for base Moic resources commands
"""
import click

from moic.cli import console, global_settings, logger
from moic.cli.utils import get_plugin_command


# List Commands
# TODO: Add autocomplete on all commands
@click.group()
def resources():
    """List projects, issue_types, priorities, status"""
    logger.debug("Execute 'resources' command")
    if not global_settings.get("current_context"):
        console.print("[yellow]No context defined yet[/yellow]")
        console.print("[grey]> Please run '[bold]moic context add[/bold]' to setup configuration[/grey]")
        console.line()
        exit(0)


@resources.command()
def projects():
    """
    List projects
    """
    logger.debug("Execute 'resources projects' command")
    get_plugin_command("resources", "projects")()


@resources.command()
def issue_type():
    """
    List issue types
    """
    logger.debug("Execute 'resources issue-type' command")
    get_plugin_command("resources", "issue_type")()


@resources.command()
def priorities():
    """
    List priorities
    """
    logger.debug("Execute 'resources priorities' command")
    get_plugin_command("resources", "priorities")()


@resources.command()
def status():
    """
    List status
    """
    logger.debug("Execute 'resources status' command")
    get_plugin_command("resources", "status")()
