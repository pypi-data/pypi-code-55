"""This module contains the Serializer for the WorkerEndpoint class.

Classes:
    WorkerEndpointSerializer: Concrete Serializer for the WorkerEndpoint class.
"""
from typing import Any, List, Optional

from ...core.worker_endpoint import WorkerEndpoint
from ..models import WorkerEndpointModel
from .amnes_object import AmnesObjectSerializer
from .base import Serializer
from .utils import (
    pull_out_amnes_object,
    pull_out_amnes_object_stored,
    raise_if_incorrect_type,
    raise_if_invalid_object_id,
)


class WorkerEndpointSerializer(Serializer):
    """Map data between WorkerEndpoint instances and database."""

    @staticmethod
    def exists_by_id(object_id: int) -> bool:
        """Check if a given WorkerEndpoint exists in the database.

        Args:
            object_id (int): Index of entry in database

        Returns:
            bool: True if an WorkerEndpoint with the given `object_id` exists in the
                  database, False if not.
        """
        raise_if_invalid_object_id(object_id)
        query = WorkerEndpointModel.select().where(WorkerEndpointModel.id == object_id)
        return query.exists()

    @staticmethod
    def insert(instance: WorkerEndpoint, parent: Optional[Any] = None) -> int:
        """Insert Plain-Python-Object WorkerEndpoint into the database.

        Args:
            instance (WorkerEndpoint): Non-Empty Plain-Python-Object
                                       WorkerEndpoint instance.
            parent (Optional[Any]): This serializer does not need a parental reference.
                                    This parameter will be ignored.

        Returns:
            object_id (int): Index of entry in database
        """
        raise_if_incorrect_type(instance, WorkerEndpoint)
        amnes_object_model_id = pull_out_amnes_object_stored(instance)
        worker_endpoint_model_instance = WorkerEndpointModel.create(
            address=instance.address,
            port=instance.port,
            amnes_object=amnes_object_model_id,
        )
        return worker_endpoint_model_instance.get_id()

    @staticmethod
    def insert_bulk(
        instances: List[WorkerEndpoint], parent: Optional[Any] = None
    ) -> List[int]:
        """Insert multiple WorkerEndpoint into the database.

        Args:
            instances (List[WorkerEndpoint]): List of Non-Empty WorkerEndpoint
                                              instances.
            parent (Optional[Any]): This serializer does not need a parental reference.
                                    This parameter will be ignored.

        Returns:
            instances_ids (List[int]): Returns a list of id in the order they were
                                       inserted.
        """
        instances_ids: List[int] = []
        for instance in instances:
            instances_ids.append(WorkerEndpointSerializer.insert(instance))

        return instances_ids

    @staticmethod
    def delete_by_id(object_id: int) -> None:
        """Delete an WorkerEndpoint by id from the database.

        Args:
            object_id (int): Index of entry in database

        Raises:
            ValueError: If corresponding entry of `object_id` does not exist
                        in the database.
        """
        raise_if_invalid_object_id(object_id)
        if not WorkerEndpointSerializer.exists_by_id(object_id):
            raise ValueError("WorkerEndpoint database-entry was not found.")

        worker_endpoint_model_instance = WorkerEndpointModel.get_by_id(object_id)
        AmnesObjectSerializer.delete_by_id(
            worker_endpoint_model_instance.amnes_object.id
        )
        worker_endpoint_model_instance.delete_instance()

    @staticmethod
    def update_by_id(instance: WorkerEndpoint, object_id: int) -> None:
        """Update a WorkerEndpoint entry in the database.

        Args:
            instance (WorkerEndpoint): Plain-Python-Object WorkerEndpoint,
                                       will be updated in the database.
            object_id (int): Unique identification of data-entry.

        Raises:
            ValueError: If corresponding entry of `object_id` does not exist
                        in the database.
        """
        raise_if_invalid_object_id(object_id)
        if not WorkerEndpointSerializer.exists_by_id(object_id):
            raise ValueError("WorkerEndpoint database-entry was not found.")

        worker_endpoint_model_instance = WorkerEndpointModel.get_by_id(object_id)
        amnes_object_updated = pull_out_amnes_object(instance)
        amnes_object_reference = worker_endpoint_model_instance.amnes_object.id

        AmnesObjectSerializer.update_by_id(amnes_object_updated, amnes_object_reference)

        query_update = WorkerEndpointModel.update(
            {"address": instance.address, "port": instance.port}
        ).where(WorkerEndpointModel.id == object_id)

        query_update.execute()

    @staticmethod
    def get_by_id(object_id: int) -> WorkerEndpoint:
        """Returns pre-generated Plain-Python-Object WorkerEndpoint from the database.

        Args:
            object_id (int): Unique identifier, referencing to data-entry
                          inside the database.

        Returns:
            instance (WorkerEndpoint): Non-Empty Plain-Python-Object
                                       WorkerEndpoint instance.

        Raises:
            ValueError: If corresponding entry of `object_id` does not exist
                        in the database.
        """
        raise_if_invalid_object_id(object_id)
        if not WorkerEndpointSerializer.exists_by_id(object_id):
            raise ValueError("WorkerEndpoint database-entry was not found.")

        worker_endpoint_model_instance = WorkerEndpointModel.get_by_id(object_id)
        related_amnes_object = AmnesObjectSerializer.get_by_id(
            worker_endpoint_model_instance.amnes_object
        )
        worker_endpoint_instance = WorkerEndpoint(
            related_amnes_object.slug,
            related_amnes_object.name,
            related_amnes_object.description,
            worker_endpoint_model_instance.address,
            worker_endpoint_model_instance.port,
        )
        worker_endpoint_instance.add_labels(related_amnes_object.labels)
        return worker_endpoint_instance
