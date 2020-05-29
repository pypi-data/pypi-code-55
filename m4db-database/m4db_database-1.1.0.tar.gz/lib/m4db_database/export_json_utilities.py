r"""
A collection of useful utilities for export.

@author L. Nagy, W. Williams
"""
import json
import os

from sqlalchemy import tuple_

from m4db_database.sessions import get_session

from m4db_database.orm import DBUser, Project, RunningStatus
from m4db_database.orm import Software
from m4db_database.orm import Unit
from m4db_database.orm import PhysicalConstant
from m4db_database.orm import SizeConvention
from m4db_database.orm import AnisotropyForm
from m4db_database.orm import Geometry
from m4db_database.orm import Model
from m4db_database.orm import NEBCalculationType
from m4db_database.orm import NEB
from m4db_database.orm import Material


def export_db_user(dir_path, user_names=None, format_json=False):
    r"""
    Export users from the database to a file called 'db_user.json'.
    Args:
        dir_path: the directory location to which users are to be exported.
        user_names: the user names to export, if set to None all users will be exported.
        format_json: flag set to True if formatted JSON is required, otherwise false.

    Returns:
        None.
    """
    session = get_session()
    if user_names is None:
        db_users = session.query(DBUser).all()
    else:
        db_users = session.query(DBUser).filter(DBUser.user_name.in_(user_names))
    db_users_list = [db_user.as_dict() for db_user in db_users]

    db_users_file = os.path.join(dir_path, "db_user.json")
    with open(db_users_file, "w") as fout:
        if format_json:
            fout.write(json.dumps(db_users_list, indent=4, sort_keys=True))
        else:
            fout.write(json.dumps(db_users_list))
        fout.write("\n")


def export_software(dir_path, name_versions=None, format_json=False):
    r"""
    Export softwares from the database to a fille called 'software.json'.
    Args:
        dir_path: the directory location to which softwares are to be exported.
        name_versions: pairs of software names/version to export, if set to None all softwares will be exported.
        format_json: flag set to True if formatted JSON is required, otherwise false.

    Returns:
        None.
    """
    session = get_session()
    if name_versions is None:
        softwares = session.query(Software).all()
    else:
        softwares = session.query(Software).filter(tuple_(Software.name, Software.version).in_(name_versions)).all()
    softwares_list = [software.as_dict() for software in softwares]

    softwares_file = os.path.join(dir_path, "software.json")
    with open(softwares_file, "w") as fout:
        if format_json:
            fout.write(json.dumps(softwares_list, indent=4, sort_keys=True))
        else:
            fout.write(json.dumps(softwares_list))
        fout.write("\n")


def export_project(dir_path, names=None, format_json=False):
    r"""
    Export projects from the database to a file called 'project.json'.
    Args:
        dir_path: the directory location to which projects are to be exported.
        names: names of projects to export, if set to None all projects will be exported.
        format_json: flag set to True if formatted JSON is required, otherwise false.

    Returns:
        None.
    """
    session = get_session()
    if names is None:
        projects = session.query(Project).all()
    else:
        projects = session.query(Project).filter(Project.name.in_(names)).all()
    project_list = [project.as_dict() for project in projects]

    project_file = os.path.join(dir_path, "project.json")
    with open(project_file, "w") as fout:
        if format_json:
            fout.write(json.dumps(project_list, indent=4, sort_keys=True))
        else:
            fout.write(json.dumps(project_list))
        fout.write("\n")


def export_material(dir_path, name_temperture=None, format_json=False):
    r"""
    Export materials from the database to a file called 'material.json'.
    Args:
        dir_path: the directory location to which materials are to be exported.
        name_temperture: pairs of software names/version to export, if set to None all materials will be exported.
        format_json: flag set to True if formatted JSON is required, otherwise false.

    Returns:
        None.
    """
    session = get_session()
    if name_temperture is None:
        materials = session.query(Material).all()
    else:
        materials = session.query(Material).filter(tuple_(Material.name, Material.temperature).in_(name_temperture)).all()
    materials_list = [material.as_dict() for material in materials]

    materials_file = os.path.join(dir_path, "material.json")
    with open(materials_file, "w") as fout:
        if format_json:
            fout.write(json.dumps(materials_list, indent=4, sort_keys=True))
        else:
            fout.write(json.dumps(materials_list))
        fout.write("\n")


