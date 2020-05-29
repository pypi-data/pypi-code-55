r"""
A collection of utilities to import data from json files.
"""
import json

from datetime import datetime

from m4db_database.dependency_importer import DependencyImporter

from m4db_database.orm import DBUser
from m4db_database.orm import RandomField
from m4db_database.orm import UniformField
from m4db_database.orm import ModelField
from m4db_database.orm import RunningStatus
from m4db_database.orm import ModelRunData
from m4db_database.orm import ModelReportData
from m4db_database.orm import Project
from m4db_database.orm import Metadata
from m4db_database.orm import LegacyModelInfo
from m4db_database.orm import ModelMaterialAssociation
from m4db_database.orm import Software
from m4db_database.orm import Unit
from m4db_database.orm import PhysicalConstant
from m4db_database.orm import SizeConvention
from m4db_database.orm import AnisotropyForm
from m4db_database.orm import Geometry
from m4db_database.orm import Material
from m4db_database.orm import NEBCalculationType
from m4db_database.orm import NEBRunData
from m4db_database.orm import NEBReportData
from m4db_database.orm import Model
from m4db_database.orm import NEB

from m4db_database.orm import DATE_TIME_FORMAT


def import_db_user(db_user_file, session, original_dates=True):
    r"""
    Import DBUser objects stored as JSON in a file.
    Args:
        db_user_file: the file name storing DBUser JSON data.
        session: the database session to which database users are to be added.
        original_dates: flag indicating that the original dates of the import should be used.

    Returns:
        None.
    """
    with open(db_user_file, "r") as fin:
        db_user_dicts = json.load(fin)

    for db_user_dict in db_user_dicts:
        db_user = DBUser(
            user_name=db_user_dict["user_name"],
            first_name=db_user_dict["first_name"],
            initials=db_user_dict["initials"],
            surname=db_user_dict["surname"],
            email=db_user_dict["email"],
            telephone=db_user_dict["telephone"]
        )

        if original_dates:
            db_user.last_modified = datetime.strptime(db_user_dict["last_modified"], DATE_TIME_FORMAT)
            db_user.created = datetime.strptime(db_user_dict["created"], DATE_TIME_FORMAT)

        session.add(db_user)

    session.commit()


def import_software(software_file, session, original_dates=True):
    r"""
    Import Software objects stored as JSON in a file.
    Args:
        software_file: the file name storing Software JSON data.
        session: the database session to which software items are to be added.
        original_dates: flag indicating that the original dates of the import should be used.

    Returns:
        None.
    """
    with open(software_file, "r") as fin:
        software_dicts = json.load(fin)

    for software_dict in software_dicts:
        software = Software(
            name=software_dict["name"],
            version=software_dict["version"],
            description=software_dict["description"],
            url=software_dict["url"],
            citation=software_dict["citation"],
        )

        if original_dates:
            software.last_modified = datetime.strptime(software_dict["last_modified"], DATE_TIME_FORMAT)
            software.created = datetime.strptime(software_dict["created"], DATE_TIME_FORMAT)

        session.add(software)

    session.commit()


def import_project(project_file, session, original_dates=True):
    r"""
    Import Project objects stored as JSON in a file.
    Args:
        project_file: the file name storing Project JSON data.
        session: the database session to which project items are to be added.
        original_dates: flag indicating that the original dates of the import should be used.

    Returns:
        None.
    """
    with open(project_file, "r") as fin:
        project_dicts = json.load(fin)

    for project_dict in project_dicts:
        project = Project(
            name=project_dict["name"],
            description=project_dict["description"]
        )

        #if original_dates:
        #    project.last_modified = datetime.strptime(project_dict["last_modified"], DATE_TIME_FORMAT)
        #    project.created = datetime.strptime(project_dict["created"], DATE_TIME_FORMAT)

        session.add(project)

    session.commit()


