"""This module contains the Serializer for the ExperimentNode module.

Classes:
    ExperimentNodeTemplateSerializer: Concrete Serializer for the
                                      ExperimentNodeTemplate module.
    ConcreteExperimentNodeSerializer: Concrete Serializer for the
                                      ConcreteExperimentNode module.
"""
from typing import List, Optional, Sequence, Type, Union

from ...core.experiment_node import ConcreteExperimentNode, ExperimentNodeTemplate
from ...core.node_task import NodeTask
from ..models import (
    ConcreteExperimentModel,
    ConcreteExperimentNodeModel,
    ExperimentNodeTemplateModel,
    ExperimentTemplateModel,
)
from .amnes_object import AmnesObjectSerializer
from .base import Serializer
from .node_task import ExperimentNodeModel, NodeTaskSerializer
from .utils import (
    model_instance_exists_by_id,
    pull_out_amnes_object,
    pull_out_amnes_object_stored,
    raise_if_incorrect_type,
    raise_if_invalid_object_id,
)
from .worker_endpoint import WorkerEndpointSerializer

ExperimentNode = Union[ExperimentNodeTemplate, ConcreteExperimentNode]
ExperimentModel = Optional[Union[ConcreteExperimentModel, ExperimentNodeTemplateModel]]


def _experiment_node_insert(
    instance: ExperimentNode,
    experiment_node_model: Type[ExperimentNodeModel],
    parent: Optional[ExperimentModel] = None,
) -> int:
    """Inserts an ExperimentNode into the database.

    An ExperimentNode instance is a Plain-Python-Object from the core module.
    This method will insert its WorkerEndpoint, NodeTasks and related AmnesObject.
    Moreover an optional parent can be passed, such that an ExperimentModel receives
    a backreference `nodes`.

    Args:
        instance (ExperimentNode): Non-Empty ExperimentNode instance.
        experiment_node_model (Type[ExperimentNodeModel]): Model used for
                                                           create-method.
        parent (Optional[ExperimentModel]): Parent model for reference.

    Returns:
        object_id (int): Index of entry in database.
    """
    amnes_object_model_id = pull_out_amnes_object_stored(instance)
    endpoint_model_id = WorkerEndpointSerializer.insert(instance.endpoint)
    exp_node_model_instance = experiment_node_model.create(
        endpoint=endpoint_model_id,
        amnes_object=amnes_object_model_id,
        experiment=parent,
    )
    NodeTaskSerializer.insert_bulk(instance.tasks, exp_node_model_instance)
    return exp_node_model_instance.get_id()


def _experiment_nodes_insert_bulk(
    instances: Sequence[ExperimentNode],
    experiment_node_model: Type[ExperimentNodeModel],
    parent: Optional[ExperimentModel] = None,
) -> List[int]:
    """Inserts multiple ExperimentNodes into the database.

    Args:
        instances (Sequence[ExperimentNode]): List of Non-Empty ExperimentNode
                                              instances.
        experiment_node_model (Type[ExperimentNodeModel]): Model used for
                                                           create-method.
        parent (Optional[ExperimentModel]): Optional parental reference.

    Returns:
        instances_ids (List[int]): Returns a list of id in the order they were
                                   inserted.
    """
    instances_ids: List[int] = []
    for instance in instances:
        instances_ids.append(
            _experiment_node_insert(instance, experiment_node_model, parent)
        )
    return instances_ids


def _experiment_node_delete_by_id(
    object_id: int, experiment_node_model: Type[ExperimentNodeModel]
) -> None:
    """Deletes an ExperimentNode by id from the database.

    Args:
        object_id (int): Index of entry in database.
        experiment_node_model (Type[ExperimentNodeModel]): Model used for
                                                           delete_instance-method.
    """
    experiment_node_model_instance = experiment_node_model.get_by_id(object_id)
    WorkerEndpointSerializer.delete_by_id(experiment_node_model_instance.endpoint.id)
    for task in experiment_node_model_instance.tasks:
        NodeTaskSerializer.delete_by_id(task.id)
    AmnesObjectSerializer.delete_by_id(experiment_node_model_instance.amnes_object.id)
    experiment_node_model_instance.delete_instance()