def export_unit(dir_path, symbols=None, format_json=False):
    r"""
    Export units from the database to a file called 'unit.json'.
    Args:
        dir_path: the directory location to which units are to be exported.
        symbols: the symbols of units to export, if set to None all units will be exported.
        format_json: flag set to True if formatted JSON is required, otherwise false.

    Returns:
        None.
    """
    session = get_session()
    if symbols is None:
        units = session.query(Unit).all()
    else:
        units = session.query(Unit).filter(Unit.symbol.in_(symbols))
    units_list = [unit.as_dict() for unit in units]

    units_file = os.path.join(dir_path, "unit.json")
    with open(units_file, "w") as fout:
        if format_json:
            fout.write(json.dumps(units_list, indent=4, sort_keys=True))
        else:
            fout.write(json.dumps(units_list))
        fout.write("\n")


def export_physical_constant(dir_path, symbols=None, format_json=False):
    r"""
    Export physical constants from the database to a file called 'physical_constant.json'.
    Args:
        dir_path: the directory location to which physical constants are to be exported.
        symbols: the symbols of physical constants to export, if set to None all constants will be exported.
        format_json: flag set to True if formatted JSON is required, otherwise false.

    Returns:
        None.
    """
    session = get_session()
    if symbols is None:
        constants = session.query(PhysicalConstant).all()
    else:
        constants = session.query(PhysicalConstant).filter(PhysicalConstant.symbol.in_(symbols))
    constants_list = [constant.as_dict() for constant in constants]

    constants_file = os.path.join(dir_path, "physical_constant.json")
    with open(constants_file, "w") as fout:
        if format_json:
            fout.write(json.dumps(constants_list, indent=4, sort_keys=True))
        else:
            fout.write(json.dumps(constants_list))
        fout.write("\n")


def export_size_convention(dir_path, symbols=None, format_json=False):
    r"""
    Export size conventions from the database to a file called 'size_convention.json'.
    Args:
        dir_path: the directory location to which size conventions are to be exported.
        symbols: the symbols of size conventions to export, if set to None all size conventions will be exported.
        format_json: flag set to True if formatted JSON is required, otherwise false.

    Returns:
        None.
    """
    session = get_session()
    if symbols is None:
        sconvs = session.query(SizeConvention).all()
    else:
        sconvs = session.query(SizeConvention).filter(SizeConvention.symbol.in_(symbols))
    sconvs_list = [sconv.as_dict() for sconv in sconvs]

    sconvs_file = os.path.join(dir_path, "size_convention.json")
    with open(sconvs_file, "w") as fout:
        if format_json:
            fout.write(json.dumps(sconvs_list, indent=4, sort_keys=True))
        else:
            fout.write(json.dumps(sconvs_list))
        fout.write("\n")


def export_anisotropy_form(dir_path, names=None, format_json=False):
    r"""
    Export anisotropy forms from the database to a file called 'anisotropy_form.json'.
    Args:
        dir_path: the directory location to which anisotropy forms are to be exported.
        names: the names of anisotropy forms to export, if set to None all anisotropy forms will be exported.
        format_json: flag set to True if formatted JSON is required, otherwise false.

    Returns:
        None.
    """
    session = get_session()
    if names is None:
        aforms = session.query(AnisotropyForm).all()
    else:
        aforms = session.query(AnisotropyForm).filter(AnisotropyForm.name.in_(names))
    aforms_list = [aforms.as_dict() for aforms in aforms]

    aforms_file = os.path.join(dir_path, "anisotropy_form.json")
    with open(aforms_file, "w") as fout:
        if format_json:
            fout.write(json.dumps(aforms_list, indent=4, sort_keys=True))
        else:
            fout.write(json.dumps(aforms_list))
        fout.write("\n")


def export_running_status(dir_path, names=None, format_json=False):
    r"""
    Export running statuses from the database to a file called 'running_status.json'.
    Args:
        dir_path: the directory location to which running statuses are to be exported.
        names: the names of running statuses to export, if set to None all anisotropy forms will be exported.
        format_json: flag set to True if formatted JSON is required, otherwise false.

    Returns:
        None.
    """
    session = get_session()
    if names is None:
        running_statuses = session.query(RunningStatus).all()
    else:
        running_statuses = session.query(RunningStatus).filter(RunningStatus.name.in_(names))
    running_status_dicts = [running_status.as_dict() for running_status in running_statuses]

    running_status_file = os.path.join(dir_path, "running_status.json")
    with open(running_status_file, "w") as fout:
        if format_json:
            fout.write(json.dumps(running_status_dicts, indent=4, sort_keys=True))
        else:
            fout.write(json.dumps(running_status_dicts))
        fout.write("\n")


