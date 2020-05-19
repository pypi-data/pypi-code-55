r"""
Created on Aug, 2018

@file: orm.py
@author: Nagy, Lesleis
"""


from datetime import datetime
from math import sqrt, sin, cos, acos, atan2, pi

import uuid

from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, Numeric
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint, Index
from sqlalchemy import event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property
from sqlalchemy.orm import relationship


now = datetime.now


Base = declarative_base()


def new_unique_id():
    r"""
    Returns: a global unique id.

    """
    return str(uuid.uuid4())


class DBUser(Base):
    """
    Holds information about who a model belongs to. NOTE: this is not ownership
    in the sense of permissions but it gives us a useful dimension to
    differentiate different models.

    Attributes:
        id            : a unique internal id for the object

        user_name     : a unique name for the user

        first_name    : the user's first name

        initials      : the user's middle initials

        surname       : the user's surname

        email         : the user's surname

        telephone     : the user's telephone

        last_modified : the date/time at which this object/record was modified

        created       : the creation date/time of this object/record
    """
    __tablename__ = 'db_user'

    id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    initials = Column(String, nullable=True)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    telephone = Column(String, nullable=True)
    last_modified = Column(DateTime, default=now(), onupdate=now(), nullable=False)
    created = Column(DateTime, default=now(), nullable=False)

    UniqueConstraint('first_name', 'surname', 'email', 'telephone', name='uniq_user_01')
    UniqueConstraint('user_name', name='uniq_user_02')


class Software(Base):
    """
    Holds information about the software used to run models.

    Attributes:
        id            : a unique internal id for the object

        name          : the name of the software package

        version       : the version of the software package

        description   : a description of the software package

        url           : a URL for the software package

        citation      : a citation for the software package

        last_modified : the date/time at which this object/record was modified

        created       : the creation date/time of this object/record

    """
    __tablename__ = 'software'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    description = Column(String, nullable=True)
    url = Column(String, nullable=True)
    citation = Column(String, nullable=True)
    last_modified = Column(DateTime, default=now(), onupdate=now(), nullable=False)
    created = Column(DateTime, default=now(), nullable=False)

    UniqueConstraint('name', 'version', name='uniq_software_01')


class Unit(Base):
    """
    Holds a number of units used to give the sizes/magnitudes of some values
    found in the database.

    Attributes:
        id            : a unique internal id for the object

        symbol        : the symbol associated with the unit

        name          : the unit's name

        power         : the power/exponent of the unit (in the natural base
                        of the unit)

        last_modified : the date/time at which this object/record was modified

        created       : the creation date/time of this object/record
    """
    __tablename__ = 'unit'

    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False)
    name = Column(String, nullable=False)
    power = Column(Float, nullable=False)
    last_modified = Column(DateTime, default=now(), onupdate=now(), nullable=False)
    created = Column(DateTime, default=now(), nullable=False)

    UniqueConstraint('symbol', name='uniq_unit_01')


class PhysicalConstant(Base):
    """
    Holds a number of important physical constants.

    Attributes:
        id            : a unique internal id for the object

        symbol        : the symbol associated with the physical constant

        name          : the constant's name

        value         : the constant's value

        unit          : the symbolic unit for the contant

        last_modified : the date/time at which this object/record was modified

        created       : the creation date/time of this object/record
    """
    __tablename__ = 'physical_constant'

    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False)
    name = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    last_modified = Column(DateTime, default=now(), onupdate=now(), nullable=False)
    created = Column(DateTime, default=now(), nullable=False)

    UniqueConstraint('symbol', name='uniq_physica_constant_01')


class SizeConvention(Base):
    """
    Holds a size convention, size conventions are useful since we use them as
    a short hand to refer to volumentric sizes. For example: what do we mean by
    "100nm grain"?, if we're using equivalent spherical volume diameter (ESVD)
    then the grain has a volume equivalent to a sphere of diameter 100nm.

    Attributes:
        id            : a unique internal id for the object

        symbol        : the symbol associated with the size convention

        description   : a description for the size convention

        last_modified : the date/time at which this object/record was modified

        created       : the creation date/time of this object/record
    """
    __tablename__ = 'size_convention'

    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False)
    description = Column(String, nullable=False)
    last_modified = Column(DateTime, default=now(), onupdate=now(), nullable=False)
    created = Column(DateTime, default=now(), nullable=False)

    UniqueConstraint('symbol', name='uniq_size_convention_01')


