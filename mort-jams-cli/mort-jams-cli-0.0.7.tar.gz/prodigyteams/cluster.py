import typer

from .utils import (
    dicts_to_table,
    get_broker,
    get_broker_meta,
    get_fresh_identity_data,
    printer,
    state,
)

app = typer.Typer()


@app.callback()
def cluster():
    """
    Sub-commands to interact with cluster.
    """


@app.command()
def info():
    """
    View information about the active cluster.
    """
    get_fresh_identity_data()
    broker = get_broker()
    meta = get_broker_meta()
    printer.divider(broker.address)


@app.command()
def verify():
    """
    Verify the cluster has no problems.
    """
    get_fresh_identity_data()
    broker = get_broker()
    meta = get_broker_meta()
    problems = meta["problems"]
    printer.divider(f"({len(problems)}) Problems")
    if len(problems) == 0:
        printer.good("No cluster problems found!")
        return
    for problem in problems:
        printer.fail(problem.get("name", "no name"))
        printer.text(problem.get("description", "no description"))
        data = problem.get("data", None)
        if data is None:
            continue
        if isinstance(data, dict):
            printer.table(data, header=data.keys(), divider=True, max_col=3000)
        elif isinstance(data, str):
            printer.text(data)
    printer.fail(f"Found ({len(problems)}) problems!")
