#!/usr/bin/env python3
"""
A command line tool to interact with Portugal COVID-19 data.
"""
import argparse
import sys

from . import cache
from . import commands


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    # global options.
    parser.add_argument(
        "-v", "--verbose", action="count", help="increase output verbosity"
    )
    parser.add_argument(
        "--clear", action="store_true", help="clears cache."
    )

    sub_parser = parser.add_subparsers(dest="subcommand")
    sub_parser.required = (
        True  # required to be done this way for py36 argparse compatibility.
    )

    commands.add_concelho(sub_parser)

    args = parser.parse_args(argv[1:])
    return args


def main(argv=None):
    if argv is None:
        argv = sys.argv
    args = parse_args(argv)
    try:
        if args.clear:
            cache.clear()
        args.command(args)
    except KeyboardInterrupt:
        sys.exit(-1)


if __name__ == "__main__":
    sys.exit(main(sys.argv) or 0)