class AnisotropyForm(Base):
    """
    Hold different anisotropy forms for example 'cubic' and 'uniaxial'.

    Attributes:
        id            : a unique internal id for the object

        name          : anisotropy form's name

        description   : a description for the anisotropy form convention

        last_modified : the date/time at which this object/record was modified

        created       : the creation date/time of this object/record
    """
    __tablename__ = 'anisotropy_form'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    last_modified = Column(DateTime, default=now(), onupdate=now(), nullable=False)
    created = Column(DateTime, default=now(), nullable=False)

    UniqueConstraint('name', name='uniq_anisotropy_form_01')


class Geometry(Base):
    """
    Hold's geometry data. The natural key for a geometry is name/size pair
    (hence the reason why size is a string). Note: size is given as a string
    decimal of the form '[0-9]*\.[0-9]+', and is assumed to have the units
    defined by size_unit.

    Attributes:

        id                       : a unique internal id for the object

        unique_id                : a unique identifier for the geometry that
                                   may be used outside the database.

        name                     : the name of the geometry

        size                     : the size of the geometry in the given units

        element_size             : the size of the elements that comprise this
                                   geometry

        description              : a brief description of the geometry

        nelements                : the number of elements that comprise the
                                   geometry

        nvertices                : the number of vertices that comprise the
                                   geometry

        has_patran               : a patran file is available for the geometry

        has_exodus               : an exodus file is available for the geometry

        has_mesh_gen_script      : a script to generate the mesh is available
                                   for the geometry

        last_modified            : the date/time at which this object/record
                                   was modified

        created                  : the creation date/time of this object/record
    """
    __tablename__ = 'geometry'

    id = Column(Integer, primary_key=True, nullable=False)
    unique_id = Column(String, default=new_unique_id, nullable=False)
    name = Column(String, nullable=False)
    size = Column(Numeric(10,5), nullable=False)
    element_size = Column(Numeric(10,5), nullable=True)
    description = Column(String, nullable=True)
    nelements = Column(Integer, nullable=False)
    nvertices = Column(Integer, nullable=False)
    nsubmeshes = Column(Integer, default=1, nullable=False)
    volume_total = Column(Float, nullable=True)
    has_patran = Column(Boolean, default=False, nullable=False)
    has_exodus = Column(Boolean, default=False, nullable=False)
    has_mesh_gen_script = Column(Boolean, default=False, nullable=False)
    has_mesh_gen_output = Column(Boolean, default=False, nullable=False)
    last_modified = Column(DateTime, default=now(), onupdate=now(), nullable=False)
    created = Column(DateTime, default=now(), nullable=False)

    size_unit_id = Column(Integer, ForeignKey('unit.id'), nullable=False)
    size_unit = relationship('Unit', uselist=False, foreign_keys=[size_unit_id])

    element_size_unit_id = Column(Integer, ForeignKey('unit.id'), nullable=True)
    element_size_unit = relationship('Unit', uselist=False, foreign_keys=[element_size_unit_id])

    size_convention_id = Column(Integer, ForeignKey('size_convention.id'), nullable=False)
    size_convention = relationship('SizeConvention', uselist=False)

    # The software id used to generate the geometry
    software_id = Column(Integer, ForeignKey('software.id'), nullable=True)
    software = relationship('Software')

    UniqueConstraint(
        'name',
        'size',
        'size_unit_id',
        name='uniq_geometry_01'
    )

    UniqueConstraint('unique_id', name='uniq_geometry_02')

    Index('idx_geometry_01', 'name', 'size')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Material(Base):
    """
    Holds material data that is important for micromagnetic calculations. The
    natural key for a material is name/temperature pair (hence the reason why
    temperature is an integer). Note: temperature is *ALWAYS* assumed to be in
    degrees Celsius.

    Attributes:
        id            : a unique internal id for the object

        name          : the name of the material (e.g. magnetite)

        temperature   : the temperature at which material constants are
                        calculated

        k1            : the first magnetocrystalline anisotropy constant

        a             : the exchange constant

        ms            : the saturation magnetization constant

        lambda_ex     : the exchange length

        q_hardness    : the micromagnetic magnetic hardness

        last_modified : the data/time at which the object/record was modified

        created       : the creation date/time of this object/record
    """
    __tablename__ = 'material'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    temperature = Column(Numeric(8,3), nullable=False)
    k1 = Column(Float, nullable=False)
    aex = Column(Float, nullable=False)
    ms = Column(Float, nullable=False)
    kd = Column(Float, nullable=False)
    lambda_ex = Column(Float, nullable=True)
    q_hardness = Column(Float, nullable=True)
    axis_theta = Column(Float, nullable=True, default=0.0)
    axis_phi = Column(Float, nullable=True, default=0.0)
    last_modified = Column(DateTime, default=now(), onupdate=now(), nullable=False)
    created = Column(DateTime, default=now(), nullable=False)

    anisotropy_form_id = Column(Integer, ForeignKey('anisotropy_form.id'), nullable=False)
    anisotropy_form = relationship('AnisotropyForm', uselist=False)

    UniqueConstraint('name', 'temperature', name='uniq_material_01')
    Index('idx_material_01', 'name', 'temperature')


