from dataclasses import dataclass
from pathlib import Path
from typing import Set, Sequence, Mapping, MutableSequence

from clutch import Client
from clutch.schema.user.method.torrent.action import TorrentActionMethod
from torrentool.torrent import Torrent

from clutchless.search import TorrentSearch, find


def get_incompletes() -> Sequence[Mapping]:
    client = Client()
    response: Mapping = client.torrent.accessor(
        fields=["id", "name", "percent_done", "torrent_file"]
    ).dict(exclude_none=True)
    try:
        response_torrents: Sequence[Mapping] = response["arguments"]["torrents"]
        incomplete_responses = [
            torrent for torrent in response_torrents if torrent["percent_done"] == 0.0
        ]
        return incomplete_responses
    except KeyError:
        return []


@dataclass
class LinkResult:
    failed: Sequence[Mapping]
    succeeded: Sequence[Mapping]


def link(data_dirs: Set[Path]) -> LinkResult:
    incomplete_responses = get_incompletes()
    responses: Mapping[str, Mapping] = {
        Torrent.from_file(torrent["torrent_file"]).info_hash: torrent
        for torrent in incomplete_responses
    }

    client = Client()
    search = TorrentSearch()
    search += [Path(torrent["torrent_file"]) for torrent in incomplete_responses]
    matches: Mapping[Torrent, Path] = find(search, data_dirs)
    succeeded: MutableSequence[Mapping] = []
    failed: MutableSequence[Mapping] = []
    for (torrent, path) in matches.items():
        torrent_response = responses[torrent.info_hash]
        move_response = client.torrent.move(
            ids=torrent_response["id"], location=str(path.resolve(strict=True))
        )
        if move_response.result != "success":
            failed.append(move_response.dict(exclude_none=True))
            continue
        verify_response = client.torrent.action(
            ids=torrent_response["id"], method=TorrentActionMethod.VERIFY
        )
        if verify_response.result != "success":
            failed.append(verify_response.dict(exclude_none=True))
            continue
        else:
            succeeded.append(verify_response.dict(exclude_none=True))
    return LinkResult(failed, succeeded)
