import click
from etna_cli import config


@click.group(name="ticket")
def main():
    """Tickets."""


@main.command(name="create")
@click.option("-t", "--title", required=True, help="set title")
@click.option("-c", "--content", required=True,
              help="set content")
@click.option("-T", "--tags", required=True,
              help="specify tags separeted by commas")
@click.option("-s", "--students",
              help="specify one or more student separated by commas")
def create_ticket(title: str, content: str, tags: str, students: str = None):
    """Create ticket."""
    wrapper = config.setup_api()

    tag_list = tags.split(',')
    if students:
        student_list = students.split(',')
    else:
        student_list = None
    wrapper.open_ticket(title, content, tag_list, student_list)


@main.command(name="list")
def list():
    """List tickets."""
    wrapper = config.setup_api()
    tickets = wrapper.get_tickets()
    for ticket in tickets['data']:
        print("========================")
        print("id          : {}".format(ticket['id']))
        print("title       : {}".format(ticket['title']))
        print("created at  : {}".format(ticket['created_at']))
        print("updated at  : {}".format(ticket['updated_at']))
        print("closed at   : {}".format(ticket['closed_at']))
        print("creator     : {}".format(ticket['creator']['login']))
        print("last edit   : {}".format(ticket['last_edit']['login']))
        print("last author : {}".format(ticket['last_author']['login']))


def get_latest_ticket_id(wrapper) -> int:
    """Get latest ticket id."""
    ticket = wrapper.get_tickets()
    ticket_id = ticket['data'][0]['id']
    return int(ticket_id)


@main.command(name="close")
@click.option("-i", "--id", "task_id", help="ticket id")
def close_ticket(task_id: int = None):
    """Close ticket."""
    wrapper = config.setup_api()
    if task_id is None:
        task_id = get_latest_ticket_id(wrapper)

    close_ticket(task_id)


@main.command(name="show")
@click.option("-i", "--id", "task_id", help="ticket id")
def show(task_id: int = None):
    """Show content of ticket."""
    wrapper = config.setup_api()
    if task_id is None:
        task_id = get_latest_ticket_id(wrapper)
    ticket = wrapper.get_ticket(task_id)

    data = ticket['data']
    print("id         : {}".format(data['id']))
    print("title      : {}".format(data['title']))
    print("ttl        : {}".format(data['ttl']))
    print("created at : {}".format(data['created_at']))
    print("updated at : {}".format(data['updated_at']))
    print("closed at  : {}".format(data['closed_at']))
    print("creator    : {}".format(data['creator']['login']))
    print("users      : ", end="")
    [print(user['login'], end=" ") for user in data['users']]
    print(end="\n")

    for message in data['messages']:
        print("========================")
        print("{} | {} :".format(message['created_at'],
                                 message['author']['login']))
        print(message['content'])
