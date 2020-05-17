"""This module contains the Serializer for the ParameterSet class.

Classes:
    ParameterSetSerializer: Concrete Serializer for the ParameterSet class.
"""
import json
from typing import Any, Dict, List

from ...core.amnes_object import AmnesObject
from ...core.parameter_set import ParameterSet
from ..models import ParameterSetModel
from .amnes_object import AmnesObjectSerializer
from .base import Serializer


class ParameterSetSerializer(Serializer):
    """Map data between ParameterSet instances and database."""

    @staticmethod
    def exists_by_id(object_id: int) -> bool:
        """Check if a given ParameterSet exists in the database.

        Args:
            object_id (int): Index of entry in database

        Returns:
            bool: True if an ParameterSet with the given `object_id` exists in the
                  database, False if not.
        """
        ParameterSetSerializer._check_object_id(object_id)

        query = ParameterSetModel.select().where(ParameterSetModel.id == object_id)
        return query.exists()

    @staticmethod
    def insert(instance: ParameterSet, parent: int = None) -> int:
        """Insert Plain-Python-Object ParameterSet into the database.

        Args:
            instance (ParameterSet): Non-Empty Plain-Python-Object
                                     ParameterSet instance.
            parent (int): Optional reference to AmnesProjectModel instance,
                          if ParameterSet has an AmnesProject as a parent.

        Returns:
            object_id (int): Index of entry in database
        """
        ParameterSetSerializer._check_parameterset_type(instance)

        amnes_object = AmnesObject(
            instance.slug, instance.name, instance.description, instance.labels
        )
        amnes_object_id = AmnesObjectSerializer.insert(amnes_object)
        parameter_set_model_instance = ParameterSetModel.create(
            amnes_object=amnes_object_id,
            parameters=json.dumps(list(instance.parameters)),
            assignments=json.dumps(dict(instance.assignments)),
            amnes_project=parent,
        )
        return parameter_set_model_instance.get_id()

    @staticmethod
    def insert_bulk(instances: List[ParameterSet], parent: int = None) -> List[int]:
        """Insert multiple ParameterSets into the database.

        Args:
            instances (List[ParameterSet]): List of Non-Empty ParameterSet instances.
            parent (int): Optional reference to AmnesProjectModel instance,
                          if ParameterSet has an AmnesProject as a parent.

        Returns:
            instances_ids (List[int]): Returns a list of id in the order they were
                                       inserted.
        """
        instances_ids: List[int] = []
        for parameter_set in instances:
            instances_ids.append(ParameterSetSerializer.insert(parameter_set, parent))

        return instances_ids

    @staticmethod
    def delete(instance: Any) -> None:
        """Not implemented yet, since the parent model is missing.

        Args:
            instance (Any): A reference to the parent PPO of ParameterSet.
                            Not implemented yet.
        """

    @staticmethod
    def delete_by_id(object_id: int) -> None:
        """Delete an ParameterSet by id from the database.

        Args:
            object_id (int): Index of entry in database
        """
        ParameterSetSerializer._check_id_existence(object_id)

        parameter_set_model_instance: ParameterSetModel = ParameterSetModel.get_by_id(
            object_id
        )
        AmnesObjectSerializer.delete_by_id(parameter_set_model_instance.amnes_object)
        parameter_set_model_instance.delete_instance()

    @staticmethod
    def update_by_id(instance: ParameterSet, object_id: int) -> None:
        """Update a ParameterSet in the database.

        Args:
            instance (ParameterSet): Plain-Python-Object ParameterSet,
                                    will be updated in the database.
            object_id (int): Unique identification of data-entry
        """
        ParameterSetSerializer._check_parameterset_type(instance)
        ParameterSetSerializer._check_id_existence(object_id)

        parameter_set_model_instance: ParameterSetModel = ParameterSetModel.get_by_id(
            object_id
        )
        amnes_object_updated = AmnesObject(
            instance.slug, instance.name, instance.description, instance.labels
        )
        amnes_object_id = parameter_set_model_instance.amnes_object
        AmnesObjectSerializer.update_by_id(amnes_object_updated, amnes_object_id)
        query_update = ParameterSetModel.update(
            {
                "parameters": json.dumps(list(instance.parameters)),
                "assignments": json.dumps(dict(instance.assignments)),
            }
        ).where(ParameterSetModel.id == object_id)

        query_update.execute()

    @staticmethod
    def get_by_id(object_id: int) -> ParameterSet:
        """Returns pre-generated Plain-Python-Object ParameterSet from the database.

        Args:
            object_id (int): Unique identifier, referencing to data-entry
                          inside the database.

        Returns:
            instance (ParameterSet): Non-Empty Plain-Python-Object
                                     ParameterSet instance.
        """
        ParameterSetSerializer._check_id_existence(object_id)

        parameter_set_model_instance: ParameterSetModel = ParameterSetModel.get_by_id(
            object_id
        )
        amnes_object_instance = AmnesObjectSerializer.get_by_id(
            parameter_set_model_instance.amnes_object
        )
        parameter_set_instance = ParameterSet(
            amnes_object_instance.slug,
            amnes_object_instance.name,
            amnes_object_instance.description,
        )
        parameter_set_instance.add_labels(amnes_object_instance.labels)
        parameters: List = json.loads(parameter_set_model_instance.parameters)

        for parameter in parameters:
            parameter_set_instance.add_parameter(parameter)
        assignments: Dict = json.loads(parameter_set_model_instance.assignments)

        for parameter, value in assignments.items():
            parameter_set_instance.add_assignments(parameter, value)

        return parameter_set_instance

    @staticmethod
    def _check_parameterset_type(instance: ParameterSet) -> None:
        """Checks if `instance` is of type `ParameterSet`.

         Args:
            instance (ParameterSet): Plain-Python-Object ParameterSet.

        Raises:
            TypeError: If `instance` is not of type `ParameterSet`.
        """
        if not isinstance(instance, ParameterSet):
            raise TypeError("Instance is not of type ParameterSet.")

    @staticmethod
    def _check_object_id(object_id: int) -> None:
        """Checks if `object_id` is a valid id.

        A valid id is an integer, higher than 0.

        Args:
            object_id (int): Unique identifier, referencing to data-entry
                          inside the database.

        Raises:
            ValueError: If the `object_id` is not a valid id.
        """
        if object_id < 1:
            raise ValueError("The `object_id` must be 1 or higher.")

    @staticmethod
    def _check_id_existence(object_id: int) -> None:
        """Checks if `object_id` exists in the ParameterSet-Database-Table.

        Args:
            object_id (int): Unique identifier, referencing to data-entry
                          inside the database.

        Raises:
            ValueError: If corresponding entry of `object_id` does not exist
                        in the database.
        """
        ParameterSetSerializer._check_object_id(object_id)
        if not ParameterSetSerializer.exists_by_id(object_id):
            raise ValueError("ParameterSet database-entry was not found.")
