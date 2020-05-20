import datetime as dt
import pendulum

import click
import tableformatter as tf
from requests.exceptions import HTTPError  # pylint: disable=no-name-in-module
from tqdm import tqdm

from ...api.oui_v3 import Client
from ...api.requests import TravelRequest
from ..ext import DateParseParamType, daterange
from ...models import Passenger

# TODO: Use pendulum everywhere


@click.command()
@click.argument("origin")
@click.argument("destination")
@click.option("--date", type=DateParseParamType(), default="now", show_default=True)
@click.option(
    "--class",
    "travel_class",
    type=click.Choice(["first", "second"]),
    default="second",
    show_default=True,
    help="Travel class.",
)
@click.pass_context
def calendar(ctx: click.Context, **args: str) -> None:
    """
    Show the prices for a given month.
    """
    stations = ctx.obj["stations"]
    client = Client(stations)

    # TODO: Choose min hour / max hour

    departure_station = stations.find_or_raise(args["origin"])
    arrival_station = stations.find_or_raise(args["destination"])
    passenger = Passenger.dummy()

    click.echo(
        "{} → {} ({:.0f}km)".format(
            departure_station.name,
            arrival_station.name,
            departure_station.distance_to(arrival_station),
        ),
        err=True,
    )

    click.echo("{} ({} years old)\n".format(passenger.name, passenger.age), err=True)

    start = pendulum.instance(args["date"]).start_of("day")
    start = max(start.start_of("month"), pendulum.today().start_of("day"))
    stop = start.end_of("month")

    cols = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
    ]

    rows = [["" for _ in range(7)] for _ in range(5)]

    def lowest_price(journeys):
        lowest = None
        for journey in journeys:
            for proposal in journey.proposals:
                if not lowest or proposal.price < lowest:
                    lowest = proposal.price
        return lowest

    it = daterange(start, stop, dt.timedelta(days=1))
    for date in tqdm(it, total=(stop - start).days, leave=False):
        req = TravelRequest(
            departure_station=departure_station,
            arrival_station=arrival_station,
            passengers=[passenger],
            date=date,
            travel_class=args["travel_class"],
        )
        journeys = client.travel_request_full(req)
        lowest = lowest_price(journeys)
        if lowest:
            rows[date.week_of_month - 1][date.day_of_week] = lowest

    # TODO: Colors
    click.echo(tf.generate_table(rows, cols, grid_style=tf.FancyGrid()))
