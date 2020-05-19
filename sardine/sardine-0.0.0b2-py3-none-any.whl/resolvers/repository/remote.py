import os

from git import Repo  # type: ignore

from sardine.resolvers.repository.base import BaseRepositoryResolver


class RemoteRepositoryResolver(BaseRepositoryResolver):
    GITHUB_URL = 'https://github.com/{repository_name}'

    @classmethod
    def download(cls, repository_name: str) -> str:
        repository_location = cls.get_repository_path(repository_name)
        if not cls.repository_already_cloned(repository_location):
            cls.clone_repository(cls.GITHUB_URL.format(repository_name=repository_name), repository_location)
        return repository_location

    @classmethod
    def clone_repository(cls, repository_url: str, repository_location: str):
        Repo.clone_from(repository_url, repository_location)

    @classmethod
    def repository_already_cloned(cls, repository_location: str) -> bool:
        return os.path.isdir(repository_location)

    @classmethod
    def get_repository_name(cls, repository_name: str) -> str:
        return repository_name