class Field(Base):
    """
    The parent class/entity of all fields. This field object/entity should
    *NOT* be used on its own since it is abstract - please use one of the
    derived types:

        1) FileField      - encapsulates a field from a file (e.g. '.dat')

        2) ModelField     - encapsulates a field from an existing micromagnetic
                            model

        3) RandomField    - encapsulates a random field

        4) UniformField   - encapsulates a uniform field in a particular
                            direction

    Attributes:
        id            : a unique internal id for the object

        type          : a string that reffers to the child type (see above)

        last_modified : the date/time at which this object/record was modified

        created       : the creation date/time of this object/record
    """
    __tablename__ = 'field'

    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(String, nullable=False)
    last_modified = Column(DateTime, default=now(), onupdate=now(), nullable=False)
    created = Column(DateTime, default=now(), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'field',
        'polymorphic_on': type
    }


class FileField(Field):
    """
    A file field is a field that derives its structure from the data stored
    in a file, the file should be stored in the database and assigned its own
    unique_id.
    """
    __tablename__ = 'file_field'

    id = Column(Integer, ForeignKey('field.id'), primary_key=True, nullable=False)
    last_modified = column_property(Column(DateTime, default=now(), onupdate=now(), nullable=False),
                                    Field.last_modified)
    created = column_property(Column(DateTime, default=now(), nullable=False), Field.created)

    __mapper_args__ = {
        'polymorphic_identity': 'file_field'
    }


class ModelField(Field):
    """
    A model field is a field that that derives its structure from an existing
    model.
    """
    __tablename__ = 'model_field'

    id = Column(Integer, ForeignKey('field.id'), primary_key=True, nullable=False)
    last_modified = column_property(Column(DateTime, default=now(), onupdate=now(), nullable=False),
                                    Field.last_modified)
    created = column_property(Column(DateTime, default=now(), nullable=False), Field.created)

    model_id = Column(Integer, ForeignKey('model.id'), nullable=False)
    model = relationship('Model')

    __mapper_args__ = {
        'polymorphic_identity': 'model_field',
    }


class RandomField(Field):
    """
    A random field is really just a placeholder record to denote a random
    field.  Actual seeds my be stored if wanting to reproduce specific random
    fields (but this is not cross platform compatible).
    """
    __tablename__ = 'random_field'

    id = Column(Integer, ForeignKey('field.id'), primary_key=True, nullable=False)
    seed = Column(Integer, nullable=True)
    last_modified = column_property(Column(DateTime, default=now(), onupdate=now(), nullable=False),
                                    Field.last_modified)
    created = column_property(Column(DateTime, default=now(), nullable=False), Field.created)

    __mapper_args__ = {
        'polymorphic_identity': 'random_field',
    }


