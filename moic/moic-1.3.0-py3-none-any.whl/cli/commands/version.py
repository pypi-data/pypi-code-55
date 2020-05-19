"""
Module which contains the version command for moic
"""
import click
import pkg_resources

from moic.cli import console, logger


@click.command()
def version():
    """
    Provide the current moic installed version
    """
    logger.debug("Execute 'version' command")
    console.print(f"Moic version: [green]{pkg_resources.get_distribution('moic').version}[/]")
