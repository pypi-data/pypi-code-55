from typing import Any

import yaml


def write_docs_to_yaml(filename: str, content: Any) -> None:
    """Write out the documents to yaml file.

    Parameters
    ----------
    filename : str
        The path to the yaml file.

    content : Any
        The data that can be dumped by safe_dump.
    """
    with open(filename, 'w') as f:
        yaml.safe_dump(content, f)
    return
