import re
import datetime
import py
import git
from vcsdeploy.logic import AbstractLogic, UnknownRevisionError


class GitLogic(AbstractLogic):

    def __init__(self, config):
        self.config = config
        self.repo = git.Repo(config.path)

    def _get_current_tag(self):
        for tag in self.repo.tags:
            if tag.commit == self.repo.head.commit:
                return tag
        return None

    def get_current_version(self):
        tag =self._get_current_tag()
        if tag is not None:
            return tag.name
        if self.repo.head.commit == self.repo.branches.master.commit:
            return 'Latest version'
        return None

    def get_list_of_versions(self):
        versions = []
        for tag in self.repo.tags:
            if re.match(self.config.version_regex, tag.name):
                versions.append(tag.name)
        # repo.tags are from oldest to newest, but we want the reverse
        versions.reverse()
        return versions

    def update_to(self, version):
        try:
            self.repo.git.checkout(version)
        except git.GitCommandError as e:
            raise UnknownRevisionError(str(e))
        ## self.log_update()
        ## return self.generate_update_report_maybe()

    def get_current_revision(self):
        return self.repo.head.commit.hexsha

    def pull(self):
        """
        NOTE: this is more or less the equivalent of "hg pull", NOT "git pull"
        """
        origin = self.repo.remotes[0]
        origin.fetch()
