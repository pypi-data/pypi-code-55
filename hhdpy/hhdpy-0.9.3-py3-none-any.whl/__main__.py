# -*- coding: utf-8 -*-

import sys
import argparse
import hhdpy.typora

USAGE = ""
USAGE += hhdpy.typora.USAGE

def main():
    args = sys.argv[1:]

    if len(args) == 0:
        print("\nUSAGE : {}".format(USAGE))
        exit(0)

    if args[0] == "typora_new_file":
        hhdpy.typora.new_file(args[1])

    parser = argparse.ArgumentParser(
        epilog=USAGE,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("_", nargs="+", default=[])
    parser.parse_args(args)

    # parser.add_argument("arg0", help="arg0", type=str, default="")
    # options = parser.parse_args(args)

if __name__ == "__main__":
    sys.exit(main())