def import_material(material_file, session, original_dates=True):
    r"""
    Import Geometry objects stored as JSON in a file.
    Args:
        material_file: the file name storing Geometry JSON data.
        session: the database session to which materials are to be added.
        original_dates: flag indicating that the original dates of the import should be used.

    Returns:
        None.
    """
    with open(material_file, "r") as fin:
        material_dicts = json.load(fin)

    for material_dict in material_dicts:
        anisotropy_form = session.query(AnisotropyForm).\
            filter(AnisotropyForm.name == material_dict["anisotropy_form"]["name"]).\
            one()

        material = Material(
            name=material_dict["name"],
            temperature=material_dict["temperature"],
            k1=material_dict["k1"],
            aex=material_dict["aex"],
            ms=material_dict["ms"],
            kd=material_dict["kd"],
            lambda_ex=material_dict["lambda_ex"],
            q_hardness=material_dict["q_hardness"],
            axis_theta=material_dict["axis_theta"],
            axis_phi=material_dict["axis_phi"],
            anisotropy_form=anisotropy_form
        )
        if original_dates:
            material.last_modified = datetime.strptime(material_dict["last_modified"], DATE_TIME_FORMAT)
            material.created = datetime.strptime(material_dict["created"], DATE_TIME_FORMAT)

        session.add(material)

    session.commit()


def import_unit(unit_file, session, original_dates=True):
    r"""
    Import Unit objects stored as JSON in a file.
    Args:
        unit_file: the file name storing Unit JSON data.
        session: the database session to which units are to be added.
        original_dates: flag indicating that the original dates of the import should be used.

    Returns:
        None.
    """
    with open(unit_file, "r") as fin:
        unit_dicts = json.load(fin)

    for unit_dict in unit_dicts:
        unit = Unit(
            symbol=unit_dict["symbol"],
            name=unit_dict["name"],
            power=unit_dict["power"],

        )
        if original_dates:
            unit.last_modified = datetime.strptime(unit_dict["last_modified"], DATE_TIME_FORMAT)
            unit.created = datetime.strptime(unit_dict["created"], DATE_TIME_FORMAT)
        session.add(unit)

    session.commit()


def import_physical_constant(physical_constant_file, session, original_dates=True):
    r"""
    Import PhysicalConstant objects stored as JSON in a file.
    Args:
        physical_constant_file: the file name storing PhysicalConstant JSON data.
        session: the database session to which physical constants are to be added.
        original_dates: flag indicating that the original dates of the import should be used.

    Returns:
        None.
    """
    with open(physical_constant_file, "r") as fin:
        physical_constant_dicts = json.load(fin)

    for physical_const_dict in physical_constant_dicts:
        physical_constant = PhysicalConstant(
            symbol=physical_const_dict["symbol"],
            name=physical_const_dict["name"],
            value=physical_const_dict["value"],
            unit=physical_const_dict["unit"],
        )

        if original_dates:
            physical_constant.last_modified = datetime.strptime(physical_const_dict["last_modified"], DATE_TIME_FORMAT)
            physical_constant.created = datetime.strptime(physical_const_dict["created"], DATE_TIME_FORMAT)

        session.add(physical_constant)

    session.commit()


def import_size_convention(size_convention_file, session, original_dates=True):
    r"""
    Import SizeConvention objects stored as JSON in a file.
    Args:
        size_convention_file: the file name storing SizeConvention JSON data.
        session: the database session to which size conventions are to be added.
        original_dates: flag indicating that the original dates of the import should be used.

    Returns:
        None.
    """
    with open(size_convention_file, "r") as fin:
        size_convention_dicts = json.load(fin)

    for size_convention_dict in size_convention_dicts:
        size_convention = SizeConvention(
            symbol=size_convention_dict["symbol"],
            description=size_convention_dict["description"]
        )

        if original_dates:
            size_convention.last_modified = datetime.strptime(size_convention_dict["last_modified"], DATE_TIME_FORMAT)
            size_convention.created = datetime.strptime(size_convention_dict["created"], DATE_TIME_FORMAT)

        session.add(size_convention)
    session.commit()


def import_anisotropy_form(anisotropy_form_file, session, original_dates=True):
    r"""
    Import SizeConvention objects stored as JSON in a file.
    Args:
        anisotropy_form_file: the file name storing SizeConvention JSON data.
        session: the database session to which anisotropy forms are to be added.
        original_dates: flag indicating that the original dates of the import should be used.

    Returns:
        None.
    """
    with open(anisotropy_form_file, "r") as fin:
        anisotropy_form_dicts = json.load(fin)

    for anisotropy_form_dict in anisotropy_form_dicts:
        anisotropy_form = AnisotropyForm(
            name=anisotropy_form_dict["name"],
            description=anisotropy_form_dict["description"]
        )

        if original_dates:
            anisotropy_form.last_modified = datetime.strptime(anisotropy_form_dict["last_modified"], DATE_TIME_FORMAT)
            anisotropy_form.created = datetime.strptime(anisotropy_form_dict["created"], DATE_TIME_FORMAT)

        session.add(anisotropy_form)
    session.commit()


