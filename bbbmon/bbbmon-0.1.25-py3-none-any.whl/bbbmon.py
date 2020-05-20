#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import json
import click


# Local module imports
from bbbmon.xmldict import XmlListConfig, XmlDictConfig
from bbbmon.configuration import Config, Endpoint, SERVER_PROPERTIES_FILE, Url, Secret, get_user_config_path, init_config, new_config
from bbbmon.meetings import *
from bbbmon.printing import *



# Allow -h as help option as well
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])



class AliasedGroup(click.Group):
    """
    Subclass of Group to allow abbreviating commands like this:
    Instead of `bbbmon meetings` one could type `bbbmon m`
    """
    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))


@click.group(context_settings=CONTEXT_SETTINGS, cls=AliasedGroup)
@click.option('--userconfig', '-u', is_flag=True, help="Use user config even if on server")
@click.option('--watch', '-w', help="Run repeatedly with the given interval in seconds", type=click.IntRange(2, 2147483647, clamp=True))
def main(userconfig, watch):
    """BBBMON is a small CLI utility to monitor bbb usage

    \b
    Examples:  bbbmon config --edit
               bbbmon meetings --watch 20 --endpoint bbb

    Internally bbbmon relies on the offical bbb-API, which means you need to have the server's secret in order to create a valid request. Create a new configuration with: bbbmon config --new
    """
    pass 



@main.command(context_settings=CONTEXT_SETTINGS)
@click.pass_context
@click.option('--userconfig', '-u', is_flag=True, help="Use user config even if on server")
@click.option('--endpoint', '-e', multiple=True, help="Filter by one or more endpoints as named in the user configuration (e.g. [servername]). Order is respected.")
@click.option('--watch', '-w', help="Run repeatedly with the given interval in seconds", type=click.IntRange(2, 2147483647, clamp=True))
@click.option('-n', help="The number of meetings to show in the leaderboards (Default: 5)", type=int)
@click.option('--leaderboards/--no-leaderboards', default=True, show_default=True, help="Hide or show the meeting leaderboards")
@click.option('--participants/--no-participants', default=True, show_default=True, help="Hide or show the participants")
@click.option('--meetings/--no-meetings', default=True, show_default=True, help="Hide or show the meetings")
@click.option('--presenter/--no-presenter', default=True, show_default=True, help="Hide or show the presenters")
@click.option('--presenter-id/--no-presenter-id', default=False, show_default=True, help="Hide or show the presenter IDs")
@click.option('--short', '-s', is_flag=True, help="Print less")
@click.option('--compact/--expanded', '-c/-x', default=True, show_default=True, help="Print compactly (in columns) or expanded (on seperate lines)")
@click.option('--twolines', '-2', is_flag=True, help="Print essentials on two lines")
@click.option('--all', '-a', 'all_', is_flag=True, help="Print all")
@click.option('--fancy/--no-fancy', default=False, show_default=True, help="Use fancy headers")
def meetings(ctx, userconfig, watch, short, compact, n, all_, twolines, leaderboards, participants, presenter, presenter_id, meetings, endpoint, fancy):
    """View currently active meetings"""
    if short:
        leaderboards = False
    if all_:
        leaderboards = True
        participants = True
        presenter = True
        presenter_id = True
        meetings = True
        if n is None:
            n = 99999
    if compact:
        if n is None:
            n = 1
    if n is None:
        n = 5

    config = init_config(userconfig)
    config.filter_endpoints(endpoint)
    if watch is not None:
        while watch is not None:
            if twolines:
                meetings_twolines(config, watch, fancy)
            else:
                list_meetings(config, leaderboards, n, participants, presenter, presenter_id, meetings, watch, fancy, compact)
            time.sleep(watch)
    else:
        if twolines:
            meetings_twolines(config, watch, fancy)
        else:
            list_meetings(config, leaderboards, n, participants, presenter, presenter_id, meetings, watch, fancy, compact)



@main.command(context_settings=CONTEXT_SETTINGS)
@click.pass_context
@click.option('--watch', '-w', help="Run repeatedly with the given interval in seconds", type=click.IntRange(2, 2147483647, clamp=True))
@click.option('--userconfig', '-u', is_flag=True, help="Use user config even if on server")
@click.option('--new', is_flag=True, help="Create a new default config and open it in the default editor")
@click.option('--edit', is_flag=True, help="Open the config in the default editor")
@click.option('--print', 'print_', is_flag=True, help="Print the config to stdout")
@click.option('--path', is_flag=True, help="Print the path to the config")
def config(ctx, userconfig, watch, new, edit, path, print_):
    """Print, show or edit the config"""
    user_config_path = get_user_config_path()

    if edit:
        if os.path.isfile(user_config_path):
            click.edit(filename=user_config_path)
        else:
            new_config(user_config_path)
    elif path:
        print(get_user_config_path())
    elif print_:
        with open(get_user_config_path(), "r") as f:
            print(f.read())
    elif new:
        if os.path.isfile(user_config_path):
            click.echo("{} There is already a config file at {} !".format(click.style(" WARNING ", bg="bright_red", fg="black", bold=True), user_config_path))
            if click.confirm(click.style('Do you want to edit it with your default editor instead of overwriting it?', fg="yellow")):
                click.edit(filename=user_config_path)
            else:
                if click.confirm(click.style('Do you want to overwrite it with the default config instead?', fg="red"), abort=True):
                    new_config(user_config_path, skip_prompt=True)
        else:
            new_config(user_config_path)
    else:
        ctx = click.get_current_context()
        click.echo(ctx.get_help())


@main.command(context_settings=CONTEXT_SETTINGS)
@click.pass_context
@click.option('--watch', '-w', help="Run repeatedly with the given interval in seconds", type=click.IntRange(2, 2147483647, clamp=True))
@click.option('--compact/--pretty', '-c/-p', default=False, show_default=True, help="Print pretty and indented json or compact")
@click.option('--userconfig', '-u', is_flag=True, help="Use user config even if on server")
@click.option('--endpoint', '-e', multiple=True, help="Filter by one or more endpoints as named in the user configuration (e.g. [servername]). Order is respected.")
def json(ctx, userconfig, watch, endpoint, compact):
    """Print json"""
    config = init_config(userconfig)
    config.filter_endpoints(endpoint)
    if not config.endpoints:
        exit()
    if watch is not None:
        while watch is not None:
            print(format_json(config, watch, compact))
            time.sleep(watch)
    else:
        print(format_json(config, watch, compact))




if __name__ == "__main__":
    main()