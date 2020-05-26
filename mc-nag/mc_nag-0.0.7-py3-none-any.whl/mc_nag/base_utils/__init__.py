"""General utilities for mc-nag."""


def read_template_file(file_path):
    """Read contents of template file."""
    with open(file_path) as file_handle:
        return file_handle.read()


def find_key_in_structure(key, struct):
    """Search a structure for the given key.

    https://stackoverflow.com/a/29652561
    """
    if isinstance(struct, dict):
        for subkey, subvalue in struct.items():
            if subkey == key:
                yield subvalue
            for result in find_key_in_structure(key, subvalue):
                yield result
    elif isinstance(struct, list):
        for item in struct:
            for result in find_key_in_structure(key, item):
                yield result