def _experiment_node_get_by_id(
    object_id: int,
    experiment_node_model: Type[ExperimentNodeModel],
    experiment_node: Type[ExperimentNode],
) -> ExperimentNode:
    """Returns pre-generated Plain-Python-Object ExperimentNode from the database.

    Args:
        object_id (int): Unique identifier, referencing to data-entry
                      inside the database.
        experiment_node_model (Type[ExperimentNodeModel]): Model used for
                                                           get_by_id-method.
        experiment_node (Type[ExperimentNode]): Class type used for object-creation.

    Returns:
        instance (ExperimentNode): Non-Empty Plain-Python-Object ExperimentNode
                                   instance. Depending on the given arguments,
                                   an ExperimentNode is either an
                                   ExperimentNodeTemplate or a ConcreteExperimentNode.
    """
    experiment_node_model_instance = experiment_node_model.get_by_id(object_id)
    related_amnes_object = AmnesObjectSerializer.get_by_id(
        experiment_node_model_instance.amnes_object
    )
    related_endpoint = WorkerEndpointSerializer.get_by_id(
        experiment_node_model_instance.endpoint.id
    )
    tasks: List[NodeTask] = [
        NodeTaskSerializer.get_by_id(task.id)
        for task in experiment_node_model_instance.tasks
    ]
    experiment_node_instance = experiment_node(
        related_amnes_object.slug,
        related_amnes_object.name,
        related_amnes_object.description,
        related_endpoint,
    )
    experiment_node_instance.add_tasks(tasks)
    experiment_node_instance.add_labels(related_amnes_object.labels)
    return experiment_node_instance


def _experiment_node_update_by_id(
    instance: ExperimentNode,
    object_id: int,
    experiment_node_model: Type[ExperimentNodeModel],
) -> None:
    """Updates a ExperimentNode entry in the database.

    Args:
        instance (ExperimentNode): Plain-Python-Object of ExperimentNodeAbstract, will
                                   be updated in the database.
        object_id (int): Unique identification of data-entry.
        experiment_node_model (Type[ExperimentNodeModel]): Model used for
                                                           get_by_id-method.
    """
    experiment_node_model_instance = experiment_node_model.get_by_id(object_id)
    amnes_object_updated = pull_out_amnes_object(instance)
    amnes_object_reference = experiment_node_model_instance.amnes_object
    AmnesObjectSerializer.update_by_id(amnes_object_updated, amnes_object_reference)
    worker_endpoint_reference = experiment_node_model_instance.endpoint.id
    WorkerEndpointSerializer.update_by_id(instance.endpoint, worker_endpoint_reference)
    for task in experiment_node_model_instance.tasks:
        task.delete_instance()
    NodeTaskSerializer.insert_bulk(instance.tasks, experiment_node_model_instance)


