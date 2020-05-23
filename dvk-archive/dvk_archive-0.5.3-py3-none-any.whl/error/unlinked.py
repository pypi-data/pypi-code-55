#!/usr/bin/env python3

"""Functions for checking media files with no linked Dvk."""

from tqdm import tqdm
from os import getcwd, listdir
from os.path import abspath, join, isdir
from argparse import ArgumentParser
from dvk_archive.file.dvk_handler import DvkHandler
from dvk_archive.processing.printing import print_paths


def unlinked_media(
        dvk_directories: list = None,
        dvk_handler: DvkHandler = None) -> list:
    """
    Check for files without corresponding DVK files.

    Parameters:
        dvk_directory (str): Directory from which to search for DVK files.
            Used if dvk_handler is None
        dvk_handler (list): DvkHandler with loaded DVK files.

    Returns:
        list: List of paths for files with no corresponding DVK file
    """
    if dvk_handler is not None:
        handler = dvk_handler
    else:
        handler = DvkHandler()
        handler.load_dvks(dvk_directories)
    # FIND ALL MEDIA FILES
    print("Searching for all media files.")
    missing = []
    for path in tqdm(handler.paths):
        for f in listdir(abspath(path)):
            file = abspath(join(abspath(path), f))
            if not file.endswith(".dvk") and not isdir(file):
                missing.append(file)
    # REMOVES UNLINKED MEDIA
    print("Searching for all unlinked media.")
    d_size = handler.get_size()
    for d_num in tqdm(range(0, d_size)):
        # GETS MEDIA FILES FROM DVK
        dvk = handler.get_dvk_direct(d_num)
        d_files = [dvk.get_media_file()]
        if dvk.get_secondary_file() is not None:
            d_files.append(dvk.get_secondary_file())
        # REMOVES FROM THE MISSING FILES LIST
        m_num = 0
        while m_num < len(missing):
            i = 0
            while i < len(d_files):
                if d_files[i] == missing[m_num]:
                    del d_files[i]
                    del missing[m_num]
                    i = i - 1
                    m_num = m_num - 1
                i = i + 1
            m_num = m_num + 1
            if len(d_files) == 0 or len(missing) == 0:
                break
    return missing


def main():
    """Run the unlinked_media function from the command line."""
    parser = ArgumentParser()
    parser.add_argument(
        "directory",
        help="Directory in which to preform operations.",
        nargs="?",
        type=str,
        default=str(getcwd()))
    args = parser.parse_args()
    dir = abspath(args.directory)
    print_paths(unlinked_media([dir]), dir)


if __name__ == "__main__":
    main()