def export_neb_calculation_type(dir_path, names=None, format_json=False):
    r"""
    Export NEB calculation types from the database to a file called 'neb_calculation_type.json'.
    Args:
        dir_path: the directory location to which NEB calculation types are to be exported.
        names: the names of NEB calculation types to export, if set to None all calculation types will be exported.
        format_json: flag set to True if formatted JSON is required, otherwise false.

    Returns:
        None.
    """
    session = get_session()
    if names is None:
        calc_types = session.query(NEBCalculationType).all()
    else:
        calc_types = session.query(NEBCalculationType).filter(NEBCalculationType.name.in_(names))
    calc_types_list = [aforms.as_dict() for aforms in calc_types]

    calc_types_file = os.path.join(dir_path, "neb_calculation_type.json")
    with open(calc_types_file, "w") as fout:
        if format_json:
            fout.write(json.dumps(calc_types_list, indent=4, sort_keys=True))
        else:
            fout.write(json.dumps(calc_types_list))
        fout.write("\n")


def export_geometry_by_unique_id(dir_path, unique_ids=None, format_json=False):
    r"""
    Export geometries from the database to a file called 'geometry.json'.
    Args:
        dir_path: the directory location to which geometry metadata is to be exported.
        unique_ids: the unique ids of geometries to export, if set to None all geometries will be exported.
        format_json: flag set to True if formatted JSON is required, otherwise false.

    Returns:
        None.
    """
    session = get_session()
    if unique_ids is None:
        geometries = session.query(Geometry).all()
    else:
        geometries = session.query(Geometry).filter(Geometry.unique_id.in_(unique_ids))
    geometries_list = [geometry.as_dict() for geometry in geometries]

    geometries_file = os.path.join(dir_path, "geometry.json")
    with open(geometries_file, "w") as fout:
        if format_json:
            fout.write(json.dumps(geometries_list, indent=4, sort_keys=True))
        else:
            fout.write(json.dumps(geometries_list))
        fout.write("\n")


def export_model_by_unique_id(dir_path, unique_ids=None, format_json=False):
    r"""
    Export models from the database to a file called 'model.json'.
    Args:
        dir_path: the directory location to which model metadata is to be exported.
        unique_ids: the unique ids of models to export, if set to None all models will be exported.
        format_json: flag set to True if formatted JSON is required, otherwise false.

    Returns:
        None.
    """
    session = get_session()
    if unique_ids is None:
        models = session.query(Model).all()
    else:
        models = session.query(Model).filter(Model.unique_id.in_(unique_ids))
    models_list = [model.as_dict() for model in models]

    models_file = os.path.join(dir_path, "model.json")
    with open(models_file, "w") as fout:
        if format_json:
            fout.write(json.dumps(models_list, indent=4, sort_keys=True))
        else:
            fout.write(json.dumps(models_list))
        fout.write("\n")


def export_neb_by_unique_id(dir_path, unique_ids=None, format_json=False):
    r"""
    Export NEB paths from the database to a file called 'neb.json'.
    Args:
        dir_path: the directory location to which NEB path metadata is to be exported.
        unique_ids: the unique ids of NEB paths to export, if set to None all paths will be exported.
        format_json: flag set to True if formatted JSON is required, otherwise false.

    Returns:
        None.
    """
    session = get_session()
    if unique_ids is None:
        neb_paths = session.query(NEB).all()
    else:
        neb_paths = session.query(NEB).filter(NEB.unique_id.in_(unique_ids))
    neb_paths_list = [model.as_dict() for model in neb_paths]

    neb_paths_file = os.path.join(dir_path, "neb.json")
    with open(neb_paths_file, "w") as fout:
        if format_json:
            fout.write(json.dumps(neb_paths_list, indent=4, sort_keys=True))
        else:
            fout.write(json.dumps(neb_paths_list))
        fout.write("\n")
