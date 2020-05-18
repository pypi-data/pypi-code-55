""" Locate data that belongs to torrent files.

Usage:
    clutchless find <torrents> ... (-d <data> ...)

Arguments:
    <torrents> ...  Filepath of torrent files or directories to search for torrent files.

Options:
    -d <data> ...  Folder(s) to search for data that belongs to the specified torrent files.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Set

from clutchless.search import TorrentSearch, get_torrent_files


@dataclass
class FindArgs:
    torrent_files: Set[Path]
    data_dirs: Set[Path]
    torrent_search: TorrentSearch


def parse_find(args: Mapping) -> FindArgs:
    torrent_files = parse_torrent_files(args)
    data_dirs = parse_data_dirs(args)

    torrent_search = TorrentSearch()
    torrent_search += torrent_files
    return FindArgs(torrent_files, data_dirs, torrent_search)


def parse_torrent_files(args: Mapping) -> Set[Path]:
    torrent_paths = {Path(torrent) for torrent in args["<torrents>"]}
    torrent_dirs = set()
    torrent_files = set()
    for path in torrent_paths:
        if not path.exists():
            raise ValueError("Supplied torrent path doesn't exist")
        elif path.is_dir():
            torrent_dirs.add(path)
        elif path.is_file():
            torrent_files.add(path)
        else:
            raise ValueError("Invalid ")

    for directory in torrent_dirs:
        torrent_files.update(get_torrent_files(directory))
    return {file.resolve(strict=True) for file in torrent_files}


def parse_data_dirs(args: Mapping) -> Set[Path]:
    data_paths = [Path(data_dir) for data_dir in args["-d"]]
    data_dirs = set()
    for path in data_paths:
        if not path.exists():
            raise ValueError("Supplied data path doesn't exist")
        elif path.is_dir():
            data_dirs.add(path)
        else:
            raise ValueError("Invalid")
    return data_dirs
