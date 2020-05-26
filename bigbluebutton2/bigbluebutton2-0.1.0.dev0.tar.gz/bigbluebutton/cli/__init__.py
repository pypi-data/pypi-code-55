import logging
from getpass import getuser
from pathlib import Path
from typing import Optional, TextIO, Tuple
from urllib.parse import urlparse

import click
import click_log
import toml
from tabulate import tabulate

from ..api import BigBlueButtonGroup
from ..api.attendee import Attendee, Role

logger = logging.getLogger()
click_log.basic_config(logger)


@click.group()
@click_log.simple_verbosity_option(logger, default="WARNING")
@click.option("--config", help="Path to configuration file", type=click.File("r"))
@click.option("--url", help="Base URL of BigBlueBUtton API")
@click.option("--secret", help="Secret salt to authenticate API calls")
@click.option("--group", help="Name of server group entry in configuration file", default="default")
@click.option("--server-name", help="Name of server from group to operate on")
@click.pass_context
def bbb(
    ctx: click.Context,
    config: Optional[TextIO] = None,
    url: Optional[str] = None,
    secret: Optional[str] = None,
    group: str = "default",
    server_name: Optional[str] = None,
):
    """Command-line wrapper for the BigBlueButton API."""
    ctx.ensure_object(dict)

    bbb_group = BigBlueButtonGroup(group)

    # Find config files from XDG if not set
    if config is None:
        candidate = Path(click.get_app_dir("python-bigbluebutton2"), "bbb-cli.toml")
        if candidate.exists():
            config = open(candidate, "r")
            logger.debug(f"Loaded configuration from {candidate}")

    if config is not None:
        config_dict = toml.load(config)
    else:
        config_dict = {}

    if url is not None and secret is not None and config is None:
        bbb_group.add("", url, secret)
        logger.debug("Using single server from command-line")
    elif "groups" in config_dict:
        for server in config_dict["groups"].get(group, []):
            # Guess host/url parameters from each other if necessary
            if server.get("host") and not server.get("url"):
                server["url"] = f"https://{server['host']}/bigbluebutton/api/"
            elif server.get("url") and not server.get("host"):
                server["host"] = urlparse(server["url"]).netloc.split(":")[0]

            if server_name is None or server["name"] == server_name:
                bbb_group.new(server["name"], server["url"], server["secret"], server["host"])
                logger.debug(f"Added server {server['name']} from configuration")
    else:
        raise click.UsageError("Either url/secret or config file must be set.")

    ctx.obj["apis"] = bbb_group


@bbb.group()
@click.pass_context
def servers(ctx):
    pass


@servers.command("list")
@click.pass_context
def servers_list(ctx):
    """List all servers in the group and their state."""
    # Update all possible data for all servers
    ctx.obj["apis"].refresh()

    data = []
    for name, api in ctx.obj["apis"].apis.items():
        if api.sysstat is not None:
            try:
                loadavgs = (
                    float(api.sysstat.reports["queue"].tail(1)["ldavg-1"]),
                    float(api.sysstat.reports["queue"].tail(1)["ldavg-5"]),
                    float(api.sysstat.reports["queue"].tail(1)["ldavg-15"]),
                )
            except KeyError:
                loadavgs = tuple()

            num_cpus = api.sysstat.num_cpus
        else:
            loadavgs = tuple()
            num_cpus = ""

        data.append(
            (name, api.host, ", ".join(["{:.2f}".format(val) for val in loadavgs]), str(num_cpus))
        )
    headers = ("Name", "Hostname", "Load avg.", "CPUs")

    print(tabulate(data, headers=headers))


@servers.command("ssh")
@click.argument("command", nargs=-1, required=True)
@click.pass_context
def ssh(ctx, command: Tuple[str]):
    """Execute command via ssh on all hosts."""
    stdin = click.get_text_stream("stdin")
    stdout = click.get_text_stream("stdout")
    stderr = click.get_text_stream("stderr")

    if not stdin.isatty():
        # Consume stdin completely to multiplex it
        input_ = stdin.read()
    else:
        # Ignore stdin if run interactively
        input_ = None

    res = ctx.obj["apis"].ssh_command(command, input_)

    for name, output in res.items():
        stdout.write(output.stdout)
        stderr.write(output.stderr)


@bbb.group()
@click.pass_context
def meetings(ctx):
    pass


@meetings.command("list")
@click.pass_context
def meetings_list(ctx):
    """List all current meetings and basic data in tabular form."""
    meetings = ctx.obj["apis"].get_meetings()

    data = [
        (
            meeting.meeting_id,
            meeting.meeting_name,
            meeting.voice_bridge,
            meeting.running,
            meeting.listener_count,
            meeting.voice_participant_count,
            meeting.video_count,
            meeting.origin,
            meeting.api.name,
        )
        for _, meeting in meetings.items()
    ]
    headers = ("ID", "Name", "Bridge", "Running", "Listeners", "Voice", "Video", "Origin", "Server")

    print(tabulate(data, headers=headers))


@meetings.command("attendees")
@click.pass_context
def meetings_attendees(ctx):
    """List all attendees in all current meetings in tabular form."""
    meetings = ctx.obj["apis"].get_meetings()
    ctx.obj["meetings"] = meetings

    ctx.invoke(meeting_attendees)


@meetings.command("create")
@click.option("--name", help="Displayed name of new meeting", required=True)
@click.pass_context
def meetings_create(ctx, name: str):
    """Create a new meeting."""
    meeting = ctx.obj["apis"].create_meeting(meeting_name=name)

    click.echo(f"Meeting ID {meeting.meeting_id} created.")


@bbb.group()
@click.argument("meeting_id", required=True)
@click.pass_context
def meeting(ctx, meeting_id: str):
    meeting = ctx.obj["apis"].get_meetings()[meeting_id]
    ctx.obj["meetings"] = {meeting_id: meeting}


@meeting.command("attendees")
@click.pass_context
def meeting_attendees(ctx):
    """List all current attendees in a meeting in tabular form."""
    attendees = {}
    for meeting_id, meeting in ctx.obj["meetings"].items():
        attendees.update(meeting.attendees)

    data = [
        (
            attendee.full_name,
            attendee.user_id,
            attendee.role.name,
            "X" if attendee.is_presenter else " ",
            "X" if attendee.is_listening_only else " ",
            "X" if attendee.has_joined_voice else " ",
            "X" if attendee.has_video else " ",
            attendee.meeting.meeting_name,
            attendee.meeting.api.name,
        )
        for _, attendee in attendees.items()
    ]
    headers = (
        "Name",
        "ID",
        "role",
        "Presenter",
        "Listening",
        "Voice",
        "Video",
        "Meeting",
        "Server",
    )

    print(tabulate(data, headers=headers))


@meeting.command("join")
@click.option("--full-name", help="Full display name to join with", default=getuser())
@click.option(
    "--role",
    help="Full display name to join with",
    type=click.Choice(["VIEWER", "MODERATOR"], case_sensitive=False),
    default="VIEWER",
)
@click.pass_context
def meeting_join(ctx, full_name: str, role: Role):
    """Join the meeting by opening the default browser."""
    meeting = list(ctx.obj["meetings"].values())[0]
    attendee = Attendee(meeting, full_name=full_name, role=Role[role])
    attendee.join(browser=True)
