import os

import typer

from .postgres import get_instance
from .tools import is_tool_exists
from remo_app.config import REMO_HOME


def check_runtime_requirements(db_params):
    if not db_params:
        typer.echo("Invalid database connection parameters.")
        raise typer.Exit()

    get_instance().on_start_check(db_params)

    # TODO: this needed only for Windows
    vips_bin_path = str(os.path.join(REMO_HOME, 'libs', 'vips', 'vips-dev-8.8', 'bin'))
    if os.path.exists(vips_bin_path) and vips_bin_path not in os.environ["PATH"]:
        os.environ["PATH"] = vips_bin_path + os.pathsep + os.environ["PATH"]

    vips = is_tool_exists('vips')
    if vips:
        return

    msg = 'Warning - Remo stopped as some requirements are missing:'
    if not vips:
        msg = """{}

vips library was not found.
Please do `python -m remo_app init` or install library manually.""".format(msg)

    typer.echo(msg)
    raise typer.Exit()


def check_installation_requirements():
    sqlite = is_tool_exists('sqlite3')
    if all((sqlite,)):
        return

    msg = 'Warning - Remo stopped as some requirements are missing:'

    if not sqlite:
        msg = """{}

SQLite binaries not installed.
You can install remo in a conda environment, which comes with SQLite pre-installed.
Or can install SQLite manually,
e.g. see instructions here https://www.sqlitetutorial.net/download-install-sqlite/""".format(msg)

    typer.echo(msg)
    raise typer.Exit()