class UniformField(Field):
    """
    A UniformField consists of a vector in spherical polar coordinates using
    using (azimuthal, polar, magnitude) = (theta, phi, magnitude) convention.
    Internally theta and phi are stored in radians, but helper functions are
    provided that convert between Cartesian/spherical-polar and degrees and
    radians.

    Attributes:
        id            : a unique internal id for the object

        theta         : the azimuthal component of the field

        phi           : polar component of the field

        dir_x         : the x component of the field direction

        dir_y         : the y component of the field direction

        dir_z         : the z component of the field direction

        magnitude     : the radial component of the field

        last_modified : the date/time at which this object/record was modified

        created       : the creation date/time of this object/record

        unit_id       : the id of a unit record, this is the unit of the field
                        magnitude
    """
    __tablename__ = 'uniform_field'

    id = Column(Integer, ForeignKey('field.id'), primary_key=True, nullable=False)
    theta = Column(Float, nullable=False)
    phi = Column(Float, nullable=False)
    dir_x = Column(Float, nullable=False)
    dir_y = Column(Float, nullable=False)
    dir_z = Column(Float, nullable=False)
    magnitude = Column(Float, nullable=False)
    last_modified = column_property(Column(DateTime, default=now(), onupdate=now(), nullable=False),
                                    Field.last_modified)
    created = column_property(Column(DateTime, default=now(), nullable=False), Field.created)

    unit_id = Column(Integer, ForeignKey('unit.id'), nullable=False)
    unit = relationship('Unit')

    __mapper_args__ = {
        'polymorphic_identity': 'uniform_field',
    }

    def __init__(self, **kwargs):
        use_degrees = False
        if 'use_degrees' in kwargs.keys():
            use_degrees = kwargs['use_degrees']

        if 'theta' in kwargs.keys() and 'phi' in kwargs.keys() and 'magnitude' in kwargs.keys():
            # Initialise based on spherical-polar.
            if use_degrees:
                self.theta = self.degree_to_radian(kwargs['theta'])
                self.phi = self.degree_to_radian(kwargs['phi'])
                self.magnitude = kwargs['magnitude']
                self.dir_x, self.dir_y, self.dir_z = self.spherical_to_cartesian_direction(self.theta, self.phi)
            else:
                self.theta = kwargs['theta']
                self.phi = kwargs['phi']
                self.magnitude = kwargs['magnitude']
                self.dir_x, self.dir_y, self.dir_z = self.spherical_to_cartesian_direction(self.theta, self.phi)
        elif 'dx' in kwargs.keys() and 'dy' in kwargs.keys() and 'dz' in kwargs.keys() and 'magnitude' in kwargs.keys():
            # Initialise based on Cartesian.
            dx = kwargs['dx']
            dy = kwargs['dy']
            dz = kwargs['dz']

            (theta, phi) = UniformField.cartesian_to_spherical_direction(dx, dy, dz)

            self.theta = theta
            self.phi = phi
            self.magnitude = kwargs['magnitude']

            vlen = sqrt(dx*dx + dy*dy + dz*dz)
            self.dir_x = dx/vlen
            self.dir_y = dy/vlen
            self.dir_z = dz/vlen
        else:
            raise ValueError(
                "UniformField must be defined in therms of ('magnitude', 'theta', 'phi')"
                " OR ('dx', 'dy', 'dz', 'magnitude')")

        if 'unit' in kwargs.keys():
            self.unit = kwargs['unit']

    @hybrid_property
    def cartesian_direction(self):
        r"""
        Access the direction of the UniformField vector using Cartesian representation.
        """
        return UniformField.spherical_to_cartesian_direction(self.theta, self.phi)

    @hybrid_property
    def degree_direction(self):
        r"""
        Retrieve the directional component (theta, phi) of the UniformField in units of degree.
        """
        return self.radian_to_degree(self.theta), self.radian_to_degree(self.phi)

    @cartesian_direction.setter
    def cartesian_direction(self, **kwargs):
        r"""
        Set the direction of a UniformField vector to correspond to the new direction defined in Cartesian
        components.
        """
        if 'dx' in kwargs.keys() and 'dy' in kwargs.keys() and 'dz' in kwargs.keys():
            # Only change the direction.
            dx = kwargs['dx']
            dy = kwargs['dy']
            dz = kwargs['dz']
            theta, phi = UniformField.cartesian_to_spherical_direction(dx, dy, dz)
            self.theta = theta
            self.phi = phi

    @degree_direction.setter
    def degree_direction(self, **kwargs):
        r"""
        Set the internal representation of the UniformField vector to
        correspond to the new field y-component value.
        """

        self.theta = UniformField.degree_to_radian(kwargs['theta'])
        self.phi = UniformField.degree_to_radian(kwargs['phi'])

    @staticmethod
    def spherical_to_cartesian_direction(theta, phi):
        """
        Private function to convert sphercal-polar coordinate to Cartesian.
        """

        x = cos(theta) * sin(phi)
        y = sin(theta) * sin(phi)
        z = cos(phi)

        return x, y, z

    @staticmethod
    def cartesian_to_spherical_direction(x, y, z):
        """
        Private function to convert Cartesian coordinate to spheical-polar.
        """
        theta = atan2(y, x)
        phi = acos(z)        # Don't divide by radial component here since we assume x,y,z specifies *ONLY* a direction.

        return theta, phi

    @staticmethod
    def degree_to_radian(value):
        return value * (pi / 180.0)

    @staticmethod
    def radian_to_degree(value):
        return value * (180.0 / pi)