def import_running_status(running_status_file, session, original_dates=True):
    r"""
    Import RunningStatus objects stored as JSON in a file.
    Args:
        running_status_file: the file name storing RunningStatus JSON data.
        session: the database session to which runnning statuses are to be added.
        original_dates: flag indicating that the original dates of the import should be used.

    Returns:
        None.
    """
    with open(running_status_file, "r") as fin:
        running_status_dicts = json.load(fin)

    for running_status_dict in running_status_dicts:
        running_status = RunningStatus(
            name=running_status_dict["name"],
            description=running_status_dict["description"]
        )

        if original_dates:
            running_status.last_modified = datetime.strptime(running_status_dict["last_modified"], DATE_TIME_FORMAT)
            running_status.created = datetime.strptime(running_status_dict["created"], DATE_TIME_FORMAT)

        session.add(running_status)
    session.commit()


def import_neb_calculation_type(neb_calc_type_file, session, original_dates=True):
    r"""
    Import NEB calculation type objects stored as JSON in a file.
    Args:
        neb_calc_type_file: the file name storing NEBCalculationType JSON data.
        session: the database session to which materials are to be added.
        original_dates: flag indicating that the original dates of the import should be used.

    Returns:
        None.
    """
    with open(neb_calc_type_file, "r") as fin:
        neb_calc_type_dicts = json.load(fin)

    for neb_calc_type_dict in neb_calc_type_dicts:
        neb_calc_type = NEBCalculationType(
            name=neb_calc_type_dict["name"],
            description=neb_calc_type_dict["description"]
        )

        if original_dates:
            neb_calc_type.last_modified = datetime.strptime(neb_calc_type_dict["last_modified"], DATE_TIME_FORMAT)
            neb_calc_type.created = datetime.strptime(neb_calc_type_dict["created"], DATE_TIME_FORMAT)

        session.add(neb_calc_type)

    session.commit()


def import_geometry(geometry_file, session, original_dates=True):
    r"""
    Import Geometry objects stored as JSON in a file.
    Args:
        geometry_file: the file name storing Geometry JSON data.
        session: the database session to which geometries are to be added.
        original_dates: flag indicating that the original dates of the import should be used.

    Returns:
        None.
    """
    with open(geometry_file, "r") as fin:
        geometry_dicts = json.load(fin)

    for geometry_dict in geometry_dicts:
        if geometry_dict["size_unit"] is None:
            raise ValueError("geometry dict must contain 'size_unit'")
        if geometry_dict["size_convention"] is None:
            raise ValueError("geometry dict must contain 'size_convention'")

        size_unit = session.query(Unit). \
            filter(Unit.symbol == geometry_dict["size_unit"]["symbol"]). \
            one()

        size_convention = session.query(SizeConvention). \
            filter(SizeConvention.symbol == geometry_dict["size_convention"]["symbol"]). \
            one()

        if geometry_dict["element_size_unit"] is None:
            element_size_unit = None
        else:
            element_size_unit = session.query(Unit). \
                filter(Unit.symbol == geometry_dict["element_size_unit"]["symbol"]). \
                one()

        geometry = Geometry(
            unique_id=geometry_dict["unique_id"],
            name=geometry_dict["name"],
            size=geometry_dict["size"],
            element_size=geometry_dict["element_size"] if "element_size" in geometry_dict.keys() else None,
            description=geometry_dict["description"] if "description" in geometry_dict.keys() else None,
            nelements=geometry_dict["nelements"],
            nvertices=geometry_dict["nvertices"],
            nsubmeshes=geometry_dict["nsubmeshes"],
            volume_total=geometry_dict["volume_total"] if "volume_total" in geometry_dict.keys() else None,
            has_patran=geometry_dict["has_patran"],
            has_exodus=geometry_dict["has_exodus"],
            has_mesh_gen_script=geometry_dict["has_mesh_gen_script"],
            has_mesh_gen_output=geometry_dict["has_mesh_gen_output"],
            size_unit=size_unit,
            size_convention=size_convention,
            element_size_unit=element_size_unit
        )
        if original_dates:
            geometry.last_modified = datetime.strptime(geometry_dict["last_modified"], DATE_TIME_FORMAT)
            geometry.created = datetime.strptime(geometry_dict["created"], DATE_TIME_FORMAT)

        session.add(geometry)

    session.commit()


