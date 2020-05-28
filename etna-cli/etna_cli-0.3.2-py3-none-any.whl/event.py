import click
import dateutil.parser as dp
import pendulum
from datetime import datetime
from typing import Tuple

from etna_cli import config


@click.group(name="event")
def main():
    """Events."""


def get_dates(time: str = None) -> Tuple[datetime, datetime]:
    """
    Return start and end dates for the events to list.
    """
    if time is None:
        time = 'week'

    today = pendulum.now()
    start_of = today.start_of(time)
    end_of = today.end_of(time)

    start = str(start_of).split('T')[0]
    end = str(end_of).split('T')[0]

    start_date = dp.parse(start)
    end_date = dp.parse(end)

    return start_date, end_date


def get_events(wrapper, student: str = None, time: str = None) -> dict:
    """
    list events
    """
    start, end = get_dates(time)
    event_data = wrapper.get_events(start_date=start,
                                    end_date=end,
                                    login=student)
    return event_data


@main.command()
@click.argument("student", type=click.STRING, required=False)
@click.option("-t", "--time", help="specify week, month, year")
def list(student: str = None, time: str = None):
    """List events."""
    wrapper = config.setup_api()
    events_data = get_events(wrapper, student, time)

    for i, _ in enumerate(events_data):
        print("==============================")
        print("name     : {}".format(events_data[i]['name']))
        print("uv name  : {}".format(events_data[i]['uv_name']))
        print("activity : {}".format(events_data[i]['activity_name']))
        print("location : {}".format(events_data[i]['location']))
        print("starts at: {}".format(events_data[i]['start']))
        print("ends at  : {}".format(events_data[i]['end']))