class RunningStatus(Base):
    r'''
    The running status of a model. Models can be in one of the following states
        I)   not-run
        II)  re-run
        III) running
        IV)  finnished

    :param id: the primary key id of a RunningStatus object.
    :param name: the name of the running status.
    :param description: a description of the running status.
    :param last_modified: the last modified time of the RunningStatus object.
    :param created: the creation time of the RunningStatus object.
    '''
    __tablename__ = 'running_status'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    last_modified = Column(DateTime, default=now(), onupdate=now(), nullable=False)
    created = Column(DateTime, default=now(), nullable=False)


class ModelRunData(Base):
    r'''
    Important metadata regarding a model.

    Attributes:
        id: a unique internal id for the object

        has_script        : a flag to indicate whether the model has a script
                            (which generated the model) associated with it

        has_stdout        : a flag to indicate whether the model has a standard
                            output file associated with it

        has_stderr        : a flag to indicate whether the model has a standard
                            error file associated with it

        has_energy_log    : a flag to indicate whether the model has an energy
                            log associated with it

        has_tecplot       : a flag to indicate whether the model has a tecplot
                            representation associated with it

        has_json          : a flag to indicate whether the model has a json
                            representation associated with it

        has_dat           : a flag to indicate whether the model has a dat
                            representation associated with it

        has_helicity_dat  : a flag to indicate whether the model has a dat
                            representation of its helicity scalar field
                            associated with it

        has_vorticity_dat : a flag to indicate whether the model has a dat
                            representation of its vorticity vector field
                            associated with it

        has_adm_dat       : a flag to indicate whether the model has a dat
                            representation of its adm scalar field associated
                            with it

        last_modified     : the date/time at which this object/record
                            was modified

        created           : the creation date/time of this object/record
    '''
    __tablename__ = 'model_run_data'

    id = Column(Integer, primary_key=True, nullable=False)
    has_script = Column(Boolean, default=False, nullable=False)
    has_stdout = Column(Boolean, default=False, nullable=False)
    has_stderr = Column(Boolean, default=False, nullable=False)
    has_energy_log = Column(Boolean, default=False, nullable=False)
    has_tecplot = Column(Boolean, default=False, nullable=False)
    has_json = Column(Boolean, default=False, nullable=False)
    has_dat = Column(Boolean, default=False, nullable=False)
    has_helicity_dat = Column(Boolean, default=False, nullable=False)
    has_vorticity_dat = Column(Boolean, default=False, nullable=False)
    has_adm_dat = Column(Boolean, default=False, nullable=False)
    last_modified = Column(DateTime, default=now(), onupdate=now(), nullable=False)
    created = Column(DateTime, default=now(), nullable=False)


class ModelReportData(Base):
    r"""
    Some metadata to track whether some data items used for generating a Model
    report have been created.

    :param id: the primary key.
    :param has_xy_thumb_png: a boolean set to true if there is a thumbnail image
                             of the model with the x-y axis corresponding to the
                             user's screen/monitor.
    :param has_yz_thumb_png: a boolean set to true if there is a thumbnail image
                             of the model with the y-z axis corresponding to the
                             user's screen/monitor.
    :param has_xz_thumb_png: a boolean set to true if there is a thumbnail image
                             of the model with the x-z axis corresponding to the
                             user's screen/monitor.
    :param has_xy_png:       a boolean set to true if there is an image of the
                             model with the x-y axis corresponding to the
                             user's screen/monitor.
    :param has_yz_png:       a boolean set to true if there is an image of the
                             model with the y-z axis corresponding to the
                             user's screen/monitor.
    :param has_xz_png:       a boolean set to true if there is an image of the
                             model with the x-z axis corresponding to the
                             user's screen/monitor.
    """
    __tablename__ = 'model_report_data'

    id = Column(Integer, primary_key=True, nullable=False)
    has_xy_thumb_png = Column(Boolean, default=False, nullable=False)
    has_yz_thumb_png = Column(Boolean, default=False, nullable=False)
    has_xz_thumb_png = Column(Boolean, default=False, nullable=False)
    has_xy_png = Column(Boolean, default=False, nullable=False)
    has_yz_png = Column(Boolean, default=False, nullable=False)
    has_xz_png = Column(Boolean, default=False, nullable=False)