def import_model(model_file, session, original_dates=True):
    r"""
    Import Model objects stored as JSON in a file.
    Args:
        model_file: the file name storing Model JSON data.
        session: the database session to which models are to be added.
        original_dates: flag indicating that the original dates of the import should be used.

    Returns:
        None.
    """
    with open(model_file, "r") as fin:
        model_dicts = json.load(fin)

    for model_dict in model_dicts:

        # The model's geometry.
        geometry = session.query(Geometry).\
            filter(Geometry.unique_id == model_dict["geometry"]["unique_id"]).\
            one()

        # The model's start magnetization.
        if model_dict["start_magnetization"]["type"] == "random_field":
            start_magnetization = RandomField()
        elif model_dict["start_magnetization"]["type"] == "uniform_field":
            start_field_unit = session.query(Unit). \
                filter(Unit.symbol == model_dict["start_magnetization"]["unit"]["symbol"]). \
                one()
            start_magnetization = UniformField(
                dir_x=model_dict["start_magnetization"]["dir_x"],
                dir_y=model_dict["start_magnetization"]["dir_y"],
                dir_z=model_dict["start_magnetization"]["dir_z"],
                magnitude=model_dict["start_magnetization"]["magnitude"],
                unit=start_field_unit
            )
        elif model_dict["start_magnetization"]["type"] == "model_field":
            model = session.query(Model). \
                filter(Model.unique_id == model_dict["start_magnetization"]["model_unique_id"]). \
                one()
            start_magnetization = ModelField(
                model=model
            )
        else:
            raise ValueError(
                "Unsupported start magnetization type '{}'".format(
                    model_dict["start_magnetization"]["type"]
                )
            )

        # The model's external field
        if model_dict["external_field"] is None:
            external_field = None
        elif model_dict["external_field"]["type"] == "uniform_field":
            external_field_unit = session.query(Unit). \
                filter(Unit.symbol == model_dict["external_field"]["unit"]["symbol"]). \
                one()
            external_field = UniformField(
                dir_x=model_dict["external_field"]["dir_x"],
                dir_y=model_dict["external_field"]["dir_y"],
                dir_z=model_dict["external_field"]["dir_z"],
                magnitude=model_dict["external_field"]["magnitude"],
                unit=external_field_unit
            )
        else:
            raise ValueError(
                "Unsupported external field type '{}'".format(
                    model_dict["external_field"]["type"]
                )
            )

        # The model's running status.
        running_status = session.query(RunningStatus). \
            filter(RunningStatus.name == model_dict["running_status"]["name"]).\
            one()

        # The model's run data.
        model_run_data = ModelRunData(
            has_stdout=model_dict["model_run_data"]["has_stdout"],
            has_stderr=model_dict["model_run_data"]["has_stderr"],
            has_energy_log=model_dict["model_run_data"]["has_energy_log"],
            has_script=model_dict["model_run_data"]["has_script"],
            has_tecplot=model_dict["model_run_data"]["has_tecplot"],
            has_json=model_dict["model_run_data"]["has_json"],
            has_dat=model_dict["model_run_data"]["has_dat"],
            has_helicity_dat=model_dict["model_run_data"]["has_helicity_dat"],
            has_vorticity_dat=model_dict["model_run_data"]["has_vorticity_dat"],
            has_adm_dat=model_dict["model_run_data"]["has_adm_dat"]
        )

        # The model's report data.
        model_report_data = ModelReportData(
            has_xy_thumb_png=model_dict["model_report_data"]["has_xy_thumb_png"],
            has_yz_thumb_png=model_dict["model_report_data"]["has_yz_thumb_png"],
            has_xz_thumb_png=model_dict["model_report_data"]["has_xz_thumb_png"],
            has_xy_png=model_dict["model_report_data"]["has_xy_png"],
            has_yz_png=model_dict["model_report_data"]["has_yz_png"],
            has_xz_png=model_dict["model_report_data"]["has_xz_png"]
        )

        # The user that the model belongs to.
        db_user = session.query(DBUser). \
            filter(DBUser.user_name == model_dict["mdata"]["db_user_user_name"]). \
            one()

        # The project that the model belongs to.
        project = session.query(Project). \
            filter(Project.name == model_dict["mdata"]["project_name"]). \
            one()

        # The software that created/will create the model.
        software = session.query(Software). \
            filter(Software.name == model_dict["mdata"]["software_name"]). \
            filter(Software.version == model_dict["mdata"]["software_version"]). \
            one()

        # The new metadata
        mdata = Metadata(
            db_user=db_user,
            project=project,
            software=software
        )

        # If there is legacy model info then include that here.
        if model_dict["legacy_model_info"] is None:
            legacy_model_info = None
        else:
            legacy_model_info = LegacyModelInfo(
                index=model_dict["legacy_model_info"]["index"]
            )

        model = Model(
            unique_id=model_dict["unique_id"],
            mx_tot=model_dict["mx_tot"],
            my_tot=model_dict["my_tot"],
            mz_tot=model_dict["mz_tot"],
            vx_tot=model_dict["vx_tot"],
            vy_tot=model_dict["vy_tot"],
            vz_tot=model_dict["vz_tot"],
            h_tot=model_dict["h_tot"],
            adm_tot=model_dict["adm_tot"],
            e_typical=model_dict["e_typical"],
            e_anis=model_dict["e_anis"],
            e_ext=model_dict["e_ext"],
            e_demag=model_dict["e_demag"],
            e_exch1=model_dict["e_exch1"],
            e_exch2=model_dict["e_exch2"],
            e_exch3=model_dict["e_exch3"],
            e_exch4=model_dict["e_exch4"],
            e_tot=model_dict["e_tot"],
            max_energy_evaluations=model_dict["max_energy_evaluations"],
            geometry=geometry,
            start_magnetization=start_magnetization,
            external_field=external_field,
            running_status=running_status,
            model_run_data=model_run_data,
            model_report_data=model_report_data,
            mdata=mdata,
            legacy_model_info=legacy_model_info

        )
        if original_dates:
            model.last_modified = datetime.strptime(model_dict["last_modified"], DATE_TIME_FORMAT)
            model.created = datetime.strptime(model_dict["created"], DATE_TIME_FORMAT)

        # Materials are added here
        for material_dict in model_dict["materials"]:
            material = session.query(Material). \
                filter(Material.name == material_dict["name"]). \
                filter(Material.temperature == material_dict["temperature"]). \
                one()
            mma = ModelMaterialAssociation(
                index=1,
                material=material
            )
            model.materials.append(mma)

        session.add(model)

    session.commit()


