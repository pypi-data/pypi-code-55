import click
from etna_cli import config


@click.group(name="project")
def main():
    """Projects."""


def is_validated(validation: str = None) -> str:
    """Check if validated."""
    if validation == "Validée":
        validated = "YES"
    elif validation == "Non validée":
        validated = "NO"
    else:
        validated = "Not yet"
    return validated


@main.command()
def list():
    """List projects."""
    wrapper = config.setup_api()
    projects = wrapper.get_projects()

    for project in projects:
        print("==============================")
        print("name       : {}".format(project['name']))
        print("long name  : {}".format(project['long_name']))
        print("UV         : {}".format(project['uv_name']))
        print("starts on  : {}".format(project['date_start']))
        print("ends on    : {}".format(project['date_end']))
        print("duration   : {}".format(int(project['duration']) / 3600))
        print("validated  : {}".format(is_validated(project['validation'])))


@main.command()
@click.option("-t", "--type", "type_", help="[cours|project|quest]")
def activites(type_: str = None):
    """List activites."""
    wrapper = config.setup_api()
    projects = wrapper.get_projects()

    for project in projects:
        pid = project['id']
        activites = wrapper.get_project_activites(pid)
        handle_activites(activites, type_)


def handle_activites(activites: dict, act_type: str = None):
    """Handle different types of activites."""
    for activity in activites:
        if act_type is not None:
            if activity['type'] == act_type:
                print_activity(activity)
        else:
            print_activity(activity)


def print_activity(quest: dict):
    """Print content of activity."""
    val = "Yes"
    print("========================")
    print("name         : {}".format(quest['name']))
    print("coef         : {}".format(quest['coefficient']))
    print("type         : {}".format(quest['type']))
    if quest['eliminate'] is None:
        val = "No"
    print("eliminate    : {}".format(val))

    try:
        print("mark min     : {}".format(quest['mark_min']))
        print("mark max     : {}".format(quest['mark_max']))
        print("average mark : {}".format(quest['average_mark']))
        print("student mark : {}".format(quest['student_mark']))
    except KeyError:
        pass

    print("starts on    : {}".format(quest['date_start']))
    print("ends on      : {}".format(quest['date_end']))