class Project(Base):
    r"""
    Some metadata regarding a project.

    :param id:    the primary key.
    :name:        the name of the project.
    :description: a description of the project.
    """
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    UniqueConstraint('project_name', name='uniq_project_01')


class Metadata(Base):
    r"""
    Metadata associated with a model. Each model has a user that created it,
    a project to which it belongs and a peice of software that generated it.

    :param id:            the primary key

    :param project:       the Project object associated with this piece of
                          metadata.

    :param db_user:       the DBUser object associated with this piece of
                          metadata.

    :param software:      the Software object associated with this piece of
                          metadata.

    :param created:       the time when the object was created.

    :param last_modified: the time when the object was last modified.
    """
    __tablename__ = 'metadata'

    id = Column(Integer, primary_key=True, nullable=False)
    last_modified = Column(DateTime, default=now(), onupdate=now(), nullable=False)
    created = Column(DateTime, default=now(), nullable=False)

    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
    project = relationship('Project')

    db_user_id = Column(Integer, ForeignKey('db_user.id'), nullable=False)
    db_user = relationship('DBUser')

    software_id = Column(Integer, ForeignKey('software.id'), nullable=True)
    software = relationship('Software')


class LegacyModelInfo(Base):
    r"""
    Some models have some legacy information associated with them, these are
    stored in this object.

    :param id:            the primary key.

    :param index:         the index refferint to the the model index from the
                          legacy data structure.

    :param created:       the time when the object was created.

    :param last_modified: the time when the object was last modified.
    """
    __tablename__ = 'legacy_model_info'

    id = Column(Integer, primary_key=True, nullable=False)
    index = Column(Integer, nullable=False)
    last_modified = Column(DateTime, default=now(), onupdate=now(), nullable=False)
    created = Column(DateTime, default=now(), nullable=False)


class ModelMaterialAssociation(Base):
    r"""
    A helper object that associated Materials and Models together. This object
    provides a many-to-many link between Models and Materials so that one
    Model can have many materials, and one Material can belong to many
    Models.

    :param model_id:    the primary key of a Model.

    :param material_id: the primary key of a Material.

    :param index:       the index of the material, this should correspond with
                        the submesh indexing of the Geometry (in particular its
                        underlying file) associated with a Model.
    r"""
    __tablename__ = 'model_material_association'
    model_id = Column(Integer, ForeignKey('model.id'), primary_key=True)
    material_id = Column(Integer, ForeignKey('material.id'), primary_key=True)
    index = Column(Integer, nullable=False)

    material = relationship("Material")


