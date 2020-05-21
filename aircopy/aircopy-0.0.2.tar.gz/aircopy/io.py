from typing import Any

from ruamel.yaml import YAML

# regolith style yaml loader
RG_LOADER = YAML()
RG_LOADER.indent(mapping=2, sequence=4, offset=2)


def write_docs_to_yaml(filename: str, content: Any, loader=RG_LOADER) -> None:
    """Write out the documents to yaml file.

    Parameters
    ----------
    filename : str
        The path to the yaml file.

    content : Any
        The data that can be dumped by safe_dump.

    loader : YAML
        The loader to dump to yaml. It must have method 'dump'.
    """
    with open(filename, 'w') as f:
        loader.dump(content, f)
    return
