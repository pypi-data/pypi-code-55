"""Console script for anthill."""
import sys
import click
import yaml
import json

from .src.cli.core import Commands


@click.group()
def main():
    """
    Orchastrate. Build. Run.
    """
    pass

@main.command()
@click.argument('nest', type=click.File('r'))
def build(nest):
    """
    Build anthill using the yml file provided
    """
    click.echo("***************************** Ants building your anthill, hold tight ! *****************************")
    _nest = json.dumps(yaml.safe_load(nest))
    # while True:
    #         chunk = nest.read(1024)
    #         if not chunk:
    #             break
    #         _nest.append(chunk)
    Commands(nest=_nest)
    click.echo("***************************** Anthill built successfully ! *****************************")
    return 0

if __name__ == "__main__":
    main()  # pragma: no cover