class ExperimentNodeTemplateSerializer(Serializer):
    """Maps data between ExperimentNodeTemplate instances and database."""

    @staticmethod
    def exists_by_id(object_id: int) -> bool:
        """Check if a given ExperimentNodeTemplate exists in the database.

        Args:
            object_id (int): Index of entry in database.

        Returns:
            bool: True if an ExperimentNodeTemplate with the given `object_id` exists in
                  the database, False if not.
        """
        raise_if_invalid_object_id(object_id)
        return model_instance_exists_by_id(object_id, ExperimentNodeTemplateModel)

    @staticmethod
    def insert(
        instance: ExperimentNodeTemplate,
        parent: Optional[ExperimentTemplateModel] = None,
    ) -> int:
        """Inserts Plain-Python-Object ExperimentNodeTemplate into the database.

        Args:
            instance (ExperimentNodeTemplate): Non-Empty Plain-Python-Object
                                               ExperimentNodeTemplate instance.
            parent (Optional[ExperimentTemplateModel]): Optional parental
                                                        reference.

        Returns:
            object_id (int): Index of entry in database.
        """
        raise_if_incorrect_type(instance, ExperimentNodeTemplate)
        return _experiment_node_insert(instance, ExperimentNodeTemplateModel, parent)

    @staticmethod
    def insert_bulk(
        instances: Sequence[ExperimentNodeTemplate],
        parent: Optional[ExperimentTemplateModel] = None,
    ) -> List[int]:
        """Inserts multiple ExperimentNodeTemplates into the database.

        Args:
            instances (List[ExperimentNodeTemplate]): List of Non-Empty
                                                      ExperimentNodeTemplates
                                                      instances.
            parent (Optional[ExperimentTemplateModel]): Optional parental
                                                        reference.

        Returns:
            instances_ids (List[int]): Returns a list of id in the order they were
                                       inserted.
        """
        return _experiment_nodes_insert_bulk(
            instances, ExperimentNodeTemplateModel, parent
        )

    @staticmethod
    def delete_by_id(object_id: int) -> None:
        """Deletes an ExperimentNodeTemplate by id from the database.

        Args:
            object_id (int): Index of entry in database.

        Raises:
            ValueError: If corresponding entry of `object_id` does not exist
                        in the database.
        """
        raise_if_invalid_object_id(object_id)
        if not ExperimentNodeTemplateSerializer.exists_by_id(object_id):
            raise ValueError("ExperimentNodeTemplate database-entry was not found.")
        _experiment_node_delete_by_id(object_id, ExperimentNodeTemplateModel)

    @staticmethod
    def update_by_id(instance: ExperimentNodeTemplate, object_id: int) -> None:
        """Updates a ExperimentNodeTemplate entry in the database.

        Args:
            instance (ExperimentNodeTemplate): Plain-Python-Object of
                                               ExperimentNodeTemplate, will be updated
                                               in the database.
            object_id (int): Unique identification of data-entry.

        Raises:
            ValueError: If corresponding entry of `object_id` does not exist
                        in the database.
            TypeError: If `instance` is not of type ExperimentNodeTemplate.
        """
        raise_if_invalid_object_id(object_id)
        if not ExperimentNodeTemplateSerializer.exists_by_id(object_id):
            raise ValueError("ExperimentNodeTemplate database-entry was not found.")

        if not isinstance(instance, ExperimentNodeTemplate):
            raise TypeError("Given `instance` is not of type ExperimentNodeTemplate")

        _experiment_node_update_by_id(instance, object_id, ExperimentNodeTemplateModel)

    @staticmethod
    def get_by_id(object_id: int) -> ExperimentNodeTemplate:
        """Returns pre-generated ExperimentNodeTemplate from the database.

        Args:
            object_id (int): Unique identifier, referencing to data-entry
                          inside the database.

        Returns:
            instance (ExperimentNodeTemplate): Non-Empty Plain-Python-Object
                                               ExperimentNodeTemplate instance.

        Raises:
            ValueError: If corresponding entry of `object_id` does not exist
                        in the database.
            TypeError: If internal method `_experiment_node_get_by_id` does not
                       return object of type ExperimentNodeTemplate.
        """
        raise_if_invalid_object_id(object_id)
        if not ExperimentNodeTemplateSerializer.exists_by_id(object_id):
            raise ValueError("ExperimentNodeTemplate database-entry was not found.")
        experiment_node = _experiment_node_get_by_id(
            object_id, ExperimentNodeTemplateModel, ExperimentNodeTemplate
        )
        if not isinstance(experiment_node, ExperimentNodeTemplate):
            raise TypeError("ExperimentNodeTemplate could not be generated.")
        return experiment_node