def import_neb(neb_file, session, original_dates=True):
    r"""
    Import NEB path objects stored as JSON in a file.
    Args:
        neb_file: the file name storing NEB JSON data.
        session: the database session to which NEB paths are to be added.
        original_dates: flag indicating that the original dates of the import should be used.

    Returns:
        None.
    """
    with open(neb_file, "r") as fin:
        neb_dicts = json.load(fin)

    # Create a function that knows how to return a unique id of an neb_dict
    def get_neb_dict_unique_id(neb_dict):
        return neb_dict["unique_id"]

    # Create a function that knows how to return the parent unique id of an neb_dict
    def get_neb_dict_parent_unique_id(neb_dict):
        return neb_dict["parent_neb_unique_id"]

    # Create a function that knows how to save an neb_dict to the database.
    def save_neb_to_database(neb_dict):
        lcl_session = save_neb_to_database.session
        lcl_with_original_dates = save_neb_to_database.with_original_dates

        # Create an external field object.
        if neb_dict["external_field"] is None:
            external_field = None
        elif neb_dict["external_field"]["type"] == "uniform_field":
            external_field_unit = session.query(Unit). \
                filter(Unit.symbol == neb_dict["external_field"]["unit"]["symbol"]). \
                one()
            external_field = UniformField(
                dir_x=neb_dict["external_field"]["dir_x"],
                dir_y=neb_dict["external_field"]["dir_y"],
                dir_z=neb_dict["external_field"]["dir_z"],
                magnitude=neb_dict["external_field"]["magnitude"],
                unit=external_field_unit
            )
        else:
            raise ValueError(
                "Unsupported external field type '{}'".format(
                    neb_dict["external_field"]["type"]
                )
            )

        # Retrieve the start model
        start_model = lcl_session.query(Model).\
            filter(Model.unique_id == neb_dict["start_model_unique_id"]).\
            one()

        # Retrieve the end model.
        end_model = lcl_session.query(Model).\
            filter(Model.unique_id == neb_dict["end_model_unique_id"]).\
            one()

        # Retrieve the parent NEB.
        if neb_dict["parent_neb_unique_id"] is None:
            parent_neb = None
        else:
            parent_neb = lcl_session.query(NEB).\
                filter(NEB.unique_id == neb_dict["parent_neb_unique_id"]).\
                one()

        # Retrieve the NEB calculation type.
        neb_calculation_type = lcl_session.query(NEBCalculationType).\
            filter(NEBCalculationType.name == neb_dict["neb_calculation_type"]["name"]).\
            one()

        # Create an NEBRunData object.
        neb_run_data = NEBRunData(
            has_script=neb_dict["neb_run_data"]["has_script"],
            has_stdout=neb_dict["neb_run_data"]["has_stdout"],
            has_stderr=neb_dict["neb_run_data"]["has_stderr"],
            has_energy_log=neb_dict["neb_run_data"]["has_energy_log"],
            has_tecplot=neb_dict["neb_run_data"]["has_tecplot"],
            has_neb_energies=neb_dict["neb_run_data"]["has_neb_energies"]
        )

        # Create an NEBReportData object.
        neb_report_data = NEBReportData(
            has_x_png=neb_dict["neb_report_data"]["has_x_png"],
            has_y_png=neb_dict["neb_report_data"]["has_y_png"],
            has_z_png=neb_dict["neb_report_data"]["has_z_png"],
            has_x_thumb_png=neb_dict["neb_report_data"]["has_x_thumb_png"],
            has_y_thumb_png=neb_dict["neb_report_data"]["has_y_thumb_png"],
            has_z_thumb_png=neb_dict["neb_report_data"]["has_z_thumb_png"]
        )

        # Retrieve the running status.
        running_status = lcl_session.query(RunningStatus).\
            filter(RunningStatus.name == neb_dict["running_status"]["name"]).\
            one()

        # The user that the model belongs to.
        db_user = lcl_session.query(DBUser).\
            filter(DBUser.user_name == neb_dict["mdata"]["db_user_user_name"]).\
            one()

        # The project that the model belongs to.
        project = lcl_session.query(Project).\
            filter(Project.name == neb_dict["mdata"]["project_name"]).\
            one()

        # The software that created/will create the model.
        software = lcl_session.query(Software).\
            filter(Software.name == neb_dict["mdata"]["software_name"]).\
            filter(Software.version == neb_dict["mdata"]["software_version"]).\
            one()

        # Create a new metadata from user, project & software.
        mdata = Metadata(
            db_user=db_user,
            project=project,
            software=software
        )

        # Create the new NEB object
        neb = NEB(
            unique_id=neb_dict["unique_id"],
            spring_constant=neb_dict["spring_constant"],
            curvature_weight=neb_dict["curvature_weight"],
            no_of_points=neb_dict["no_of_points"],
            max_energy_evaluations=neb_dict["max_energy_evaluations"],
            max_path_evaluations=neb_dict["max_path_evaluations"],
            external_field=external_field,
            start_model=start_model,
            end_model=end_model,
            parent_neb=parent_neb,
            neb_calculation_type=neb_calculation_type,
            neb_run_data=neb_run_data,
            neb_report_data=neb_report_data,
            running_status=running_status,
            mdata=mdata
        )

        lcl_session.add(neb)

    # Add the session object to the 'save_neb_to_database' function
    save_neb_to_database.session = session

    # Add the flag that indicates whether we should use the original dates to the 'save_neb_to_database' function.
    save_neb_to_database.with_original_dates = original_dates

    # Create a DependencyImporter object with the three functions (get_neb_dict_unique_id,
    # get_neb_dict_parent_unique_id and save_neb_to_database) defined above.
    dependency_importer = DependencyImporter(
        get_neb_dict_unique_id, get_neb_dict_parent_unique_id, save_neb_to_database
    )

    # Run the importer on the list of dicts
    dependency_importer.perform_import(neb_dicts)

    session.commit()
