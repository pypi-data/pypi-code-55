"""This module contains a concrete, default StorageBackendPeewee.

Classes:
    StorageBackendPeewee: A concrete StorageBackendPeewee of class StorageBackend.
                          It will initialize the database and acts as a layer between
                          the ORM and application.
"""
from logging import Logger
from pathlib import Path
from typing import IO, ItemsView, List, Optional, Type

import peewee
from peewee import IntegrityError

from ...core.amnes_object import AmnesObject
from ...core.amnes_project import AmnesProject
from ...core.experiment import ConcreteExperiment, ExperimentState
from ...exec.logging import InstanceLogging
from ..database.database_abstract import AmnesDatabaseAbstract
from ..models import (
    ANNOTATIONMODEL_LABELMODEL_THROUGH,
    CONCRETEEXPERIMENTMODEL_AMNESOBJECTMODEL_THROUGH,
    DATABASE_PROXY,
    EXPERIMENTTEMPLATEMODEL_AMNESOBJECTMODEL_THROUGH,
    AmnesObjectModel,
    AmnesProjectModel,
    AnnotationModel,
    BaseModel,
    ConcreteExperimentModel,
    ConcreteExperimentNodeModel,
    ExperimentNodeTemplateModel,
    ExperimentSequenceModel,
    ExperimentTemplateModel,
    FileModel,
    LabelModel,
    NodeTaskModel,
    ParameterSetModel,
    WorkerEndpointModel,
)
from ..serializer import (
    AmnesObjectSerializer,
    AmnesProjectSerializer,
    ConcreteExperimentSerializer,
    FileSerializer,
)
from ..serializer.file import FileObject
from .storage_backend import (
    ConcreteExperimentReference,
    FileDetails,
    FileList,
    StorageBackend,
)

MODELS = [
    AmnesObjectModel,
    LabelModel,
    AnnotationModel,
    ANNOTATIONMODEL_LABELMODEL_THROUGH,
    FileModel,
    ParameterSetModel,
    WorkerEndpointModel,
    NodeTaskModel,
    ExperimentNodeTemplateModel,
    ConcreteExperimentNodeModel,
    ConcreteExperimentModel,
    CONCRETEEXPERIMENTMODEL_AMNESOBJECTMODEL_THROUGH,
    ExperimentTemplateModel,
    EXPERIMENTTEMPLATEMODEL_AMNESOBJECTMODEL_THROUGH,
    ExperimentSequenceModel,
    AmnesProjectModel,
]


def _get_concrete_experiment_id_by_reference(
    reference: ConcreteExperimentReference,
) -> int:
    concrete_experiment_aom = AmnesObjectModel.alias()
    amnes_project_aom = AmnesObjectModel.alias()
    parameter_set_aom = AmnesObjectModel.alias()
    query = (
        ConcreteExperimentModel.select(ConcreteExperimentModel)
        .join(concrete_experiment_aom)
        .switch(ConcreteExperimentModel)
        .join(ExperimentSequenceModel)
        .join(ParameterSetModel)
        .join(parameter_set_aom)
        .switch(ExperimentSequenceModel)
        .join(AmnesProjectModel)
        .join(amnes_project_aom)
        .where(
            (amnes_project_aom.slug == reference.amnes_project_slug)
            & (
                (concrete_experiment_aom.slug == reference.concrete_experiment_slug)
                & (parameter_set_aom.slug == reference.sequence_parameter_set_slug)
            )
        )
    )
    return query[0].id


