"""This module contains all necessary definitions for StorageBackend.

Classes:
    FileDetails: NamedTuple, acting as a detailed description for a file.
    ConcreteExperimentReference: NamedTuple, acting as a reference to a
                                 ConcreteExperiment in the database.
    StorageBackend: An abstraction for concrete StorageBackends,
                    which will all inherit from StorageBackend.
"""
from abc import ABCMeta, abstractmethod
from typing import IO, ItemsView, NamedTuple, Optional, Sequence

from ...core.amnes_object import AmnesObject
from ...core.amnes_project import AmnesProject
from ...core.experiment import ConcreteExperiment, ExperimentState
from ..serializer.file import FileObject


class FileDetails(NamedTuple):
    """NamedTuple which defines a file.

    The file is decorated by a unique id, repetition and AmnesObject.

    Attributes:
        file_id (int): Unique file identifier.
        repetition (Optional[int]): Repetition of files parent ConcreteExperiment.
        amnes_object (Optional[AmnesObject]): AmnesObject describing the file.
    """

    file_id: int
    repetition: Optional[int]
    amnes_object: Optional[AmnesObject]


FileList = Sequence[FileDetails]


class ConcreteExperimentReference(NamedTuple):
    """NamedTuple which defines the explicit location of a ConcreteExperiment.

    This NamedTuple acts a directions instruction for the StorageBackend.

    Attributes:
        concrete_experiment_slug (str): Slug of seeked ConcreteExperiment Plain-Python-
                                        Object.
        sequence_parameter_set_slug (str): Slug of ParameterSet which is the child of
                                           ConcreteExperiments parent
                                           ExperimentSequence.
        amnes_project_slug (str): Slug of the AmnesProject which contains the seeked
                                  ConcreteExperiment.
    """

    concrete_experiment_slug: str
    sequence_parameter_set_slug: str
    amnes_project_slug: str


class StorageBackend(metaclass=ABCMeta):
    """Abstract StorageBackend class, from which all StorageBackend classes inherit.

    This class defines essential methods of a StorageBackend.
    A StorageBackend creates an additional layer between persisted data and
    the rest of the application. Data might be persisted by a database/ data lake or
    filesystem.
    """

    @abstractmethod
    def import_amnes_project(self, amnes_project: AmnesProject) -> int:
        """Imports and persists an instance of AmnesProject.

        A StorageBackend stores the full hierarchy of an AmnesProject. The
        implementation of a StorageBackend might vary. - It can be a database,
        Data lake or even the direct filesystem.

        Args:
            amnes_project (AmnesProject):  Instance of AmnesProject class, which will
                                           be imported.
        """

    @abstractmethod
    def get_amnes_project_by_slug(self, slug: str) -> Optional[AmnesProject]:
        """Gets an instance of the AmnesProject which has the given slug.

        Args:
            slug (str): Unique slug of the AmnesProject.
        """

    @abstractmethod
    def update_concrete_experiment(
        self,
        concrete_experiment: ConcreteExperiment,
        reference: ConcreteExperimentReference,
    ) -> int:
        """Updates an instance of ConcreteExperiment class.

        This method might be used to update the state of a ConcreteExperiment.

        Args:
            concrete_experiment (ConcreteExperiment): To-be-updated ConcreteExperiment
                                                      instance.
            reference (ConcreteExperimentReference): A namedtuple which acts as the
                                                     directions to the seeked
                                                     ConcreteExperiment.
        """

    @abstractmethod
    def update_experiment_states(
        self,
        states: ItemsView[int, ExperimentState],
        reference: ConcreteExperimentReference,
    ) -> int:
        """Updates a specific ExperimentState in a ConcreteExperiment.

        Args:
            states (ItemsView[int, ExperimentState]): ItemsView of dictionary with all
                    states which will update the states of the ConcreteExperiment in
                    the database. The key is a positive number, which describes the
                    repetition of specified ExperimentState. The value describes the
                    relative ExperimentState.
            reference (ConcreteExperimentReference): A namedtuple which acts as the
                                                     reference to the seeked
                                                     ConcreteExperiment.
        """

    @abstractmethod
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
        """

    @abstractmethod
    def load_file_by_id(self, file_id: int) -> FileObject:
        """Returns a file with metadata for a given file_id.

        Args:
            file_id (int): Reference to expected file.
        """

    @abstractmethod
    def load_file_object_by_id(self, file_id: int) -> IO:
        """Returns a file object for a given file_id.

        Args:
            file_id (int): Reference to expected file.
        """

    @staticmethod
    @abstractmethod
    def get_file_ids_of_experiment(reference: ConcreteExperimentReference) -> FileList:
        """Returns a list of tuples with file_id, repetition and AmnesObject.

        Args:
            reference (ConcreteExperimentReference): A namedtuple which acts as the
                                                     directions to the seeked
                                                     ConcreteExperiment.
        """
