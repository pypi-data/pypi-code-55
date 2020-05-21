"""
Traverse a folder looking for TODO files and merge into a single TODO file
"""

import sys
import os
from glob2 import glob
import argparse


def concat_todo_files(todo_files, include_header=False):

    combined = ""
    for todo in todo_files:
        if include_header:
            combined += f"\n{todo}\n\n"
        file_content = open(todo, "r").read() + "\n"
        combined += file_content

    return combined


def list_todo_files(parent, basename="TODO.md"):

    """List any files named {basename} in this directory or any of its
    subdirectories """

    glob_str = os.path.join(parent, f"**/{basename}")

    return sorted(glob(glob_str))


def main():

    parser = argparse.ArgumentParser("btodo - make a big TODO file")
    parser.add_argument("dir", type=str, help="the root directory")
    parser.add_argument("--name",
                        type=str,
                        default="TODO.md",
                        help="the name of the file to combine")
    parser.add_argument("--include-header", action="store_true",
                        help="prepend the relative file path to each section")

    args = parser.parse_args(sys.argv[1:])

    todo_files = list_todo_files(args.dir, basename=args.name)
    print(concat_todo_files(todo_files, include_header=args.include_header))


if __name__ == "__main__":
    main()