class StorageBackendPeewee(StorageBackend, InstanceLogging):
    """The StorageBackendPeewee class initializes the database with its tables.

    A StorageBackendPeewee a singleton and proxies persisted data between the
    peewee ORM and the application logic. This StorageBackend can be connected to any
    of peewee's supported databases. The wrapper `AmnesDatabaseAbstract` wraps currently
    peewees's Postgresql- and Sqliteadapter.

    Attributes:
        database (AmnesDatabaseAbstract): Database used, by the StorageBackendPeewee
                                          instance
        static_files_dir (str): Path to folder, used by StorageBackend to persist files.

    Examples:
        >>> from amnes.data.manager.storage_backend_peewee import StorageBackendPeewee
        >>> from amnes.data.database import SqliteDatabaseAdapter
        >>> db = SqliteDatabaseAdapter(":memory:", "storage/")
        >>> storage = StorageBackendPeewee(db)
        >>> amnes_project = AmnesProject(...)
        >>> object_id = storage.import_amnes_project(amnes_project)
    """

    def __init__(
        self,
        logger: Logger,
        database: AmnesDatabaseAbstract,
        static_files_dir: str = ".",
    ) -> None:
        """The constructor method for StorageBackend.

        Args:
            logger (Logger): Logger for object instance.
            database (AmnesDatabaseAbstract): An instance of AmnesDatabase. By default
                                              are SqliteDatabaseAdapter and
                                              PostgresqlDatabaseAdapter classes
                                              available.
            static_files_dir (str): Sets the root directory for files, used by the
                                    StorageBackend.
        """
        InstanceLogging.__init__(self, logger)
        peewee.logger = self.logger.getChild("peewee")
        self.database = database
        self._init_database(self.database)
        self._create_tables(self.database, MODELS)
        self.static_files_dir = static_files_dir

    @property
    def database(self) -> AmnesDatabaseAbstract:
        """Currently used instance of database.

        Returns:
            database (AmnesDatabase): Currently used instance of AmnesDatabase.
        """
        return self.__db

    @database.setter
    def database(self, database: AmnesDatabaseAbstract) -> None:
        """Database Setter method.

        Args:
            database (AmnesDatabaseAbstract): AmnesDatabase connection for
                                              StorageBackend.
        """
        self.__db = database

    @staticmethod
    def _create_tables(
        database: AmnesDatabaseAbstract, tables: List[Type[BaseModel]]
    ) -> None:
        """Creates tables for given models inside the selected database.

        Args:
            database (AmnesDatabaseAbstract): Instance of database from Peewee
            tables (List[Type[BaseModel]]): A list of models,
                                  where each of them will get its own table.
        """
        database.create_tables(tables)

    @staticmethod
    def _init_database(database: AmnesDatabaseAbstract) -> None:
        """Initializes database for the Models.

        The database instance will be passed to all Models via proxy.
        The database must be a valid instance from Peewee, such as SqliteDatabase
        or PostgresqlDatabase.

        Args:
            database (AmnesDatabaseAbstract): AmnesDatabase connection for
                                              StorageBackend.
        """
        DATABASE_PROXY.initialize(database)

    @property
    def static_files_dir(self) -> str:
        """str: Path to a static folder, where data will be stored.

        Returns:
            path (str): The current path where all static files will be stored.
        """
        return str(self.__static_files_dir.absolute())

    @static_files_dir.setter
    def static_files_dir(self, path: str) -> None:
        """Setter function for static_files_dir.

        Args:
            path (str): Path to a Folder with read and write access.

        Raises:
            TypeError: If `path` is not of type string.
            FileNotFoundError: If `path` to folder does not exist in filesystem.
            ValueError: If `path` does not point to an existing folder.
        """
        if not isinstance(path, str):
            raise TypeError("The static path is not of type string.")

        if not Path(path).exists():
            raise FileNotFoundError("Folder does not exist.")

        if not Path(path).is_dir():
            raise ValueError("Path does not point to a folder.")

        self.__static_files_dir = Path(path)

    def import_amnes_project(self, amnes_project: AmnesProject) -> int:
        """Imports and persists an instance of AmnesProject.

        A StorageBackend stores the full hierarchy of an AmnesProject. The
        implementation of a StorageBackend might vary. - It can be a database,
        Data lake or even the direct filesystem.

        Args:
            amnes_project (AmnesProject):  Instance of AmnesProject class, which will
                                           be imported.

        Returns:
            object_id (int): Returns a unique identification number.
        """
        with DATABASE_PROXY.atomic() as transaction:
            try:
                object_id = AmnesProjectSerializer.insert(amnes_project)

            except (TypeError, IntegrityError):
                transaction.rollback()
            else:
                self.logger.debug(f"AmnesProject '{amnes_project.slug}' imported.")
                return object_id
        return -1

    def get_amnes_project_by_slug(self, slug: str) -> Optional[AmnesProject]:
        """Gets an instance of the AmnesProject which has the given slug.

        Args:
            slug (str): Unique slug of the AmnesProject.

        Returns:
            project (AmnesProject): AmnesProject instance referenced by the given slug
                                    or None if slug is not used by any project.
        """
        with DATABASE_PROXY.atomic():
            query = (
                AmnesProjectModel.select(AmnesProjectModel)
                .join(AmnesObjectModel)
                .where(AmnesObjectModel.slug == slug)
            )
            if query.exists():
                project = AmnesProjectSerializer.get_by_id(query[0].id)
                return project
            return None

    def update_concrete_experiment(
        self,
        concrete_experiment: ConcreteExperiment,
        reference: ConcreteExperimentReference,
    ) -> int:
        """Updates an instance of ConcreteExperiment class in the database.

        This method is used to update an entire ConcreteExperiment. If only updating
        the ExperimentState is desired, please consider the faster
        `update_experiment_state` method.

        Args:
            concrete_experiment (ConcreteExperiment): To-be-updated ConcreteExperiment
                                                      instance.
            reference (ConcreteExperimentReference): A namedtuple which acts as the
                                                     directions to the seeked
                                                     ConcreteExperiment.

        Returns:
            object_id (int): Returns the unique object_id of the updated
                             ConcreteExperiment.
        """
        with DATABASE_PROXY.atomic() as transaction:
            concrete_experiment_id = _get_concrete_experiment_id_by_reference(reference)
            try:
                ConcreteExperimentSerializer.update_by_id(
                    concrete_experiment, concrete_experiment_id
                )
            except ValueError:
                transaction.rollback()
            else:
                self.logger.debug(
                    f"ConcreteExperiment '"
                    + f"{reference.amnes_project_slug}"
                    + f"${reference.sequence_parameter_set_slug}"
                    + f"${reference.concrete_experiment_slug}"
                    + f"' with ID {concrete_experiment_id} updated."
                )
                return concrete_experiment_id
        return -1

    def update_experiment_states(
        self,
        states: ItemsView[int, ExperimentState],
        reference: ConcreteExperimentReference,
    ) -> int:
        """Updates multiple ExperimentStates of a ConcreteExperiment in the database.

        This method updates only the states and related repetitions of
        a ConcreteExperiment.

        Args:
            states (ItemsView[int, ExperimentState]): ItemsView of dictionary with all
                    states which will update the states of the ConcreteExperiment in
                    the database. The key is a positive number, which describes the
                    repetition of specified ExperimentState. The value describes the
                    relative ExperimentState.
            reference (ConcreteExperimentReference): A namedtuple which acts as the
                                                     reference to the seeked
                                                     ConcreteExperiment.

        Returns:
            object_id (int): Returns the unique object_id of the updated
                             ConcreteExperiment.
        """
        with DATABASE_PROXY.atomic() as transaction:
            object_id = _get_concrete_experiment_id_by_reference(reference)
            try:
                ConcreteExperimentSerializer.update_states_by_id(states, object_id)
            except (TypeError, ValueError):
                transaction.rollback()
            else:
                self.logger.debug(
                    f"Updated states of ConcreteExperiment '"
                    f"{reference.amnes_project_slug}"
                    f"${reference.sequence_parameter_set_slug}"
                    f"${reference.concrete_experiment_slug}"
                    f"' with ID {object_id} to states '{states}'."
                )
                return object_id
        return -1

    def import_file(
        self,
        file_object: IO,
        amnes_object: Optional[AmnesObject] = None,
        reference: Optional[ConcreteExperimentReference] = None,
        repetition: Optional[int] = None,
    ) -> int:
        """Imports and persists a file object.

        It is possible to assign given file object to a already persisted
        ConcreteExperiment.

        Args:
            file_object (IO):  A file object is the returned value of method `open()`.
            amnes_object (Optional[AmnesObject]): Optional AmnesObject, to describe
                                                  inserted file.
            reference (ConcreteExperimentReference): A namedtuple which acts as the
                                                     directions to the seeked
                                                     ConcreteExperiment.
            repetition (Optional[int]): Selected repetition in `concrete_experiment`.
                                        File object reference will be added internally
                                        to selected repetition.

        Returns:
            file_id (int): Returns a unique file identification number.
        """
        with DATABASE_PROXY.atomic() as transaction:
            concrete_experiment: Optional[ConcreteExperimentModel] = None
            if reference and repetition:
                concrete_experiment_id = _get_concrete_experiment_id_by_reference(
                    reference
                )
                concrete_experiment = ConcreteExperimentModel.get_by_id(
                    concrete_experiment_id
                )
            try:
                file_id = FileSerializer.insert(
                    file_object,
                    self.__static_files_dir,
                    amnes_object,
                    concrete_experiment,
                    repetition,
                )
            except (ValueError, TypeError):
                transaction.rollback()
            else:
                self.logger.debug(f"File with ID {file_id} imported.")
                return file_id
        return -1

    def load_file_by_id(self, file_id: int) -> FileObject:
        """Returns a file object for a given file_id.

        Args:
            file_id (int): Reference to expected file.

        Returns:
            file_object (IO): Returns a file object which can be used as a
                              contextmanager, to read the file.
        """
        with DATABASE_PROXY.atomic():
            return FileSerializer.get_by_id(file_id, self.__static_files_dir)

    def load_file_object_by_id(self, file_id: int) -> IO:
        """Returns a file object for a given file_id.

        Args:
            file_id (int): Reference to expected file.

        Returns:
            file_object (IO): Returns a file object which can be used as a
                              contextmanager, to read the file.
        """
        with DATABASE_PROXY.atomic():
            file_object, *_ = FileSerializer.get_by_id(file_id, self.__static_files_dir)
        return file_object

    @staticmethod
    def get_file_ids_of_experiment(reference: ConcreteExperimentReference) -> FileList:
        """Returns a list of tuples with file_id, repetition and AmnesObject.

        Args:
            reference (ConcreteExperimentReference): A namedtuple which acts as the
                                                     directions to the seeked
                                                     ConcreteExperiment.

        Returns:
            file_list (FileList): Returns a list of namedtuples, containing the
                                  `file_id`, `repetition` and AmnesObject.
        """
        experiment_id = _get_concrete_experiment_id_by_reference(reference)
        experiment = ConcreteExperimentModel.get_by_id(experiment_id)
        file_list = []
        for file in experiment.stored_files:
            file_id: int = file.id
            repetition: int = file.repetition
            amnes_object: AmnesObject = AmnesObjectSerializer.get_by_id(
                file.amnes_object.id
            )
            file_list.append(
                FileDetails(
                    file_id=file_id, repetition=repetition, amnes_object=amnes_object
                )
            )
        return file_list
