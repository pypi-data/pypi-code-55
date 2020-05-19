r"""
A set of utility functions that will allow the user to import data that is stored in a simple tabular data format,
(referred to as a 'table file') for example the 'unit.dat' file looks like this:

id | symbol |    name    | power |       last_modified        |          created
----+--------+------------+-------+----------------------------+----------------------------
  1 | 1      | unitless   |     1 | 2019-04-27 01:45:16.563754 | 2019-04-27 01:45:16.563804
  2 | m      | meter      |     1 | 2019-04-27 01:45:16.563754 | 2019-04-27 01:45:16.563804
  3 | cm     | centimeter |  0.01 | 2019-04-27 01:45:16.563754 | 2019-04-27 01:45:16.563804
  4 | mm     | millimeter | 0.001 | 2019-04-27 01:45:16.563754 | 2019-04-27 01:45:16.563804
  5 | um     | micrometer | 1e-06 | 2019-04-27 01:45:16.563754 | 2019-04-27 01:45:16.563804
  6 | nm     | nanometer  | 1e-09 | 2019-04-27 01:45:16.563754 | 2019-04-27 01:45:16.563804
  7 | pm     | picometer  | 1e-12 | 2019-04-27 01:45:16.563754 | 2019-04-27 01:45:16.563804
  8 | fm     | femtometer | 1e-15 | 2019-04-27 01:45:16.563754 | 2019-04-27 01:45:16.563804
  9 | am     | attometer  | 1e-18 | 2019-04-27 01:45:16.563754 | 2019-04-27 01:45:16.563804
 10 | T      | tesla      |     1 | 2019-04-27 01:45:16.563754 | 2019-04-27 01:45:16.563804
 11 | mT     | millitesla | 0.001 | 2019-04-27 01:45:16.563754 | 2019-04-27 01:45:16.563804
 12 | uT     | microtesla | 1e-06 | 2019-04-27 01:45:16.563754 | 2019-04-27 01:45:16.563804
 13 | nT     | nanotesla  | 1e-09 | 2019-04-27 01:45:16.563754 | 2019-04-27 01:45:16.563804
 14 | pT     | picotesla  | 1e-12 | 2019-04-27 01:45:16.563754 | 2019-04-27 01:45:16.563804
 15 | fT     | femtotesla | 1e-15 | 2019-04-27 01:45:16.563754 | 2019-04-27 01:45:16.563804
 16 | aT     | attotesla  | 1e-18 | 2019-04-27 01:45:16.563754 | 2019-04-27 01:45:16.563804

@file utilities.py
@author L. Nagy, W. Williams
"""
import pandas as pd
from decimal import Decimal

from sqlalchemy import or_

from m4db_database.orm import AnisotropyForm
from m4db_database.orm import DBUser
from m4db_database.orm import Material
from m4db_database.orm import Software
from m4db_database.orm import Project
from m4db_database.orm import SizeConvention
from m4db_database.orm import Unit
from m4db_database.orm import RunningStatus
from m4db_database.orm import PhysicalConstant
from m4db_database.orm import Metadata
from m4db_database.orm import NEBCalculationType
from m4db_database.orm import Geometry
from m4db_database.orm import Model
from m4db_database.orm import ModelMaterialAssociation
from m4db_database.orm import ModelRunData
from m4db_database.orm import ModelReportData
from m4db_database.orm import RandomField
from m4db_database.orm import NEB
from m4db_database.orm import NEBRunData
from m4db_database.orm import NEBReportData


def string_to_bool(str):
    r"""
    Function to convert boolean strings to Python boolean values.
    Args:
        str: the input string.

    Returns: the boolean version of str

    """
    if str.lower() in ["true", "t"]:
        return True
    elif str.lower() in ["false", "f"]:
        return False
    else:
        raise ValueError("Can't interpret '{}' as boolean".format(str))


