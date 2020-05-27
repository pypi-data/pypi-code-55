import click
from etna_cli import config


@click.group(name="declare")
def main():
    """Declaration."""


@main.command(name="list")
def list_declarations():
    """List declarations."""
    wrapper = config.setup_api()

    declarations = wrapper.get_declarations()

    for declaration in declarations['hits']:
        print("========================")
        print("UV name     : {}".format(declaration['uv_name']))
        print("started at  : {}".format(declaration['start']))
        print("ended at    : {}".format(declaration['end']))
        print("description : {}".format(declaration['metas']['description']))
        print("declared at : {}".format(declaration['metas']['declared_at']))


@main.command(name="schedule")
def schedule():
    """List schedule."""
    wrapper = config.setup_api()

    logs = wrapper.get_logs()
    # there could me multipe contracts.
    # at this point just use the last one
    for schedule in logs['contracts'][0]['schedules']:
        print("========================")
        print("starts at : {}".format(schedule['start']))
        print("ends at   : {}".format(schedule['end']))


@main.command(name="go")
@click.option("-m", "--module", help="specify module")
@click.option("-c", "--content", help="specify content")
def do_declare(module: str, content: str):
    """Declare work."""
    # tbh I'm a bit lazy for the moment
    # I swear I'll implement that #son
    print("WIP")
