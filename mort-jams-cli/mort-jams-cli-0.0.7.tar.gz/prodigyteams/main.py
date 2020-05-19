from typing import Optional

import typer

from . import cluster, packages, projects, sources, tasks
from .about import __version__
from .utils import get_fresh_api_token, get_fresh_id_token, printer, set_cli_host

cli = typer.Typer()
cli.add_typer(cluster.app, name="cluster")
cli.add_typer(sources.app, name="sources")
cli.add_typer(packages.app, name="packages")
cli.add_typer(projects.app, name="projects")
cli.add_typer(tasks.app, name="tasks")


def print_version(ctx: typer.Context, param, value: bool) -> None:
    if not value or ctx.resilient_parsing:
        return
    typer.echo(f"Prodigy Teams CLI version: {__version__}")
    raise typer.Exit()


@cli.callback()
def callback(version: bool = typer.Option(False, "--version", help="Print version and exit.", callback=print_version)):  # type: ignore
    """
    Prodigy Teams Command Line Interface.

    More info at https://prodi.gy/
    """


@cli.command()
def login(env: Optional[str] = None):
    """
    Login to your Prodigy Teams account.

    You normally don't need to call this manually.
    It will automatically authenticate when needed.
    """
    if env is not None:
        printer.info(f"Setting login environment to: {env}")
        set_cli_host(env)
    get_fresh_id_token()
    get_fresh_api_token()
    printer.good(f"Auth tokens successfully saved.")


if __name__ == "__main__":
    cli()
