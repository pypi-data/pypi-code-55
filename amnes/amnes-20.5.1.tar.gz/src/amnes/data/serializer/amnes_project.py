"""This module contains the Serializer for the AmnesProject class.

Classes:
    AmnesProjectSerializer: Concrete Serializer for the AmnesProject class.
"""
from typing import Any, List, Optional, Sequence

from peewee import IntegrityError

from ...core.amnes_project import AmnesProject
from ...core.experiment_sequence import ExperimentSequence
from ...core.parameter_set import ParameterSet
from ..models import AmnesObjectModel, AmnesProjectModel
from .amnes_object import AmnesObjectSerializer
from .base import Serializer
from .experiment import ExperimentTemplateSerializer
from .experiment_sequence import ExperimentSequenceSerializer
from .parameter_set import ParameterSetSerializer
from .utils import (
    model_instance_exists_by_id,
    pull_out_amnes_object,
    pull_out_amnes_object_stored,
    raise_if_incorrect_type,
    raise_if_invalid_object_id,
)


class AmnesProjectSerializer(Serializer):
    """Maps data between AmnesProject instances and database."""

    @staticmethod
    def exists_by_id(object_id: int) -> bool:
        """Checks if a given AmnesProject exists in the database.

        Args:
            object_id (int): Index of entry in database.

        Returns:
            bool: True if an AmnesProject with the given `object_id` exists in the
                  database, False if not.
        """
        raise_if_invalid_object_id(object_id)
        return model_instance_exists_by_id(object_id, AmnesProjectModel)

    @staticmethod
    def insert(instance: AmnesProject, parent: Optional[Any] = None) -> int:
        """Inserts Plain-Python-Object AmnesProject into the database.

        Args:
            instance (AmnesProject): Non-Empty Plain-Python-Object
                                     AmnesProject instance.
            parent (Optional[Any]): Parental reference is not used in the
                                    AmnesProjectModel/ Serializer.

        Returns:
            object_id (int): Index of entry in database.

        Raises:
            IntegrityError: If given AmnesProject instance exists in the database.
        """
        raise_if_incorrect_type(instance, AmnesProject)
        if AmnesProjectSerializer.__amnes_project_exists(instance):
            raise IntegrityError(
                "An AmnesProject cannot be imported twice. "
                "The slug of an AmnesProject must be unique."
            )
        amnes_object_id = pull_out_amnes_object_stored(instance)
        experiment_template_id = ExperimentTemplateSerializer.insert(instance.template)

        amnes_project_model_instance = AmnesProjectModel.create(
            template=experiment_template_id,
            repetitions=instance.repetitions,
            amnes_object=amnes_object_id,
        )
        AmnesProjectSerializer.__add_parameter_sets(
            amnes_project_model_instance, instance.psets
        )
        AmnesProjectSerializer.__add_experiment_sequences(
            amnes_project_model_instance, instance.sequences
        )
        return amnes_project_model_instance.get_id()

    @staticmethod
    def __amnes_project_exists(instance: AmnesProject) -> bool:
        """Checks if given AmnesProject exists in the database.

        This method compares the slugs of the given AmnesProject and all inserted
        AmnesProjects.

        Args:
            instance (AmnesProject): AmnesProject instance for the check, against
                                     database.

        Returns:
            bool: Returns `True` if the given AmnesProject instance exists in the
                  database and `False` if it does not.
        """
        query = (
            AmnesProjectModel.select(AmnesObjectModel.slug)
            .join(AmnesObjectModel)
            .where(AmnesObjectModel.slug == instance.slug)
        )
        return query.exists()

    @staticmethod
    def insert_bulk(
        instances: Sequence[AmnesProject], parent: Optional[Any] = None
    ) -> List[int]:
        """Inserts multiple ExperimentSequences into the database.

        Args:
            instances (List[AmnesProject]): List of Non-Empty AmnesProject
                                            instances.
            parent (Optional[Any]): Parental reference is not used in the
                                    AmnesProjectModel/ Serializer.

        Returns:
            instances_ids (List[int]): Returns a list of id in the order they were
                                       inserted.
        """
        instances_ids: List[int] = []
        for instance in instances:
            instances_ids.append(AmnesProjectSerializer.insert(instance))
        return instances_ids

    @staticmethod
    def delete_by_id(object_id: int) -> None:
        """Deletes an AmnesProject by id from the database.

        Args:
            object_id (int): Index of entry in database.

        Raises:
            ValueError: If corresponding entry of `object_id` does not exist
                        in the database.
        """
        raise_if_invalid_object_id(object_id)
        if not AmnesProjectSerializer.exists_by_id(object_id):
            raise ValueError("AmnesProject database-entry was not found.")

        ap_model_instance = AmnesProjectModel.get_by_id(object_id)

        AmnesObjectSerializer.delete_by_id(ap_model_instance.amnes_object.id)
        ExperimentTemplateSerializer.delete_by_id(ap_model_instance.template.id)

        AmnesProjectSerializer.__delete_parameter_sets(ap_model_instance)
        AmnesProjectSerializer.__delete_experiment_sequences(ap_model_instance)

        ap_model_instance.delete_instance()

    @staticmethod
    def update_by_id(instance: AmnesProject, object_id: int) -> None:
        """Updates a AmnesProject entry in the database.

        Args:
            instance (AmnesProject): Plain-Python-Object of AmnesProject, will be
                                     updated in the database.
            object_id (int): Unique identification of data-entry.

        Raises:
            ValueError: If corresponding entry of `object_id` does not exist
                        in the database.
        """
        raise_if_invalid_object_id(object_id)
        raise_if_incorrect_type(instance, AmnesProject)
        if not AmnesProjectSerializer.exists_by_id(object_id):
            raise ValueError("AmnesProject database-entry was not found.")

        ap_model_instance = AmnesProjectModel.get_by_id(object_id)
        AmnesProjectSerializer.__update_foreign_keys(ap_model_instance, instance)
        query_update = AmnesProjectModel.update(
            {"repetitions": instance.repetitions}
        ).where(AmnesProjectModel.id == object_id)

        query_update.execute()

    @staticmethod
    def get_by_id(object_id: int) -> AmnesProject:
        """Returns pre-generated AmnesProject instance from the database.

        Args:
            object_id (int): Unique identifier, referencing to data-entry
                          inside the database.

        Returns:
            instance (AmnesProject): Non-Empty Plain-Python-Object
                                     `AmnesProject` instance.

        Raises:
            ValueError: If corresponding entry of `object_id` does not exist
                        in the database.
        """
        raise_if_invalid_object_id(object_id)
        if not AmnesProjectSerializer.exists_by_id(object_id):
            raise ValueError("AmnesProject database-entry was not found.")

        ap_model_instance = AmnesProjectModel.get_by_id(object_id)
        amnes_object = AmnesObjectSerializer.get_by_id(
            ap_model_instance.amnes_object.id
        )
        experiment_template = ExperimentTemplateSerializer.get_by_id(
            ap_model_instance.template.id
        )
        ap_instance = AmnesProject(
            amnes_object.slug,
            amnes_object.name,
            amnes_object.description,
            experiment_template,
            ap_model_instance.repetitions,
        )
        parameter_sets = AmnesProjectSerializer.__get_parameter_sets(ap_model_instance)
        ap_instance.add_psets(parameter_sets)

        experiment_sequences = AmnesProjectSerializer.__get_experiment_sequences(
            ap_model_instance
        )
        ap_instance.add_sequences(experiment_sequences)
        ap_instance.add_labels(amnes_object.labels)
        return ap_instance

    @staticmethod
    def __add_experiment_sequences(
        ap_model_instance: AmnesProjectModel,
        experiment_sequences: List[ExperimentSequence],
    ) -> None:
        """Adds and insert ExperimentSequences to a AmnesProjectModel instance.

        Args:
            ap_model_instance (AmnesProjectModel): Selected AmnesProjectModel.
            experiment_sequences (List[ExperimentSequence]): List of ExperimentSequence
                                                             , which will be added.
        """
        ExperimentSequenceSerializer.insert_bulk(
            experiment_sequences, ap_model_instance
        )

    @staticmethod
    def __add_parameter_sets(
        ap_model_instance: AmnesProjectModel, parameter_sets: List[ParameterSet]
    ) -> None:
        """Adds and insert ParameterSets to a AmnesProjectModel instance.

        Args:
            ap_model_instance (AmnesProjectModel): Selected AmnesProjectModel.
            parameter_sets (List[ParameterSet]): List of ParameterSet,
                                                 which will be added.
        """
        ParameterSetSerializer.insert_bulk(parameter_sets, ap_model_instance)

    @staticmethod
    def __get_experiment_sequences(
        ap_model_instance: AmnesProjectModel,
    ) -> List[ExperimentSequence]:
        experiment_sequences: List[ExperimentSequence] = []
        for experiment_sequence in ap_model_instance.experiment_sequences:
            experiment_sequences.append(
                ExperimentSequenceSerializer.get_by_id(experiment_sequence.id)
            )
        return experiment_sequences

    @staticmethod
    def __get_parameter_sets(
        ap_model_instance: AmnesProjectModel,
    ) -> List[ParameterSet]:
        parameter_sets: List[ParameterSet] = []
        for parameter_set in ap_model_instance.parameter_sets:
            parameter_sets.append(ParameterSetSerializer.get_by_id(parameter_set.id))
        return parameter_sets

    @staticmethod
    def __update_foreign_keys(
        ap_model_instance: AmnesProjectModel, instance: AmnesProject
    ) -> None:
        AmnesProjectSerializer.__update_amnes_object(ap_model_instance, instance)
        ExperimentTemplateSerializer.update_by_id(
            instance.template, ap_model_instance.template.id
        )
        AmnesProjectSerializer.__delete_parameter_sets(ap_model_instance)
        AmnesProjectSerializer.__add_parameter_sets(ap_model_instance, instance.psets)
        AmnesProjectSerializer.__delete_experiment_sequences(ap_model_instance)
        AmnesProjectSerializer.__add_experiment_sequences(
            ap_model_instance, instance.sequences
        )

    @staticmethod
    def __update_amnes_object(
        ap_model_instance: AmnesProjectModel, instance: AmnesProject
    ) -> None:
        amnes_object_updated = pull_out_amnes_object(instance)
        AmnesObjectSerializer.update_by_id(
            amnes_object_updated, ap_model_instance.amnes_object.id
        )

    @staticmethod
    def __delete_experiment_sequences(ap_model_instance: AmnesProjectModel) -> None:
        for experiment_sequence in ap_model_instance.experiment_sequences:
            ExperimentSequenceSerializer.delete_by_id(experiment_sequence.id)

    @staticmethod
    def __delete_parameter_sets(ap_model_instance: AmnesProjectModel) -> None:
        for paramter_set in ap_model_instance.parameter_sets:
            ParameterSetSerializer.delete_by_id(paramter_set.id)