class Model(Base):
    r"""
    Holds information about a single micromagnetic model. A micromagnetic
    model, fundamentally consists of a Geometry, one or more Materials and
    a solution. The data in this object is used both to populate a
    micromagnetic calculation (prior to a solution) and to track the parameters
    used to generate a solution (after the solution has been computed).

    :param id: the primary key.

    :unique_id: a universal unique identifier string that identifies the object.

    :mx_tot:    the x-component of the total remanence vector (over the volume).

    :my_tot:    the y-component of the total remanence vector (over the volume).

    :mz_tot:    the z-component of the total remanence vector (over the volume).



    """
    __tablename__ = 'model'

    id = Column(Integer, primary_key=True, nullable=False)
    unique_id = Column(String, default=new_unique_id, nullable=False)
    mx_tot = Column(Float, nullable=True)
    my_tot = Column(Float, nullable=True)
    mz_tot = Column(Float, nullable=True)
    vx_tot = Column(Float, nullable=True)
    vy_tot = Column(Float, nullable=True)
    vz_tot = Column(Float, nullable=True)
    h_tot = Column(Float, nullable=True)
    adm_tot = Column(Float, nullable=True)
    e_typical = Column(Float, nullable=True)
    e_anis = Column(Float, nullable=True)
    e_ext = Column(Float, nullable=True)
    e_demag = Column(Float, nullable=True)
    e_exch1 = Column(Float, nullable=True)
    e_exch2 = Column(Float, nullable=True)
    e_exch3 = Column(Float, nullable=True)
    e_exch4 = Column(Float, nullable=True)
    e_tot = Column(Float, nullable=True)
    max_energy_evaluations = Column(Integer, nullable=False)
    last_modified = Column(DateTime, default=now(), onupdate=now(), nullable=False)
    created = Column(DateTime, default=now(), nullable=False)

    geometry_id = Column(Integer, ForeignKey('geometry.id'), nullable=False)
    geometry = relationship('Geometry', uselist=False)

    materials = relationship("ModelMaterialAssociation")

    start_magnetization_id = Column(Integer, ForeignKey('field.id'), nullable=False)
    start_magnetization = relationship('Field', uselist=False, foreign_keys=[start_magnetization_id])

    external_field_id = Column(Integer, ForeignKey('field.id'), nullable=True)
    external_field = relationship('Field', uselist=False, foreign_keys=[external_field_id])

    running_status_id = Column(Integer, ForeignKey('running_status.id'), nullable=False)
    running_status = relationship('RunningStatus', uselist=False)

    model_run_data_id = Column(Integer, ForeignKey('model_run_data.id'), nullable=False)
    model_run_data = relationship('ModelRunData', uselist=False)

    model_report_data_id = Column(Integer, ForeignKey('model_report_data.id'), nullable=False)
    model_report_data = relationship('ModelReportData', uselist=False)

    mdata_id = Column(Integer, ForeignKey('metadata.id'), nullable=False)
    mdata = relationship('Metadata', uselist=False)

    legacy_model_info_id = Column(Integer, ForeignKey('legacy_model_info.id'), nullable=True)
    legacy_model_info = relationship('LegacyModelInfo', uselist=False)

    nebs = relationship('NEBModelSplit', back_populates='model')

    UniqueConstraint('unique_id', name='uniq_model_01')


class NEBCalculationType(Base):
    r"""
    The type of neb calculation used to calculate the data associated with a
    NEB. For example:
       neb          NEB calculation based on the Nudged Elastic Band (NEB)
       fs_heuristic NEB calculation based on Fabian & Shcherbakov (arXiv:1702.00070v1)

    """
    __tablename__ = 'neb_calculation_type'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    last_modified = Column(DateTime, default=now(), onupdate=now(), nullable=False)
    created = Column(DateTime, default=now(), nullable=False)


class NEBRunData(Base):
    __tablename__ = 'neb_run_data'

    id = Column(Integer, primary_key=True, nullable=False)
    has_script = Column(Boolean, default=False, nullable=False)
    has_stdout = Column(Boolean, default=False, nullable=False)
    has_stderr = Column(Boolean, default=False, nullable=False)
    has_energy_log = Column(Boolean, default=False, nullable=False)
    has_tecplot = Column(Boolean, default=False, nullable=False)
    has_neb_energies = Column(Boolean, default=False, nullable=False)
    last_modified = Column(DateTime, default=now(), onupdate=now(), nullable=False)
    created = Column(DateTime, default=now(), nullable=False)


class NEBReportData(Base):
    __tablename__ = 'neb_report_data'

    id = Column(Integer, primary_key=True, nullable=False)
    has_x_thumb_png = Column(Boolean, default=False, nullable=False)
    has_y_thumb_png = Column(Boolean, default=False, nullable=False)
    has_z_thumb_png = Column(Boolean, default=False, nullable=False)
    has_x_png = Column(Boolean, default=False, nullable=False)
    has_y_png = Column(Boolean, default=False, nullable=False)
    has_z_png = Column(Boolean, default=False, nullable=False)
    last_modified = Column(DateTime, default=now(), onupdate=now(), nullable=False)
    created = Column(DateTime, default=now(), nullable=False)


