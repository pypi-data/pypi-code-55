"""repo module"""

from pathlib import Path
import yaml


class Error(Exception):
    """Basic repo error"""
    def __init__(self, message):
        super().__init__(self)
        self.message = message


class Repo:
    """A repo contains a sub-directory .alfa-ci in the given location storing
       all environments and metadata. Additionally, a repo provides a
       convenient filesystem representation for the user,
       the so-called working tree, in the given location."""

    repo_dir = '.alfa-ci'
    config_file = 'config.yaml'

    def __init__(self, path):
        self._location = path / Repo.repo_dir

        if not (self.location.exists() or
                (self.location / Repo.config_file).exists()):
            raise Error('Repository is not initialized')

        with (self.location / Repo.config_file).open() as file:
            yaml.full_load(file)

    @property
    def location(self):
        """location getter"""
        return self._location


def init_repo(path):
    """Initializes a new repo in the given path and
       returns a Repo object for it"""

    if not isinstance(path, Path):
        path = Path(path)

    try:
        repo = Repo(path)
        raise Error('Repository already exists in %s' % repo.location)
    except Error:
        (path / Repo.repo_dir).mkdir(parents=False, exist_ok=False)
        (path / Repo.repo_dir / Repo.config_file).touch(exist_ok=False)

    return Repo(path)
