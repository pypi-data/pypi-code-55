import json
import os

from sardine.config import SARDINE_RC_PATH
from sardine.resolvers.manifest.base import BaseManifestResolver
from sardine.exceptions.manifest_not_found import ManifestNotFound


class LocalManifestResolver(BaseManifestResolver):

    @classmethod
    def manifest_exists(cls) -> bool:
        return os.path.isfile(cls._manifest_path())

    @classmethod
    def create_directories(cls) -> None:
        os.makedirs(SARDINE_RC_PATH.split(os.sep)[:-1], exist_ok=True)

    @classmethod
    def _load_manifest(cls) -> str:
        try:
            with open(cls._manifest_path()) as manifest_file:
                return manifest_file.read()
        except FileNotFoundError as file_not_found_error:
            raise ManifestNotFound(cls._manifest_path()) from file_not_found_error

    @classmethod
    def _manifest_path(cls) -> str:
        return SARDINE_RC_PATH
