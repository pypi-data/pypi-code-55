"""
Command line interface for tzview
"""

import argparse
import pytz.exceptions
import tzview

__version__ = "0.1"
__author__ = "Julin S"


def create_parser() -> argparse.ArgumentParser:
    """
    Create the parser for the cli.

    Returns the parser object.
    """
    parser = argparse.ArgumentParser(
        prog="tzview",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="A tzview description for argparse"
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s ' + __version__
    )
    parser.add_argument('--dt', default='now')
    parser.add_argument('--from-tz', dest='from_tz', default='local')
    parser.add_argument('to_tzs', nargs='+')
    return parser


def main(args: argparse.Namespace) -> int:
    """
    The main function for the CLI.

    Returns non-zero on error and zero on successful operation.
    """

    try:
        # Find source datetime
        dt = tzview.parse_dt(args.dt)

        # Find source timezone
        from_tz = tzview.parse_tz(args.from_tz)

        # Find target timezones
        to_tzs = []
        for to_tz_str in args.to_tzs:
            to_tz = tzview.parse_tz(to_tz_str)
            to_tzs.append(to_tz)

        # Call tzview
        to_dts = tzview.tzview(dt, from_tz, to_tzs)
    except pytz.exceptions.UnknownTimeZoneError as utze:
        print(f"Unknown timezone: {utze.args[0]}")
        return 1
    except ValueError:
        print(f"Invalid datetime: {args.dt}!")
        return 1
    else:
        for to_dt in to_dts:
            print(f"{to_dt} : {to_dt.tzinfo.zone}")  # type: ignore
        return 0
