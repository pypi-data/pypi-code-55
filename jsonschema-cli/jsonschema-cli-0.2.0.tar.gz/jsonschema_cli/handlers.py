"""

"""
import os
import pathlib
from urllib.parse import urlparse

from jsonschema_cli.load import load_file


def handle_file_uri(schema_path: pathlib.Path):
    def resolver(uri: str):
        parsed_uri = urlparse(uri)

        if parsed_uri.path.startswith("/"):
            file_path = pathlib.Path(uri).absolute()

        path = schema_path.parent
        file_path = pathlib.Path(path).joinpath(pathlib.Path(uri)).absolute()

        return load_file(str(file_path))

    return resolver