def import_metadatas(table_file, session):
    r"""
    Imports the metadata form data from a table file.
    Args:
        table_file: the file containing table information.
        session: the database session.

    Returns:
        None.
    """
    with open(table_file, "r") as fin:
        for line_no, line in enumerate(fin):
            line = line.strip()
            if line_no >= 2:
                values = [v.strip() for v in line.split('|')]
                db_user = session.query(DBUser).filter(DBUser.user_name == values[4]).one()
                project = session.query(Project).filter(Project.name == values[3]).one()
                software = session.query(Software).filter(Software.name == values[5]). \
                    filter(Software.version == values[6]).one()
                metadata = Metadata(
                    project=project,
                    db_user=db_user,
                    software=software
                )
                session.add(metadata)
                session.commit()


def import_anisotropy_forms(table_file, session):
    r"""
    Imports the anisotropy form data from a table file.
    Args:
        table_file: the file containing table information.
        session: the database session.

    Returns:
        None.
    """
    with open(table_file, "r") as fin:
        for line_no, line in enumerate(fin):
            line = line.strip()
            if line_no >= 2:
                values = [v.strip() for v in line.split('|')]
                anis_form = AnisotropyForm(
                    name=values[1],
                    description=values[2]
                )
                session.add(anis_form)
                session.commit()


def import_db_users(table_file, session):
    r"""
    Imports the database user data from a table file.
    Args:
        table_file: the file containing table information.
        session: the database session.

    Returns:
        None.

    """
    with open(table_file, "r") as fin:
        for line_no, line in enumerate(fin):
            line = line.strip()
            if line_no >= 2:
                values = [v.strip() for v in line.split('|')]
                db_user = DBUser(
                    user_name=values[1],
                    first_name=values[2],
                    initials=values[3],
                    surname=values[4],
                    email=values[5],
                    telephone=values[6]
                )
                session.add(db_user)
                session.commit()


def import_softwares(table_file, session):
    r"""
    Imports the database softwares data from a table file.
    Args:
        table_file: the file containing table information.
        session: the database session.

    Returns:
        None.

    """
    with open(table_file, "r") as fin:
        for line_no, line in enumerate(fin):
            line = line.strip()
            if line_no >= 2:
                values = [v.strip() for v in line.split('|')]
                software = Software(
                    name=values[1],
                    version=values[2],
                    description=values[3],
                    url=values[4],
                    citation=values[5],
                )
                session.add(software)
                session.commit()


def import_sizeconvention(table_file, session):
    r"""
    Imports the database size convention data from a table file.
    Args:
        table_file: the file containing table information.
        session: the database session.

    Returns:
        None.

    """
    with open(table_file, "r") as fin:
        for line_no, line in enumerate(fin):
            line = line.strip()
            if line_no >= 2:
                values = [v.strip() for v in line.split('|')]
                sizeconvention = SizeConvention(
                    symbol=values[1],
                    description=values[2]
                )
                session.add(sizeconvention)
                session.commit()


def import_running_status(table_file, session):
    r"""
    Imports the database running status data from a table file.
    Args:
        table_file: the file containing table information.
        session: the database session.

    Returns:
        None.

    """
    with open(table_file, "r") as fin:
        for line_no, line in enumerate(fin):
            line = line.strip()
            if line_no >= 2:
                values = [v.strip() for v in line.split('|')]
                runningstatus = RunningStatus(
                    name=values[1],
                    description=values[2]
                )
                session.add(runningstatus)
                session.commit()


def import_physical_constants(table_file, session):
    r"""
    Imports the database physical constants data from a table file.
    Args:
        table_file: the file containing table information.
        session: the database session.

    Returns:
        None.

    """
    with open(table_file, "r") as fin:
        for line_no, line in enumerate(fin):
            line = line.strip()
            if line_no >= 2:
                values = [v.strip() for v in line.split('|')]
                physicalconstant = PhysicalConstant(
                    symbol=values[1],
                    name=values[2],
                    value=values[3],
                    unit=values[4]
                )
                session.add(physicalconstant)
                session.commit()


