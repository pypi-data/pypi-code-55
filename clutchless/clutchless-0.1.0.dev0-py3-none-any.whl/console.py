""" A tool for working with torrents and their data in the Transmission BitTorrent client.

Usage:
    clutchless [options] <command> [<args> ...]

Options:
    -h, --help  Show this screen.
    --version   Show version.

The available clutchless commands are:
    add         Add torrents to Transmission (with or without data).
    find        Locate data that belongs to torrent files.
    link        For torrents with missing data in Transmission, find the data and fix the location.
    archive     Copy .torrent files from Transmission for backup.
    organize    Migrate torrents to a new location, sorting them into separate folders for each tracker.

See 'clutchless help <command>' for more information on a specific command.

"""
from pathlib import Path
from pprint import pprint
from typing import Set, KeysView

from docopt import docopt
from torrentool.torrent import Torrent

from clutchless.message.add import print_add
from clutchless.message.find import print_find
from clutchless.message.organize import print_tracker_list
from clutchless.parse.add import parse_add
from clutchless.parse.find import parse_find
from clutchless.subcommand.add import AddResult, add
from clutchless.subcommand.archive import archive
from clutchless.subcommand.find import find
from clutchless.subcommand.organize import get_ordered_tracker_list


def main():
    args = docopt(__doc__, options_first=True)
    # good to realize that argv is a list of arguments
    # here we create a list of the original command & args without "top-level" options
    argv = [args["<command>"]] + args["<args>"]
    print("args:")
    pprint(args)
    print("argv:")
    pprint(argv)
    command = args.get("<command>")
    if command == "add":
        # parse arguments
        from clutchless.parse import add as add_command

        add_args = parse_add(docopt(doc=add_command.__doc__, argv=argv))
        torrent_search, data_dirs = add_args.torrent_search, add_args.data_dirs
        # action
        add_result: AddResult = add(torrent_search, data_dirs)
        # output message
        print_add(add_result)
    elif command == "link":
        from clutchless.parse import link as link_command

        link_args = parse_add(docopt(doc=link_command.__doc__, argv=argv))
        print("link args")
        print(link_args)
    elif command == "find":
        try:
            # parse arguments
            from clutchless.parse import find as find_command

            find_args = parse_find(docopt(doc=find_command.__doc__, argv=argv))
            torrent_search, data_dirs = find_args.torrent_search, find_args.data_dirs
            # action
            matches = find(torrent_search, data_dirs)
            # output message
            torrents: KeysView[Torrent] = find_args.torrent_search.torrents.keys()
            missed: Set[Torrent] = torrents - matches.keys()
            print_find(matches, missed)
        except KeyError as e:
            print(f"failed:{e}")
        except ValueError as e:
            print(f"invalid argument(s):{e}")
    elif command == "organize":
        from clutchless.parse import organize as organize_command
        org_args = docopt(doc=organize_command.__doc__, argv=argv)
        print("organize args:")
        pprint(org_args)
        if org_args.get("--list"):
            tracker_list = get_ordered_tracker_list()
            print_tracker_list(tracker_list)
        else:
            pass
    elif command == "archive":
        from clutchless.parse import archive as archive_command
        archive_args = docopt(doc=archive_command.__doc__, argv=argv)
        location = Path(archive_args.get("<location>"))
        if location:
            count = archive(Path(location))
            if count.archived > 0:
                print(f'Archived {count.archived} torrent files at {location.resolve(strict=True)}.')
            else:
                print(f'Archived 0 torrent files.')
            if count.existing > 0:
                print(f'Tried to archive {count.existing} torrent files, but they are already archived.')
