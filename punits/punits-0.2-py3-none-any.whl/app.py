"""
Command line interface for punits
"""

__version__ = "0.2"
__author__ = "Julin S"

import argparse

import punits

SUPPORTED_MEASURES = ['mass', 'length', 'volume', 'data', 'temperature']


def create_parser() -> argparse.ArgumentParser:
    """
    Create the parser for the cli.

    Returns the parser object.
    """
    parser = argparse.ArgumentParser(
        prog="punits",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="A punits description for argparse"
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s ' + __version__
    )

    # Type conversion is automatic when `type` arg is mentioned
    parser.add_argument('measure', choices=SUPPORTED_MEASURES)
    parser.add_argument('src_unit')
    parser.add_argument('target_unit')
    parser.add_argument('values', nargs='+', type=float)
    parser.add_argument('-p', '--precision', default=2, type=int)
    parser.add_argument('-v', '--verbose', action="store_true")

    # Relevant only for length
    parser.add_argument('--dpi', type=int,
                        help="Use when converting to or from px")
    return parser


def main(args: argparse.Namespace) -> int:
    """
    The main function for the CLI.

    Returns non-zero on error and zero on successful operation.
    """
    try:
        src_unit = punits.find_unit_code(args.measure, args.src_unit)
        target_unit = punits.find_unit_code(args.measure, args.target_unit)

        params = {}
        if args.dpi is not None:
            params['dpi'] = args.dpi

        results = punits.punits(args.measure, src_unit,
                                target_unit, args.values, params)
        str_results = [
            f"{round(result, args.precision):g}" for result in results]
        out_str = ' '.join(str_results)
        print(out_str)

        if args.verbose:
            factor = punits.get_factor(args.measure, src_unit, target_unit)
            if factor is not None:
                # Linear relationship between units
                print(f"\n1 {target_unit} = {factor:g} {src_unit} (approx)")
    except ValueError as ve:
        print(ve.args[0])
        return 1
    return 0