def import_unit(table_file, session):
    r"""
    Imports the database softwares data from a table file.
    Args:
        table_file: the file containing table information.
        session: the database session.

    Returns:
        None.

    """
    with open(table_file, "r") as fin:
        for line_no, line in enumerate(fin):
            line = line.strip()
            if line_no >= 2:
                values = [v.strip() for v in line.split('|')]
                unit = Unit(
                    symbol=values[1],
                    name=values[2],
                    power=values[3]
                )
                session.add(unit)
                session.commit()


def import_projects(table_file, session):
    r"""
    Imports the database projects data from a table file.
    Args:
        table_file: the file containing table information.
        session: the database session.

    Returns:
        None.

    """
    with open(table_file, "r") as fin:
        for line_no, line in enumerate(fin):
            line = line.strip()
            if line_no >= 2:
                values = [v.strip() for v in line.split('|')]
                project = Project(
                    name=values[1],
                    description=values[2]
                )
                session.add(project)
                session.commit()


def import_materials(table_file, session):
    r"""
    Imports the material data from a table file.
    Args:
        table_file: the file containing table information.
        session: the database session.

    Returns:
        None.

    """
    with open(table_file, "r") as fin:
        # Retrieve the anisotropy form that materials belong to.
        anis_form = session.query(AnisotropyForm). \
            filter(AnisotropyForm.name == "cubic"). \
            one()
        for line_no, line in enumerate(fin):
            line = line.strip()
            if line_no >= 2:
                values = [v.strip() for v in line.split('|')]
                material = Material(
                    name=values[1],
                    temperature=float(values[2]),
                    k1=float(values[3]),
                    aex=float(values[4]),
                    ms=float(values[5]),
                    kd=float(values[6]),
                    lambda_ex=float(values[7]) if values[7] != "" else None,
                    q_hardness=float(values[8]) if values[8] != "" else None,
                    axis_theta=float(values[9]) if values[9] != "" else None,
                    axis_phi=float(values[10]) if values[10] != "" else None,
                    anisotropy_form=anis_form
                )
                session.add(material)
                session.commit()


def import_neb_calculation_types(table_file, session):
    r"""
    Imports the calculation type data from a table file.
    Args:
        table_file: the file containing table information.
        session: the database session.

    Returns:
        None.

    """
    with open(table_file, "r") as fin:
        # Retrieve the calculation type.
        for line_no, line in enumerate(fin):
            line = line.strip()
            if line_no >= 2:
                values = [v.strip() for v in line.split('|')]
                neb_calc_type = NEBCalculationType(
                    name=values[1],
                    description=values[2]
                )
                session.add(neb_calc_type)
                session.commit()


def import_geometries(table_file, session):
    r"""
    Imports the geometry data from a table file.
    Args:
        table_file: the file containing table information.
        session: the database session.

    Returns:
        None.

    """
    with open(table_file, "r") as fin:
        # Retrieve the calculation type.
        for line_no, line in enumerate(fin):
            line = line.strip()
            if line_no >= 2:
                values = [v.strip() for v in line.split('|')]

                size_convention = session.query(SizeConvention). \
                    filter(SizeConvention.symbol == values[9]).one()

                size_unit = session.query(Unit). \
                    filter(Unit.symbol == values[10]).one()

                software = session.query(Software). \
                    filter(Software.name == values[11]). \
                    filter(Software.version == values[12]).one()

                geometry = Geometry(
                    has_exodus=string_to_bool(values[0]),
                    has_mesh_gen_output=string_to_bool(values[1]),
                    has_mesh_gen_script=string_to_bool(values[2]),
                    has_patran=string_to_bool(values[3]),
                    name=values[4],
                    nelements=int(values[5]),
                    nsubmeshes=int(values[6]),
                    nvertices=int(values[7]),
                    size=Decimal(values[8]),
                    size_convention=size_convention,
                    size_unit=size_unit,
                    software=software,
                    unique_id=values[13]
                )

                session.add(geometry)
                session.commit()


