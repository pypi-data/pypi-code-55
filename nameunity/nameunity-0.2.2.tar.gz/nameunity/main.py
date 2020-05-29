#!/usr/bin/env python
#
# Author: LucasD11 <yuanzhendai@gmail.com>
#
"""
 _   _                        _   _       _ _
| \ | | __ _ _ __ ___   ___  | | | |_ __ (_) |_ _   _
|  \| |/ _` | '_ ` _ \ / _ \ | | | | '_ \| | __| | | |
| |\  | (_| | | | | | |  __/ | |_| | | | | | |_| |_| |
|_| \_|\__,_|_| |_| |_|\___|  \___/|_| |_|_|\__|\__, |
                                                |___/

A simple tool to help you unity file names.
"""
import os
import sys
import argparse
from lib.formatters import UnknownFormat, FORMATTER_CLASSES
from lib.copy_file import copy_file


DEBUG=False


def parse_args(args):
    # Parse arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__
    )
    parser.add_argument(
        "--source",
        dest="source",
        default=os.getcwd(),
        help="Path of the source directory"
    )
    parser.add_argument(
        "--target",
        dest="target",
        default=os.getcwd(),
        help="Path of the target directory"
    )
    parser.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Output logs without creating new files"
    )
    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        help="Debug mode"
    )
    return parser.parse_args(args)


def rename(source, target, filename, ts, dry_run):
    source_path = os.path.join(source, filename)

    target_filename = ts.strftime("%Y%m%d-%H%M%S.") + filename.split('.')[-1]
    target_filepath = os.path.join(target, target_filename)
    copied = copy_file(source_path, target_filepath, dry_run)
    if DEBUG and copied:
        print("Rename %s to %s" % (source_path, copied))


def main(args=sys.argv[1:]):
    args = parse_args(args)
    if args.debug:
        global DEBUG
        DEBUG = True

    success_count = 0
    fail_count = 0
    formatters = [cls() for cls in FORMATTER_CLASSES]
    for filename in os.listdir(args.source):
        ts = None
        for formatter in formatters:
            try:
                ts = formatter.format(
                    filename,
                    path=os.path.join(args.source, filename)
                )
                break
            except UnknownFormat:
                continue
        if ts is None:
            print("ERROR: Unknown Format,", filename)
        else:
            rename(args.source, args.target, filename, ts, args.dry_run)


if __name__ == '__main__':
    main()
