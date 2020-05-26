from jsonschema_cli.handlers import handle_file_uri
from jsonschema import RefResolver
import os


def relative_path_resolver(base_path=os.getcwd()):
    handler = handle_file_uri(base_path)
    ref_handlers = {"": handler}
    return RefResolver("", {}, handlers=ref_handlers)
