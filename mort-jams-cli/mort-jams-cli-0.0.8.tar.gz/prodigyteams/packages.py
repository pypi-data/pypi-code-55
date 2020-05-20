import requests
import typer

from .spinner import spinner
from .utils import (
    dicts_to_table,
    get_broker,
    printer,
    get_cached_packages,
    get_cached_binaries_for_package,
    get_packages,
    get_binaries_for_package,
)

app = typer.Typer()


def complete_package(incomplete: str):
    with spinner():
        packages = get_cached_packages()
    for element in packages:
        package_name: str = element["name"]
        if package_name.startswith(incomplete):
            yield (package_name, f"Package {package_name}")


def complete_package_filename(ctx: typer.Context, incomplete: str):
    package = ctx.params.get("package")
    if not package:
        return
    with spinner():
        binaries = get_cached_binaries_for_package(package)
    for element in binaries:
        filename: str = element["filename"]
        if filename.startswith(incomplete):
            yield (filename, "")


@app.callback()
def packages():
    """
    Sub-commands to interact with packages (including models).
    """


@app.command("list")
def list_(cache: bool = True):
    """
    List all the packages including built-ins.
    """
    if cache:
        data = get_cached_packages()
    else:
        data = get_packages()
    headers, rows = dicts_to_table(data)
    printer.table(rows, header=headers, divider=True, max_col=3000)


@app.command()
def add(package: typer.FileBinaryRead, allowoverwrite: bool = False):
    """
    Add a package from the local filesystem.

    It should be a valid file in your local file system,
    it will also be validated and indexed by your broker's Python Package Index.
    """
    broker = get_broker()
    typer.echo(f"Uploading package file {package.name}.")
    params = {"allowoverwrite": allowoverwrite}
    headers = {"Authorization": f"Bearer {broker.token}"}
    response = requests.post(
        f"{broker.address}/api/v1/models/upload",
        files={"file": package},
        params=params,
        headers=headers,
    )
    if response.status_code == 200:
        typer.echo("Package successfully added.")
    else:
        typer.echo(f"Status: {response.text}")


@app.command()
def list_package(
    package: str = typer.Argument(..., autocompletion=complete_package),
    cache: bool = True,
):
    """
    List all the binary files for a package.
    """
    if cache:
        data = get_cached_binaries_for_package(package)
    else:
        data = get_binaries_for_package(package)
    headers, rows = dicts_to_table(data)
    printer.table(rows, header=headers, divider=True, max_col=3000)


@app.command()
def download(
    *,
    package: str = typer.Argument(..., autocompletion=complete_package),
    filename: str = typer.Argument(..., autocompletion=complete_package_filename),
):
    """
    Download a package to the current directory.
    """
    with spinner():
        broker = get_broker()
        headers = {"Authorization": f"Bearer {broker.token}"}
        response = requests.get(
            f"{broker.address}/api/v1/packages/{package}/download/{filename}",
            headers=headers,
        )
    if response.status_code == 200:
        with open(filename, "wb") as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)
        typer.echo(f"Package file successfully downloaded to: {filename}")
    else:
        typer.echo(f"Status: {response.text}")


@app.command()
def delete(
    package: str = typer.Argument(..., autocompletion=complete_package),
    force: bool = typer.Option(False, help="Force deletion without confirmation"),
):
    """
    Delete a package.
    """
    if not force:
        typer.confirm(f"Are you sure you want to delete: {package}?", abort=True)
    broker = get_broker()
    headers = {"Authorization": f"Bearer {broker.token}"}
    response = requests.delete(
        f"{broker.address}/api/v1/packages/{package}", headers=headers
    )
    if response.status_code == 200:
        typer.echo("Package successfully deleted.")
    else:
        typer.echo(f"Status: {response.text}")