def import_models(table_file, session):
    r"""
    Imports the model data from a table file.
    Args:
        table_file: the file containing table information.
        session: the database session.

    Returns:
        None.

    """
    with open(table_file, "r") as fin:
        # Retrieve the calculation type.
        for line_no, line in enumerate(fin):
            line = line.strip()
            if line_no >= 2:
                values = [v.strip() for v in line.split('|')]

                geometry = session.query(Geometry). \
                    filter(Geometry.unique_id == values[10]).one()

                material = session.query(Material). \
                    filter(Material.name == values[12]). \
                    filter(Material.temperature == Decimal(values[13])).one()

                user = session.query(DBUser). \
                    filter(DBUser.user_name == values[15]).one()

                project = session.query(Project). \
                    filter(Project.name == values[16]).one()

                software = session.query(Software). \
                    filter(Software.name == values[17]). \
                    filter(Software.version == values[18]).one()

                metadata = Metadata(
                    db_user=user,
                    project=project,
                    software=software
                )

                running_status = session.query(RunningStatus). \
                    filter(RunningStatus.name == values[22]).one()

                random_field = RandomField()

                model_run_data = ModelRunData()

                model_report_data = ModelReportData()

                model = Model(
                    adm_tot=float(values[0]),
                    e_anis=float(values[1]),
                    e_demag=float(values[2]),
                    e_exch1=float(values[3]),
                    e_exch2=float(values[4]),
                    e_exch3=float(values[5]),
                    e_exch4=float(values[6]),
                    e_ext=float(values[7]),
                    e_tot=float(values[8]),
                    e_typical=float(values[9]),
                    geometry=geometry,
                    h_tot=float(values[11]),
                    max_energy_evaluations=int(values[14]),
                    mdata=metadata,
                    mx_tot=float(values[19]),
                    my_tot=float(values[20]),
                    mz_tot=float(values[21]),
                    running_status=running_status,
                    unique_id=values[23],
                    vx_tot=float(values[24]),
                    vy_tot=float(values[25]),
                    vz_tot=float(values[26]),
                    start_magnetization=random_field,
                    model_run_data=model_run_data,
                    model_report_data=model_report_data
                )

                mmassoc = ModelMaterialAssociation(index=1)
                mmassoc.material = material
                model.materials.append(mmassoc)

                session.add(model)
                session.commit()


def import_nebs(table_file, session):
    r"""
    Imports the neb data from a table file.
    Args:
        table_file: the file containing table information.
        session: the database session.

    Returns:
        None.

    """
    with open(table_file, "r") as fin:
        # Retrieve the calculation type.
        for line_no, line in enumerate(fin):
            line = line.strip()
            if line_no >= 2:
                values = [v.strip() for v in line.split('|')]

                user = session.query(DBUser). \
                    filter(DBUser.user_name == values[5]).one()

                project = session.query(Project). \
                    filter(Project.name == values[6]).one()

                software = session.query(Software). \
                    filter(Software.name == values[7]). \
                    filter(Software.version == values[8]).one()

                metadata = Metadata(
                    db_user=user,
                    project=project,
                    software=software
                )

                running_status = session.query(RunningStatus). \
                    filter(RunningStatus.name == values[11]).one()

                neb_calculation_type = session.query(NEBCalculationType). \
                    filter(NEBCalculationType.name == values[9]).one()

                end_model = session.query(Model). \
                    filter(Model.unique_id == values[2]).one()

                start_model = session.query(Model). \
                    filter(Model.unique_id == values[1]).one()

                neb_run_data = NEBRunData()
                neb_report_data = NEBReportData()

                neb = NEB(
                    unique_id=values[13],
                    spring_constant=float(values[12]),
                    running_status=running_status,
                    no_of_points=int(values[10]),
                    neb_calculation_type=neb_calculation_type,
                    mdata=metadata,
                    max_path_evaluations=int(values[4]),
                    max_energy_evaluations=int(values[3]),
                    end_model=end_model,
                    start_model=start_model,
                    curvature_weight=float(values[0]),
                    neb_run_data=neb_run_data,
                    neb_report_data=neb_report_data
                )

                session.add(neb)
                session.commit()


