from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, MutableMapping, Set

from clutch import Client
from clutch.network.rpc.message import Response
from clutch.schema.user.method.torrent.add import TorrentAddArguments
from torrentool.torrent import Torrent
from clutch.schema.user.response.torrent.add import (
    Torrent as ResponseTorrent,
    TorrentAdd,
)

from clutchless.search import TorrentSearch, find


@dataclass
class AddResult:
    added_torrents: Mapping[Torrent, ResponseTorrent]
    failed_torrents: Mapping[Torrent, str]
    matches: Mapping[Torrent, Path]


def add(torrent_search: TorrentSearch, data_dirs: Set[Path]) -> AddResult:
    added_torrents: MutableMapping[Torrent, ResponseTorrent] = {}
    failed_torrents: MutableMapping[Torrent, str] = {}
    matches = find(torrent_search, data_dirs)
    for (torrent, download_dir) in matches.items():
        response = add_torrent(torrent_search.torrents[torrent], download_dir)
        added_torrent: ResponseTorrent = response.arguments.torrent_added
        if (
            response.result == "success"
            and len(added_torrent.dict(exclude_none=True).items()) > 0
        ):
            added_torrents[torrent] = added_torrent
        else:
            failed_torrents[torrent] = response.result
    return AddResult(added_torrents, failed_torrents, matches)


def add_torrent(torrent: Path, download_dir: Path) -> Response[TorrentAdd]:
    client = Client()
    arguments: TorrentAddArguments = {
        "filename": str(torrent.resolve(strict=True)),
        "paused": True,
        "download_dir": str(download_dir.resolve(strict=True)),
    }
    return client.torrent.add(arguments)