class ConcreteExperimentNodeSerializer(Serializer):
    """Maps data between ConcreteExperimentNode instances and database."""

    @staticmethod
    def exists_by_id(object_id: int) -> bool:
        """Checks if a given ConcreteExperimentNode exists in the database.

        Args:
            object_id (int): Index of entry in database.

        Returns:
            bool: True if an ConcreteExperimentNode with the given `object_id` exists in
                  the database, False if not.
        """
        raise_if_invalid_object_id(object_id)
        return model_instance_exists_by_id(object_id, ConcreteExperimentNodeModel)

    @staticmethod
    def insert(
        instance: ConcreteExperimentNode,
        parent: Optional[ConcreteExperimentModel] = None,
    ) -> int:
        """Inserts Plain-Python-Object ConcreteExperimentNode into the database.

        Args:
            instance (ConcreteExperimentNode): Non-Empty Plain-Python-Object
                                               ConcreteExperimentNode instance.
            parent (Optional[ConcreteExperimentModel]): Optional parental
                                                        reference.

        Returns:
            object_id (int): Index of entry in database.
        """
        raise_if_incorrect_type(instance, ConcreteExperimentNode)
        return _experiment_node_insert(instance, ConcreteExperimentNodeModel, parent)

    @staticmethod
    def insert_bulk(
        instances: List[ConcreteExperimentNode],
        parent: Optional[ConcreteExperimentModel] = None,
    ) -> List[int]:
        """Inserts multiple ConcreteExperimentNodes into the database.

        Args:
            instances (List[ConcreteExperimentNode]): List of Non-Empty
                                                      ConcreteExperimentNode instances.
            parent (Optional[ConcreteExperimentModel]): Optional parental
                                                        reference.

        Returns:
            instances_ids (List[int]): Returns a list of id in the order they were
                                       inserted.
        """
        return _experiment_nodes_insert_bulk(
            instances, ConcreteExperimentNodeModel, parent
        )

    @staticmethod
    def delete_by_id(object_id: int) -> None:
        """Deletes an ConcreteExperimentNode by id from the database.

        Args:
            object_id (int): Index of entry in database.

        Raises:
            ValueError: If corresponding entry of `object_id` does not exist
                        in the database.
        """
        raise_if_invalid_object_id(object_id)
        if not ConcreteExperimentNodeSerializer.exists_by_id(object_id):
            raise ValueError("ConcreteExperimentNode database-entry was not found.")
        _experiment_node_delete_by_id(object_id, ConcreteExperimentNodeModel)

    @staticmethod
    def update_by_id(instance: ConcreteExperimentNode, object_id: int) -> None:
        """Updates a ConcreteExperimentNode entry in the database.

        Args:
            instance (ConcreteExperimentNode): Plain-Python-Object of
                                               ConcreteExperimentNode, will be updated
                                               in the database.
            object_id (int): Unique identification of data-entry.

        Raises:
            ValueError: If corresponding entry of `object_id` does not exist
                        in the database.
            TypeError: If `instance` is not of type `ConcreteExperimentNode`.
        """
        raise_if_invalid_object_id(object_id)
        if not ConcreteExperimentNodeSerializer.exists_by_id(object_id):
            raise ValueError("ConcreteExperimentNode database-entry was not found.")

        if not isinstance(instance, ConcreteExperimentNode):
            raise TypeError("Given `instance` is not of type ConcreteExperimentNode")

        _experiment_node_update_by_id(instance, object_id, ConcreteExperimentNodeModel)

    @staticmethod
    def get_by_id(object_id: int) -> ConcreteExperimentNode:
        """Returns pre-generated Plain-Python-Object ExperimentNode from the database.

        Args:
            object_id (int): Unique identifier, referencing to data-entry
                          inside the database.

        Returns:
            instance (ConcreteExperimentNode): Non-Empty Plain-Python-Object
                                               ConcreteExperimentNode instance.

        Raises:
            ValueError: If corresponding entry of `object_id` does not exist
                        in the database.
            TypeError: If internal method `_experiment_node_get_by_id` does not
                       return object of type ConcreteExperimentNode.
        """
        raise_if_invalid_object_id(object_id)
        if not ConcreteExperimentNodeSerializer.exists_by_id(object_id):
            raise ValueError("ConcreteExperimentNode database-entry was not found.")
        experiment_node = _experiment_node_get_by_id(
            object_id, ConcreteExperimentNodeModel, ConcreteExperimentNode
        )
        if not isinstance(experiment_node, ConcreteExperimentNode):
            raise TypeError("ConcreteExperimentNode could not be generated.")
        return experiment_node