def models_list_as_table(models: list):
    r"""
    Convert a list of SQLAlchemy Model objects to a tabular format.
    Args:
        models: a list of SQLAlchemy NEB objects..

    Returns:
        A dictionary/table of NEB data

    """
    table = {
        "unique_id": [],
        "mx_tot": [],
        "my_tot": [],
        "mz_tot": [],
        "vx_tot": [],
        "vy_tot": [],
        "vz_tot": [],
        "adm_tot": [],
        "e_typical": [],
        "e_anis": [],
        "e_ext": [],
        "e_demag": [],
        "e_exch1": [],
        "e_exch2": [],
        "e_exch3": [],
        "e_exch4": [],
        "e_tot": [],
        "max_energy_evaluations": [],

        "geometry_unique_id": [],

        # We add additional columns for each material, later

        # Start magnetization, can be "RandomField", "ModelField" or "UniformField" (NOTE: "FileField" is deprecated).
        "start_magnetization_type": [],
        "start_magnetization_model_field_unique_id": [],
        "start_magnetization_uniform_field_dir_x": [],
        "start_magnetization_uniform_field_dir_y": [],
        "start_magnetization_uniform_field_dir_z": [],
        "start_magnetization_uniform_field_mag": [],
        "start_magnetization_uniform_field_unit_symbol": [],

        # External field magnetization, can be "RandomField" (not recommended), "ModelField" (not recommended) or
        # "UniformField" (NOTE: "FileField" is deprecated).
        "external_field_type": [],
        "external_model_field_unique_id": [],  # is set if field type is 'model'
        "external_uniform_field_dir_x": [],  # is set if field type is 'uniform'
        "external_uniform_field_dir_y": [],  # is set if field type is 'uniform'
        "external_uniform_field_dir_z": [],  # is set if field type is 'uniform'
        "external_uniform_field_mag": [],  # is set if field type is 'uniform'
        "external_uniform_field_unit_symbol": [],  # is set if field type is 'uniform'

        "running_status": [],

        "model_run_data_has_script": [],
        "model_run_data_has_stdout": [],
        "model_run_data_has_stderr": [],
        "model_run_data_has_energy_log": [],
        "model_run_data_has_tecplot": [],
        "model_run_data_has_neb_energies": [],

        "model_report_data_has_x_thumb_png": [],
        "model_report_data_has_y_thumb_png": [],
        "model_report_data_has_z_thumb_png": [],
        "model_report_data_has_x_png": [],
        "model_report_data_has_y_png": [],
        "model_report_data_has_z_png": [],

        "metadata_db_user_name": [],
        "metadata_project_name": [],
        "metadata_software_name": [],
        "metadata_software_version": [],

        "legacy_model_info_index": []
    }

    # Here we handle materials.
    nmaterials = 0
    material_idx = 0
    for model in models:
        if nmaterials < len(model.materials):
            table["material{}_name".format(material_idx)] = []
            table["material{}_temperature".format(material_idx)] = []
            table["material{}_k1".format(material_idx)] = []
            table["material{}_a".format(material_idx)] = []
            table["material{}_ms".format(material_idx)] = []
            table["material{}_lambda_ex".format(material_idx)] = []
            table["material{}_q_hardness".format(material_idx)] = []
            table["material{}_index".format(material_idx)] = []
            nmaterials = len(model.materials)
            material_idx = material_idx + 1

    # Here we populate the table
    for model in models:
        table["unique_id"].append(model.unique_id)
        table["mx_tot"].append(model.mx_tot)
        table["my_tot"].append(model.my_tot)
        table["mz_tot"].append(model.mz_tot)
        table["vx_tot"].append(model.vx_tot)
        table["vy_tot"].append(model.vy_tot)
        table["vz_tot"].append(model.vz_tot)
        table["adm_tot"].append(model.adm_tot)
        table["e_typical"].append(model.e_typical)
        table["e_anis"].append(model.e_anis)
        table["e_ext"].append(model.e_ext)
        table["e_demag"].append(model.e_demag)
        table["e_exch1"].append(model.e_exch1)
        table["e_exch2"].append(model.e_exch2)
        table["e_exch3"].append(model.e_exch3)
        table["e_exch4"].append(model.e_exch4)
        table["e_tot"].append(model.e_tot)
        table["max_energy_evaluations"].append(model.max_energy_evaluations)

        # Adding the geometry
        table["geometry_unique_id"].append(model.geometry.unique_id)

        # Adding the start magnetization
        if model.start_magnetization.type == "random_field":
            table["start_magnetization_type"].append(model.start_magnetization.type)
        if model.start_magnetization.type == "model_field":
            table["start_magnetization_type"].append(model.start_magnetization.type)
            table["start_magnetization_model_field_unique_id"].append(model.start_magnetization.model.unique_id)
        if model.start_magnetization.type == "uniform_field":
            table["start_magnetization_type"].append(model.start_magnetization.type)
            table["start_magnetization_uniform_field_dir_x"].append(model.start_magnetization.dir_x)
            table["start_magnetization_uniform_field_dir_y"].append(model.start_magnetization.dir_y)
            table["start_magnetization_uniform_field_dir_z"].append(model.start_magnetization.dir_z)
            table["start_magnetization_uniform_field_mag"].append(model.start_magnetization.mag)
            table["start_magnetization_uniform_field_unit_symbol"].append(model.start_magnetization.unit.symbol)

        # Adding the external field magnetization
        if model.external_field.type == "random_field":
            table["external_field_type"].append(model.external_field.type)
        if model.external_field.type == "model_field":
            table["external_field_type"].append(model.external_field.type)
            table["external_field_model_field_unique_id"].append(model.external_field.model.unique_id)
        if model.external_field.type == "uniform_field":
            table["external_field_type"].append(model.external_field.type)
            table["external_field_uniform_field_dir_x"].append(model.external_field.dir_x)
            table["external_field_uniform_field_dir_y"].append(model.external_field.dir_y)
            table["external_field_uniform_field_dir_z"].append(model.external_field.dir_z)
            table["external_field_uniform_field_mag"].append(model.external_field.mag)
            table["external_field_uniform_field_unit_symbol"].append(model.external_field.unit.symbol)

        table["running_status"].append(model.running_status.name)

        # Adding model run data
        table["model_run_data_has_script"].append(model.model_run_data.has_script)
        table["model_run_data_has_stdout"].append(model.model_run_data.has_stdout)
        table["model_run_data_has_stderr"].append(model.model_run_data.has_stderr)
        table["model_run_data_has_energy_log"].append(model.model_run_data.has_energy_log)
        table["model_run_data_has_tecplot"].append(model.model_run_data.has_tecplot)
        table["model_run_data_has_neb_energies"].append(model.model_run_data.has_neb_energies)

