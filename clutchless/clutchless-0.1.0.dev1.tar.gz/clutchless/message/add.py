from pathlib import Path

from colorama import init, deinit, Fore
from torrentool.torrent import Torrent

from clutchless.subcommand.add import AddResult


def print_add(add_result: AddResult):
    init()
    added_count = len(add_result.added_torrents)
    if added_count > 0:
        print(Fore.LIGHTWHITE_EX + f"Added {added_count} torrents:")
        for (torrent, _) in add_result.added_torrents.items():
            try:
                path: Path = add_result.matches[torrent]
                print_added(torrent, path)
            except KeyError:
                print_added(torrent)
    failed_count = len(add_result.failed_torrents)
    if failed_count > 0:
        print(Fore.LIGHTWHITE_EX + f"Did not locate {failed_count} torrents:")
        for (torrent, failure_reason) in add_result.failed_torrents.items():
            print_missed(torrent, failure_reason)
    deinit()


def print_missed(torrent: Torrent, reason: str):
    print(Fore.RED + f"\N{ballot x} {torrent.name} because: {reason}")


def print_added(torrent: Torrent, path: Path = None):
    if path:
        print(
            Fore.GREEN + f"\N{check mark} {torrent.name} at {path.resolve(strict=True)}"
        )
    else:
        print(Fore.GREEN + f"\N{check mark} {torrent.name}")
