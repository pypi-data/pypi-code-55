import requests
import typer

from .utils import (
    dicts_to_table,
    get_broker,
    get_broker_meta,
    printer,
    get_cached_broker_meta,
)
from .spinner import spinner

app = typer.Typer()


def complete_source(incomplete: str):
    with spinner():
        meta = get_cached_broker_meta()
    for name, source in meta["sources"].items():
        if name.startswith(incomplete):
            yield (name, source["title"])


@app.callback()
def sources():
    """
    Sub-commands for sources.
    """


@app.command("list")
def list_(cache: bool = True):
    """
    List all the sources.
    """
    if cache:
        meta = get_cached_broker_meta()
    else:
        meta = get_broker_meta()
    headers, rows = dicts_to_table(meta["sources"].values())
    printer.table(rows, header=headers, divider=True, max_col=3000)


@app.command()
def add(source: typer.FileBinaryRead, allowoverwrite: bool = False):
    """
    Add a source from local filesystem.

    It should be a valid file in your local system,
    it will be uploaded to your cluster.
    """
    broker = get_broker()
    typer.echo(f"Uploading source file {source.name}.")
    params = {"allowoverwrite": allowoverwrite}
    headers = {"Authorization": f"Bearer {broker.token}"}
    response = requests.post(
        f"{broker.address}/api/v1/sources/upload",
        files={"file": source},
        params=params,
        headers=headers,
    )
    if response.status_code == 200:
        typer.echo("Source successfully added.")
    else:
        typer.echo(f"Status: {response.text}")


@app.command()
def delete(
    source: str = typer.Argument(..., autocompletion=complete_source),
    force: bool = typer.Option(False, help="Force deletion without confirmation"),
):
    """
    Delete a source.
    """
    if not force:
        typer.confirm(f"Are you sure you want to delete: {source}?", abort=True)
    broker = get_broker()
    headers = {"Authorization": f"Bearer {broker.token}"}
    response = requests.delete(
        f"{broker.address}/api/v1/sources/{source}", headers=headers
    )
    if response.status_code == 200:
        typer.echo("Source successfully deleted.")
    else:
        typer.echo(f"Status: {response.text}")
