import os
from abc import ABCMeta, abstractmethod

from sardine.config import SARDINE_FOLDER_PATH


class BaseRepositoryResolver(metaclass=ABCMeta):
    REPOSITORY_FOLDER_NAME = "repositories"

    @classmethod
    @abstractmethod
    def download(cls, repository_name: str) -> None:
        pass

    @classmethod
    def create_base_folders(cls) -> None:
        cls._make_directories()

    @classmethod
    def _make_directories(cls, *args) -> str:
        total_folder = os.path.join(cls._repository_folder_path(), *args)
        os.makedirs(total_folder, exist_ok=True)
        return total_folder

    @classmethod
    def _repository_folder_path(cls) -> str:
        return os.path.join(SARDINE_FOLDER_PATH, cls.REPOSITORY_FOLDER_NAME)

    @classmethod
    def get_repository_path(cls, repository_name: str) -> str:
        subnames = [name for name in cls.get_repository_name(repository_name).split('/') if name]
        total_folder = os.path.join(cls._repository_folder_path(), *subnames)
        return total_folder

    @classmethod
    @abstractmethod
    def repository_already_cloned(cls, repository_location: str):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_repository_name(cls, repository_name: str) -> str:
        raise NotImplementedError
