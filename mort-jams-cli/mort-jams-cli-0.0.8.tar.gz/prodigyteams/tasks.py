import typer

from .utils import dicts_to_table, get_fresh_identity_data, printer, state

app = typer.Typer()


@app.callback()
def tasks():
    """
    Sub-commands to interact with tasks.
    """


@app.command("list")
def list_():
    """
    List all the tasks.
    """
    get_fresh_identity_data()
    if state.projects:
        tasks = []
        for task in state.tasks:
            task_copy = task.copy()
            if "recipe" in task_copy:
                # Remove recipe as it's a long dict
                del task_copy["recipe"]
            tasks.append(task_copy)
        headers, rows = dicts_to_table(tasks)
        printer.table(rows, header=headers, divider=True, max_col=3000)
    else:
        typer.echo("No available tasks.")
