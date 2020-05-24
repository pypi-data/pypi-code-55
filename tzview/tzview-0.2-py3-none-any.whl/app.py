"""
Command line interface for tzview
"""

import argparse
import tzview

__version__ = "0.2"
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
        # Call tzview
        to_dts = tzview.tzview(args.to_tzs, args.from_tz, args.dt)
    except ValueError as ve:
        print(ve.args[0])
        return 1
    else:
        for to_dt in to_dts:
            print(f"{to_dt} : {to_dt.tzinfo.zone}")  # type: ignore
        return 0
