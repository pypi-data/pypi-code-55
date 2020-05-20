import typer

from .utils import dicts_to_table, get_fresh_identity_data, printer, state

app = typer.Typer()


@app.callback()
def projects():
    """
    Sub-commands to interact with projects.
    """


@app.command("list")
def list_():
    """
    List all the projects.
    """
    get_fresh_identity_data()
    if state.projects:
        headers, rows = dicts_to_table(state.projects)
        printer.table(rows, header=headers, divider=True, max_col=3000)
    else:
        typer.echo("No available projects")
