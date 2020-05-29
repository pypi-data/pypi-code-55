import os

import yaml


def read_config_from_file(file_name):
    r"""
    Reads an M4DB database configuration from a file.
    Args:
        file_name: the M4DB configuration file.

    Returns:
        A python dictionary representation of M4DB database related configuration information.

    """
    with open(file_name, "r") as fin:
        config = yaml.load(fin, Loader=yaml.FullLoader)

    return config


def read_config_from_environ():
    r"""
    Reads an M4DB database configuration by checking for an environment variable called 'M4DB_CONF_DATABASE".

    db_url: the database URL

    Returns:
        A python dictionary representation of M4DB database related configuration information.

    """
    file_name = os.environ.get("M4DB_CONFIG")

    if file_name is None:
        raise ValueError("M4DB_CONFIG environment variable doesn't exist")

    return read_config_from_file(file_name)


def write_config_to_file(file_name, config):
    r"""
    Writes M4DB database configuration.

    file_name: the file name to write configuration data to.
    config: A python dictionary representation of M4DB database related configuration information.

    Returns:
        None.

    """
    with open(file_name, "w") as fout:
        yaml.dump(config, fout, default_flow_style=False)
