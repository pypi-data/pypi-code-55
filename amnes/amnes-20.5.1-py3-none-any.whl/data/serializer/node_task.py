"""This module contains the Serializer for the NodeTask class.

Classes:
    NodeTaskSerializer: Concrete Serializer for the NodeTask class.
"""
import json
from typing import List, Optional, Union

from ...core.experiment_stage import ExperimentStage
from ...core.node_task import NodeTask, NodeTaskFiles, NodeTaskParams
from ..models import (
    ConcreteExperimentNodeModel,
    ExperimentNodeTemplateModel,
    NodeTaskModel,
)
from .amnes_object import AmnesObjectSerializer
from .base import Serializer
from .utils import (
    pull_out_amnes_object,
    pull_out_amnes_object_stored,
    raise_if_incorrect_type,
    raise_if_invalid_object_id,
)

ExperimentNodeModel = Union[ExperimentNodeTemplateModel, ConcreteExperimentNodeModel]


class NodeTaskSerializer(Serializer):
    """Map data between NodeTask instances and database."""

    @staticmethod
    def exists_by_id(object_id: int) -> bool:
        """Check if a given NodeTask exists in the database.

        Args:
            object_id (int): Index of entry in database

        Returns:
            bool: True if an NodeTask with the given `object_id` exists in the
                  database, False if not.
        """
        raise_if_invalid_object_id(object_id)
        query = NodeTaskModel.select().where(NodeTaskModel.id == object_id)
        return query.exists()

    @staticmethod
    def insert(instance: NodeTask, parent: Optional[ExperimentNodeModel] = None) -> int:
        """Insert Plain-Python-Object NodeTask into the database.

        Args:
            instance (NodeTask): Non-Empty Plain-Python-Object
                                 NodeTask instance.
            parent (Optional[ExperimentNodeModel]): Parent reference for a given
                                                    NodeTask.

        Returns:
            object_id (int): Index of entry in database.
        """
        raise_if_incorrect_type(instance, NodeTask)
        stage_model_id = pull_out_amnes_object_stored(instance.stage)
        amnes_object_model_id = pull_out_amnes_object_stored(instance)
        node_task_model_instance = NodeTaskModel.create(
            module=instance.module,
            stage=stage_model_id,
            params=json.dumps(dict(instance.params.pairs)),
            files=json.dumps(dict(instance.files.pairs)),
            amnes_object=amnes_object_model_id,
            experiment_template_node=parent
            if isinstance(parent, ExperimentNodeTemplateModel)
            else None,
            concrete_experiment_node=parent
            if isinstance(parent, ConcreteExperimentNodeModel)
            else None,
        )
        return node_task_model_instance.get_id()

    @staticmethod
    def insert_bulk(
        instances: List[NodeTask], parent: Optional[ExperimentNodeModel] = None
    ) -> List[int]:
        """Insert multiple NodeTask instances into the database.

        Args:
            instances (List[NodeTask]): List of Non-Empty NodeTask
                                        instances.
            parent (Optional[ExperimentNodeModel]): Parent reference for a given
                                                    NodeTask.

        Returns:
            instances_ids (List[int]): Returns a list of id in the order they were
                                       inserted.
        """
        instances_ids: List[int] = []
        for instance in instances:
            instances_ids.append(NodeTaskSerializer.insert(instance, parent))
        return instances_ids

    @staticmethod
    def delete_by_id(object_id: int) -> None:
        """Delete an NodeTask by id from the database.

        Args:
            object_id (int): Index of entry in database

        Raises:
            ValueError: If corresponding entry of `object_id` does not exist
                        in the database.
        """
        raise_if_invalid_object_id(object_id)
        if not NodeTaskSerializer.exists_by_id(object_id):
            raise ValueError("NodeTask database-entry was not found.")

        node_task_model_instance: NodeTaskModel = NodeTaskModel.get_by_id(object_id)
        AmnesObjectSerializer.delete_by_id(node_task_model_instance.amnes_object.id)
        AmnesObjectSerializer.delete_by_id(node_task_model_instance.stage.id)
        node_task_model_instance.delete_instance()

    @staticmethod
    def update_by_id(instance: NodeTask, object_id: int) -> None:
        """Update a NodeTask entry in the database.

        Args:
            instance (NodeTask): Plain-Python-Object NodeTask,
                                 will be updated in the database.
            object_id (int): Unique identification of data-entry.

        Raises:
            ValueError: If corresponding entry of `object_id` does not exist
                        in the database.
        """
        raise_if_invalid_object_id(object_id)
        if not NodeTaskSerializer.exists_by_id(object_id):
            raise ValueError("NodeTask database-entry was not found.")

        node_task_model_instance: NodeTaskModel = NodeTaskModel.get_by_id(object_id)

        amnes_object_updated = pull_out_amnes_object(instance)
        stage_updated = pull_out_amnes_object(instance.stage)

        amnes_object_reference = node_task_model_instance.amnes_object
        stage_reference = node_task_model_instance.stage

        AmnesObjectSerializer.update_by_id(amnes_object_updated, amnes_object_reference)
        AmnesObjectSerializer.update_by_id(stage_updated, stage_reference)

        query_update = NodeTaskModel.update(
            {
                "module": instance.module,
                "params": json.dumps(dict(instance.params.pairs)),
                "files": json.dumps(dict(instance.files.pairs)),
            }
        ).where(NodeTaskModel.id == object_id)

        query_update.execute()

    @staticmethod
    def get_by_id(object_id: int) -> NodeTask:
        """Returns pre-generated Plain-Python-Object NodeTask from the database.

        Args:
            object_id (int): Unique identifier, referencing to data-entry
                          inside the database.

        Returns:
            instance (NodeTask): Non-Empty Plain-Python-Object
                                       NodeTask instance.

        Raises:
            ValueError: If corresponding entry of `object_id` does not exist
                        in the database.
        """
        raise_if_invalid_object_id(object_id)
        if not NodeTaskSerializer.exists_by_id(object_id):
            raise ValueError("NodeTask database-entry was not found.")

        node_task_model_instance: NodeTaskModel = NodeTaskModel.get_by_id(object_id)
        related_amnes_object = AmnesObjectSerializer.get_by_id(
            node_task_model_instance.amnes_object
        )
        related_stage = AmnesObjectSerializer.get_by_id(node_task_model_instance.stage)
        experiment_stage = ExperimentStage(
            related_stage.slug,
            related_stage.name,
            related_stage.description,
            related_stage.labels,
        )
        node_task_params = NodeTaskParams(json.loads(node_task_model_instance.params))
        node_task_files = NodeTaskFiles(json.loads(node_task_model_instance.files))
        node_task_instance = NodeTask(
            related_amnes_object.slug,
            related_amnes_object.name,
            related_amnes_object.description,
            node_task_model_instance.module,
            experiment_stage,
            node_task_params,
            node_task_files,
        )
        node_task_instance.add_labels(related_amnes_object.labels)
        return node_task_instance
