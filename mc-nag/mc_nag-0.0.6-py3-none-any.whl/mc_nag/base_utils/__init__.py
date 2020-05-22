"""General utilities for mc-nag."""


def read_template_file(file_path):
    """Read contents of template file."""
    with open(file_path) as file_handle:
        return file_handle.read()