def nebs_list_as_table(nebs: list):
    r"""
    Convert a list of SQLAlchemy NEB objects to a tabular format.
    Args:
        nebs: a list of SQLAlchemy NEB objects..

    Returns:
        A dictionary/table of NEB data

    """
    # Create a dictionary with the necessary data to construct a complete output.
    table = {
        "unique_id": [],
        "spring_constant": [],
        "curvature_weight": [],
        "no_of_points": [],
        "max_energy_evaluations": [],
        "max_path_evaluations": [],

        "external_field_type": [],
        "external_model_field_unique_id": [],  # is set if field type is 'model'
        "external_uniform_field_dir_x": [],  # is set if field type is 'uniform'
        "external_uniform_field_dir_y": [],  # is set if field type is 'uniform'
        "external_uniform_field_dir_z": [],  # is set if field type is 'uniform'
        "external_uniform_field_mag": [],  # is set if field type is 'uniform'
        "external_uniform_field_unit_symbol": [],  # is set if field type is 'uniform'

        "start_model_unique_id": [],
        "end_model_unique_id": [],
        "parent_unique_id": [],
        "calculation_type_name": [],

        "neb_run_data_has_script": [],
        "neb_run_data_has_stdout": [],
        "neb_run_data_has_stderr": [],
        "neb_run_data_has_energy_log": [],
        "neb_run_data_has_tecplot": [],
        "neb_run_data_has_neb_energies": [],

        "neb_report_data_has_x_thumb_png": [],
        "neb_report_data_has_y_thumb_png": [],
        "neb_report_data_has_z_thumb_png": [],
        "neb_report_data_has_x_png": [],
        "neb_report_data_has_y_png": [],
        "neb_report_data_has_z_png": [],

        "metadata_db_user_name": [],
        "metadata_project_name": [],
        "metadata_software_name": [],
        "metadata_software_version": [],

        "running_status_name": []
    }

    for neb in nebs:
        table["unique_id"].append(neb.unique_id)
        table["spring_constant"].append(neb.spring_constant)
        table["curvature_weight"].append(neb.curvature_weight)
        table["no_of_points"].append(neb.no_of_points)
        table["max_energy_evaluations"].append(neb.max_path_evaluations)
        table["max_path_evaluations"].append(neb.max_path_evaluations)

        if neb.external_field.type == "model_field":
            table["external_field_type"].append(neb.external_field.type)
            table["external_model_field_unique_id"].append(neb.external_field.unique_id)
        elif neb.external_field.type == "random_field":
            table["external_field_type"].append(neb.external_field.type)
        elif neb.external_field.type == "uniform_field":
            table["external_field_type"].append(neb.external_field.type)
            table["external_uniform_field_dir_x"].append(neb.external_field.dir_x)
            table["external_uniform_field_dir_y"].append(neb.external_field.dir_y)
            table["external_uniform_field_dir_z"].append(neb.external_field.dir_z)
            table["external_uniform_field_dir_mag"].append(neb.external_field.dir_mag)
            table["external_uniform_field_dir_unit_symbol"].append(neb.external_field.unit_symbol)
        elif neb.external_field.type == "file_field":
            print("Warning NEB path '{}' uses deprecated FileField".format(neb.unique_id))
            continue
        else:
            raise ValueError("Unknown field type '{}'".format(neb.external_field.type))

        table["start_model_unique_id"].append(neb.start_model.unique_id)
        table["end_model_unique_id"].append(neb.end_model.unique_id)

        if neb.parent_neb is not None:
            table["parent_unique_id"].append(neb.parent_neb.unique_id)

        table["calculation_type_name"].append(neb.neb_calculation_type.name)

        table["neb_run_data_has_script"].append(neb.neb_run_data.has_script)
        table["neb_run_data_has_stdout"].append(neb.neb_run_data.has_stdout)
        table["neb_run_data_has_stderr"].append(neb.neb_run_data.has_stderr)
        table["neb_run_data_has_energy_log"].append(neb.neb_run_data.has_energy_log)
        table["neb_run_data_has_tecplot"].append(neb.neb_run_data.has_tecplot)
        table["neb_run_data_has_neb_energies"].append(neb.neb_run_data.has_neb_energies)

        table["neb_report_data_has_x_thumb_png"].append(neb.neb_report_data.has_x_thumb_png)
        table["neb_report_data_has_y_thumb_png"].append(neb.neb_report_data.has_y_thumb_png)
        table["neb_report_data_has_z_thumb_png"].append(neb.neb_report_data.has_z_thumb_png)
        table["neb_report_data_has_x_png"].append(neb.neb_report_data.has_x_png)
        table["neb_report_data_has_y_png"].append(neb.neb_report_data.has_y_png)
        table["neb_report_data_has_z_png"].append(neb.neb_report_data.has_z_png)

        table["metadata_db_user_name"].append(neb.metadata.db_user.user_name)
        table["metadata_project_name"].append(neb.metadata.project.name)
        table["metadata_software_name"].append(neb.metadata.software.name)
        table["metadata_software_version"].append(neb.metadata.software.version)

        table["running_status_name"].append(neb.running_status.name)

    return table
