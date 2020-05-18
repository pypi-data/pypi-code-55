from typing import List

from git import Commit


def files_committed_in_commit(commit: Commit) -> List:
    return list(commit.stats.files.keys())
