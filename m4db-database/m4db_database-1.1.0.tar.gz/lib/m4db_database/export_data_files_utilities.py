r"""
A collection of functions that export data files held in the 'file_store' directory structure.

@author L. Nagy, W. Williams
"""
import os
import shutil

from m4db_database.utilities import uid_to_dir

from m4db_database.sessions import get_session

from m4db_database.configuration import read_config_from_environ

from m4db_database.orm import Geometry
from m4db_database.orm import Model
from m4db_database.orm import NEB


def export_geometry_data_files_by_unique_id(dir_path, unique_ids=None, zipped=False, remove_geometry_dir=False):
    r"""
    Export geometry data files to a directory called 'geometry' in 'dir_path'.
    Args:
        dir_path: the destination path to export (copy) files to.
        unique_ids: the unique ids of geometries to copy.
        zipped: create a zipped version of the geometries.
        remove_geometry_dir: delete the original '<dir_path>/geometry' directory.

    Returns:
        None.

    """
    config = read_config_from_environ()
    geometry_src_dir = os.path.join(config["file_root"], "geometry")
    geometry_dst_dir = os.path.join(dir_path, "geometry")

    if unique_ids is None:
        session = get_session()
        unique_ids_list = [p[0] for p in session.query(Geometry.unique_id).all()]
    else:
        unique_ids_list = unique_ids

    for unique_id in unique_ids_list:
        geometry_src_data_dir = os.path.join(
            geometry_src_dir, uid_to_dir(unique_id)
        )
        geometry_dst_data_dir = os.path.join(
            geometry_dst_dir, uid_to_dir(unique_id)
        )

        os.makedirs(geometry_dst_data_dir, exist_ok=True)

        src_files = os.listdir(geometry_src_data_dir)

        for f in src_files:
            shutil.copy(os.path.join(geometry_src_data_dir, f), geometry_dst_data_dir)

    if zipped:
        shutil.make_archive(geometry_dst_dir, "zip", geometry_dst_dir)

    if remove_geometry_dir:
        shutil.rmtree(geometry_dst_dir)


def export_model_data_files_by_unique_id(dir_path, unique_ids=None, zipped=False, remove_model_dir=False):
    r"""
    Export model data files to a directory called 'model' in 'dir_path'.
    Args:
        dir_path: the destination path to export (copy) files to.
        unique_ids: the unique ids of models to copy.
        zipped: create a zipped version of the models.
        remove_model_dir: delete the original '<dir_path>/model' directory.

    Returns:
        None.

    """
    config = read_config_from_environ()
    model_src_dir = os.path.join(config["file_root"], "model")
    model_dst_dir = os.path.join(dir_path, "model")

    if unique_ids is None:
        session = get_session()
        unique_ids_list = [p[0] for p in session.query(Model.unique_id).all()]
    else:
        unique_ids_list = unique_ids

    for unique_id in unique_ids_list:
        model_src_data_dir = os.path.join(
            model_src_dir, uid_to_dir(unique_id)
        )
        model_dst_data_dir = os.path.join(
            model_dst_dir, uid_to_dir(unique_id)
        )

        os.makedirs(model_dst_data_dir, exist_ok=True)

        src_files = os.listdir(model_src_data_dir)

        for f in src_files:
            shutil.copy(os.path.join(model_src_data_dir, f), model_dst_data_dir)

    if zipped:
        shutil.make_archive(model_dst_dir, "zip", model_dst_dir)

    if remove_model_dir:
        shutil.rmtree(model_dst_dir)


def export_neb_data_files_by_unique_id(dir_path, unique_ids=None, zipped=False, remove_neb_dir=False):
    r"""
    Export NEB path data files to a directory called 'neb' in 'dir_path'.
    Args:
        dir_path: the destination path to export (copy) files to.
        unique_ids: the unique ids of NEB paths to copy.
        zipped: create a zipped version of the paths.
        remove_neb_dir: delete the original '<dir_path>/neb' directory.

    Returns:
        None.

    """
    config = read_config_from_environ()
    neb_path_src_dir = os.path.join(config["file_root"], "neb")
    neb_path_dst_dir = os.path.join(dir_path, "neb")

    if unique_ids is None:
        session = get_session()
        unique_ids_list = [p[0] for p in session.query(NEB.unique_id).all()]
    else:
        unique_ids_list = unique_ids

    for unique_id in unique_ids_list:
        neb_path_src_data_dir = os.path.join(
            neb_path_src_dir, uid_to_dir(unique_id)
        )
        neb_path_dst_data_dir = os.path.join(
            neb_path_dst_dir, uid_to_dir(unique_id)
        )

        os.makedirs(neb_path_dst_data_dir, exist_ok=True)

        src_files = os.listdir(neb_path_src_data_dir)

        for f in src_files:
            shutil.copy(os.path.join(neb_path_src_data_dir, f), neb_path_dst_data_dir)

    if zipped:
        shutil.make_archive(neb_path_dst_dir, "zip", neb_path_dst_dir)

    if remove_neb_dir:
        shutil.rmtree(neb_path_dst_dir)
