r"""
A collection of functions to help when importing file store data files.

@author L. Nagy, W. Williams
"""
import os
import shutil

from m4db_database.configuration import read_config_from_environ


def extract_zip_to_file_root(zip_file):
    r"""
    Extracts the zip file to the file root held in the M4DB_CONFIG configuration file.
    Args:
        zip_file: path to the zip file which is to be extracted.

    Returns:
        None.

    """
    environ = read_config_from_environ()

    file_name, file_ext = os.path.splitext(os.path.basename(zip_file))

    destination_dir = os.path.join(environ["file_root"], file_name)
    if not os.path.isdir(destination_dir):
        os.makedirs(destination_dir, exist_ok=True)

    shutil.unpack_archive(zip_file, destination_dir, "zip")
