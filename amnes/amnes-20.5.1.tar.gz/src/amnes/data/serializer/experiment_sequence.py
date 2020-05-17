"""This module contains the Serializer for the ExperimentSequence class.

Classes:
    ExperimentSequenceSerializer: Concrete Serializer for the ExperimentSequence class.
"""
from typing import List, Optional, Sequence

from ...core.experiment import ConcreteExperiment
from ...core.experiment_sequence import ExperimentSequence
from ..models import AmnesProjectModel, ExperimentSequenceModel
from .base import Serializer
from .experiment import ConcreteExperimentSerializer
from .parameter_set import ParameterSetSerializer
from .utils import (
    model_instance_exists_by_id,
    raise_if_incorrect_type,
    raise_if_invalid_object_id,
)


class ExperimentSequenceSerializer(Serializer):
    """Map data between ExperimentSequence instances and database."""

    @staticmethod
    def exists_by_id(object_id: int) -> bool:
        """Checks if a given ExperimentSequence exists in the database.

        Args:
            object_id (int): Index of entry in database.

        Returns:
            bool: True if an ExperimentSequence with the given `object_id` exists in the
                  database, False if not.
        """
        raise_if_invalid_object_id(object_id)
        return model_instance_exists_by_id(object_id, ExperimentSequenceModel)

    @staticmethod
    def insert(
        instance: ExperimentSequence, parent: Optional[AmnesProjectModel] = None
    ) -> int:
        """Inserts Plain-Python-Object ExperimentSequence into the database.

        Args:
            instance (ExperimentSequence): Non-Empty Plain-Python-Object
                                           ExperimentSequence instance.
            parent (Optional[AmnesProjectModel]): Optional parental reference.

        Returns:
            object_id (int): Index of entry in database.
        """
        raise_if_incorrect_type(instance, ExperimentSequence)

        parameter_set_id = ParameterSetSerializer.insert(instance.pset)

        experiment_seq_model_instance = ExperimentSequenceModel.create(
            parameter_set=parameter_set_id, amnes_project=parent
        )
        ExperimentSequenceSerializer.__add_experiments_to_experiments_sequence(
            experiment_seq_model_instance, instance.experiments
        )
        return experiment_seq_model_instance.get_id()

    @staticmethod
    def insert_bulk(
        instances: Sequence[ExperimentSequence],
        parent: Optional[AmnesProjectModel] = None,
    ) -> List[int]:
        """Inserts multiple ExperimentSequences into the database.

        Args:
            instances (List[ExperimentSequence]): List of Non-Empty ExperimentSequence
                                                  instances.
            parent (Optional[AmnesProjectModel]): Optional parental reference.

        Returns:
            instances_ids (List[int]): Returns a list of id in the order they were
                                       inserted.
        """
        instances_ids: List[int] = []
        for instance in instances:
            instances_ids.append(ExperimentSequenceSerializer.insert(instance, parent))
        return instances_ids

    @staticmethod
    def delete_by_id(object_id: int) -> None:
        """Deletes an ExperimentSequence by id from the database.

        Args:
            object_id (int): Index of entry in database.

        Raises:
            ValueError: If corresponding entry of `object_id` does not exist
                        in the database.
        """
        raise_if_invalid_object_id(object_id)
        if not ExperimentSequenceSerializer.exists_by_id(object_id):
            raise ValueError("ExperimentSequence database-entry was not found.")

        experiment_seq_model_instance = ExperimentSequenceModel.get_by_id(object_id)
        ParameterSetSerializer.delete_by_id(
            experiment_seq_model_instance.parameter_set.id
        )
        for experiment in experiment_seq_model_instance.experiments:
            ConcreteExperimentSerializer.delete_by_id(experiment.id)

        experiment_seq_model_instance.delete_instance()

    @staticmethod
    def update_by_id(instance: ExperimentSequence, object_id: int) -> None:
        """Updates a ExperimentSequence entry in the database.

        Args:
            instance (ExperimentSequence): Plain-Python-Object of
                                           ExperimentSequence, will be updated
                                           in the database.
            object_id (int): Unique identification of data-entry.

        Raises:
            ValueError: If corresponding entry of `object_id` does not exist
                        in the database.
        """
        raise_if_invalid_object_id(object_id)
        raise_if_incorrect_type(instance, ExperimentSequence)
        if not ExperimentSequenceSerializer.exists_by_id(object_id):
            raise ValueError("ExperimentSequence database-entry was not found.")

        experiment_seq_model_instance = ExperimentSequenceModel.get_by_id(object_id)
        ParameterSetSerializer.update_by_id(
            instance.pset, experiment_seq_model_instance.parameter_set.id
        )
        ExperimentSequenceSerializer.__delete_experiments(experiment_seq_model_instance)
        ExperimentSequenceSerializer.__add_experiments_to_experiments_sequence(
            experiment_seq_model_instance, instance.experiments
        )

    @staticmethod
    def get_by_id(object_id: int) -> ExperimentSequence:
        """Returns pre-generated ExperimentSequence instance from the database.

        Args:
            object_id (int): Unique identifier, referencing to data-entry
                          inside the database.

        Returns:
            instance (ExperimentSequence): Non-Empty Plain-Python-Object
                                           `ExperimentSequence` instance.

        Raises:
            ValueError: If corresponding entry of `object_id` does not exist
                        in the database.
        """
        raise_if_invalid_object_id(object_id)
        if not ExperimentSequenceSerializer.exists_by_id(object_id):
            raise ValueError("ExperimentSequence database-entry was not found.")

        experiment_seq_model_instance = ExperimentSequenceModel.get_by_id(object_id)
        parameter_set = ParameterSetSerializer.get_by_id(
            experiment_seq_model_instance.parameter_set.id
        )
        experiment_seq_instance = ExperimentSequence(parameter_set)
        experiment_list = ExperimentSequenceSerializer.__get_experiments(
            experiment_seq_model_instance
        )
        experiment_seq_instance.add_experiments(experiment_list)
        return experiment_seq_instance

    @staticmethod
    def __add_experiments_to_experiments_sequence(
        experiment_seq_model_instance: ExperimentSequenceModel,
        experiments: List[ConcreteExperiment],
    ) -> None:
        """Inserts ConcreteExperiments into database adds references to Sequence.

        Args:
            experiment_seq_model_instance (ExperimentSequenceModel): Parent where
                                                                    references will be
                                                                    added.
            experiments (List[ConcreteExperiment]): List of concrete Experiments, which
                                                    will be added.
        """
        ConcreteExperimentSerializer.insert_bulk(
            experiments, experiment_seq_model_instance
        )

    @staticmethod
    def __delete_experiments(
        experiment_seq_model_instance: ExperimentSequenceModel,
    ) -> None:
        for experiment in experiment_seq_model_instance.experiments:
            ConcreteExperimentSerializer.delete_by_id(experiment.id)

    @staticmethod
    def __get_experiments(
        experiment_seq_model_instance: ExperimentSequenceModel,
    ) -> List[ConcreteExperiment]:
        experiment_list: List[ConcreteExperiment] = []
        for experiment in experiment_seq_model_instance.experiments:
            experiment_instance = ConcreteExperimentSerializer.get_by_id(experiment.id)
            experiment_list.append(experiment_instance)
        return experiment_list
