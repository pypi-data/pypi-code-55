#  Copyright (c) 2020. Daniel Elsner.

import logging
from typing import List, Optional

from git import Repo, InvalidGitRepositoryError

from .hooks import Hook


class Walker(object):
    """
    Walker class to replay repository history.
    """

    def __init__(self: "Walker",
                 repository_path: str,
                 branch: str,
                 start_commit: str,
                 num_commits: int = 10,
                 pre_hooks: Optional[List[Hook]] = None,
                 hooks: Optional[List[Hook]] = None,
                 post_hooks: Optional[List[Hook]] = None) -> None:
        self.repo: Optional[Repo] = None
        try:
            self.repo = Repo(repository_path)
        except InvalidGitRepositoryError as e:
            raise InvalidGitRepositoryError(f"{str(e)} is not a git repository")
        self.branch: str = branch
        self.start_commit: str = start_commit
        self.num_commits: int = num_commits
        self.pre_hooks: List[Hook] = pre_hooks if pre_hooks is not None else []
        self.hooks: List[Hook] = hooks if hooks is not None else []
        self.post_hooks: List[Hook] = post_hooks if post_hooks is not None else []

    def walk(self: "Walker"):
        # clean for convenience
        self._reset_repo(rm_dirs=True)

        # checkout start commit
        logging.debug("Checking out commit {}.".format(self.start_commit))
        self.repo.git.checkout(self.start_commit)

        # run pre-hooks
        for h in self.pre_hooks:
            h.run()

        # init counter
        counter = 1

        # walk history along branch
        logging.debug("Obtaining linear commit history for branch {}.".format(self.branch))
        for commit in self.repo.iter_commits(f"{self.start_commit}..{self.branch}",
                                             ancestry_path=True,
                                             reverse=True,
                                             no_merges=True):
            # apply changeset from next commit
            logging.debug("Patching with commit {}.".format(commit))
            self.repo.git.cherry_pick("-n", commit.hexsha)

            # unstage changes (to be able to use `git diff`)
            self.repo.git.reset()

            # run hooks
            for h in self.hooks:
                h.run()

            # reset changes and clean untracked files
            # (keep dirs, as they might be required for caching)
            self._reset_repo(rm_dirs=False)

            # inc counter and break if `num_commits` reached
            counter += 1
            if counter > self.num_commits:
                break

            # checkout next commit
            self.repo.git.checkout(commit.hexsha)

        # run post-hooks
        for h in self.post_hooks:
            h.run()

    def _reset_repo(self: "Walker", rm_dirs: bool = True):
        self.repo.git.reset(hard=True)
        self.repo.git.clean(force=True, d=rm_dirs)
