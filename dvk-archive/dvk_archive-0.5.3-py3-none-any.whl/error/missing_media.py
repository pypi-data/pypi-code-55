#!/usr/bin/env python3

"""Functions for checking Dvk objects with missing media."""

from os import getcwd
from os.path import abspath, exists
from tqdm import tqdm
from argparse import ArgumentParser
from dvk_archive.file.dvk_handler import DvkHandler
from dvk_archive.processing.printing import print_paths


def missing_media(
        dvk_directories: list = None,
        dvk_handler: DvkHandler = None) -> list:
    """
    Check for Dvk objects which have missing media files.

    Parameters:
        dvk_directory (str): Directory from which to search for DVK files.
            Used if dvk_handler is None
        dvk_handler (list): DvkHandler with loaded DVK files.

    Returns:
        list: List of Paths for DVK files with missing linked media files
    """
    if dvk_handler is not None:
        handler = dvk_handler
    else:
        handler = DvkHandler()
        handler.load_dvks(dvk_directories)
    missing = []
    handler.sort_dvks("a", True)
    size = handler.get_size()
    print("Searching for DVK files without media files:")
    for i in tqdm(range(0, size)):
        file = handler.get_dvk_sorted(i).get_media_file()
        s_file = handler.get_dvk_sorted(i).get_secondary_file()
        if not exists(file) or (s_file is not None and not exists(s_file)):
            missing.append(handler.get_dvk_sorted(i).get_file())
    return missing


def main():
    """Run the missing_media function from the command line."""
    parser = ArgumentParser()
    parser.add_argument(
        "directory",
        help="Directory in which to preform operations.",
        nargs="?",
        type=str,
        default=str(getcwd()))
    args = parser.parse_args()
    dir = abspath(args.directory)
    print_paths(missing_media([dir]), dir)


if __name__ == "__main__":
    main()
