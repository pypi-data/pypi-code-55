from pathlib import Path

from clutchless.subcommand.archive import ArchiveCount


def print_archive_count(count: ArchiveCount, location: Path):
    if count.archived > 0:
        print(
            f"Archived {count.archived} torrent files at {location.resolve(strict=True)}."
        )
    else:
        print(f"Archived 0 torrent files.")
    if count.existing > 0:
        print(
            f"Tried to archive {count.existing} torrent files, but they are already archived."
        )