class NEB(Base):
    __tablename__ = 'neb'

    id = Column(Integer, primary_key=True, nullable=False)
    unique_id = Column(String, default=new_unique_id, nullable=False)
    spring_constant = Column(Float, nullable=True)
    curvature_weight = Column(Float, nullable=True)
    no_of_points = Column(Integer, nullable=True)
    max_energy_evaluations = Column(Integer, nullable=False, default=10000)
    max_path_evaluations = Column(Integer, nullable=False, default=5000)
    last_modified = Column(DateTime, default=now(), onupdate=now(), nullable=False)
    created = Column(DateTime, default=now(), nullable=False)

    external_field_id = Column(Integer, ForeignKey('field.id'), nullable=True)
    external_field = relationship('Field', uselist=False, foreign_keys=[external_field_id])

    start_model_id = Column(Integer, ForeignKey('model.id'), nullable=False)
    start_model = relationship('Model', uselist=False, foreign_keys=[start_model_id])

    end_model_id = Column(Integer, ForeignKey('model.id'), nullable=False)
    end_model = relationship('Model', uselist=False, foreign_keys=[end_model_id])

    parent_neb_id = Column(Integer, ForeignKey('neb.id'), default=None, nullable=True)
    parent_neb = relationship('NEB', uselist=False, foreign_keys=[parent_neb_id], remote_side=[id])

    neb_calculation_type_id = Column(Integer, ForeignKey('neb_calculation_type.id'), nullable=False)
    neb_calculation_type = relationship('NEBCalculationType')

    neb_run_data_id = Column(Integer, ForeignKey('neb_run_data.id'), nullable=False)
    neb_run_data = relationship('NEBRunData')

    neb_report_data_id = Column(Integer, ForeignKey('neb_report_data.id'), nullable=False)
    neb_report_data = relationship('NEBReportData', uselist=False)

    running_status_id = Column(Integer, ForeignKey('running_status.id'), nullable=False)
    running_status = relationship('RunningStatus', uselist=False)

    mdata_id = Column(Integer, ForeignKey('metadata.id'), nullable=False)
    mdata = relationship('Metadata', uselist=False)

    models = relationship('NEBModelSplit', back_populates='neb')

    UniqueConstraint('unique_id', name='uniq_neb_01')


# noinspection PyUnusedLocal
def validate_neb(mapper, connection, value):
    r"""
    Routine to validate the addition of a new NEB path computation.
    """
    if not value.parent_neb:
        # Start and end must have same geometries
        if value.start_model.geometry.id != value.end_model.geometry.id:
            raise ValueError('NEB does not have start/end models with same geometry')

        # Start and end must have same no. of materials
        if len(value.start_model.materials) != len(value.end_model.materials):
            raise ValueError(
                'NEB does not have start/end models with same material. '
                'No of start model materials: {}, no. of end model materials: {}'.format(
                    ' '.join(map(lambda x : '{} {}'.format(x.name, x.temperature), value.start_model.materials)),
                    ' '.join(map(lambda x : '{} {}'.format(x.name, x.temperature), value.end_model.materials))
                )
            )

        # Start and end must have same materials
        start_material_ids = set()
        end_material_ids = set()

        for start_material in value.start_model.materials:
            start_material_ids.add(start_material.material.id)

        for end_material in value.end_model.materials:
            end_material_ids.add(end_material.material.id)

        if start_material_ids != end_material_ids:
            raise ValueError('NEB does not have start/end models with same material.')

        # TODO: add test here to check external_field similar (???)


event.listen(NEB, 'before_insert', validate_neb)


class NEBModelSplit(Base):
    __tablename__ = 'neb_model_split'

    index = Column(Integer, nullable=False)
    last_modified = Column(DateTime, default=now(), onupdate=now(), nullable=False)
    created = Column(DateTime, default=now(), nullable=False)

    neb_id = Column(Integer, ForeignKey('neb.id'), primary_key=True, nullable=False)
    neb = relationship('NEB', back_populates='models')

    model_id = Column(Integer, ForeignKey('model.id'), primary_key=True, nullable=False)
    model = relationship('Model', back_populates='nebs')


class MGSTStartEndPairCount(Base):
    r"""
    This table counts the number of start/end pairs for each mgst (material, geometry,
    size and temperature) tuple that have been selected.
    """
    __tablename__ = 'mgst_start_end_pair_count'
    id = Column(Integer, primary_key=True, nullable=False)
    last_modified = Column(DateTime, default=now(), onupdate=now(), nullable=False)
    created = Column(DateTime, default=now(), nullable=False)
    material = Column(String, nullable=False)
    geometry = Column(String, nullable=False)
    size = Column(String, nullable=False)
    temperature = Column(String, nullable=False)
    pair_count = Column(Integer, nullable=False, default=0)
