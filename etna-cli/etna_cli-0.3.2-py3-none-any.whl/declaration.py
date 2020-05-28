import click
from datetime import datetime
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


@main.command(name="modules")
def list_available_modules():
    """Available modules to declare for.
    This is a temp function, the goal is to
    call the function which is in project.py.
    """
    wrapper = config.setup_api()
    logs = wrapper.get_logs()
    start = logs['contracts'][0]['periods'][0]['start']
    start_run = datetime.strptime(start.split()[0], '%Y-%m-%d')

    projects = wrapper.get_projects(date=start_run)
    for project in projects:
        print("==============================")
        print("id         : {}".format(project['id']))
        print("name       : {}".format(project['name']))
        print("long name  : {}".format(project['long_name']))
        print("UV         : {}".format(project['uv_name']))
        print("starts on  : {}".format(project['date_start']))
        print("ends on    : {}".format(project['date_end']))
        print("duration   : {}".format(int(project['duration']) / 3600))


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
