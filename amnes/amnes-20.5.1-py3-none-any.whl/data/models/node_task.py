"""This module contains the Model for the NodeTask class.

Classes:
    NodeTaskModel: The Model for the equivalent NodeTask class.
"""
from peewee import CharField, Check, ForeignKeyField, TextField

from .amnes_object import AmnesObjectModel
from .base import BaseModel
from .experiment_node import ConcreteExperimentNodeModel, ExperimentNodeTemplateModel


class NodeTaskModel(BaseModel):
    """Model for equivalent NodeTask class.

    Attributes:
        experiment_node (ForeignKeyField): Parent ExperimentNodeModel
        module (CharField): Path of the module used as base for the Node Task.
        stage (CharField): Stage in which the Node Task should be executed.
        params (TextField): Configuration parameters for the Node Task.
        files (TextField): Configuration files for the Node Task.
        amnes_object (ForeignKeyField): A reference to the AmnesObject for the
                                        WorkerEndpoint class.
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta class for constraints."""

        constraints = [
            Check(
                "(experiment_template_node_id IS NULL AND "
                "concrete_experiment_node_id IS NOT NULL) OR "
                "(experiment_template_node_id IS NOT NULL AND "
                "concrete_experiment_node_id IS NULL)"
            )
        ]

    experiment_template_node = ForeignKeyField(
        ExperimentNodeTemplateModel, on_delete="CASCADE", backref="tasks", null=True
    )
    concrete_experiment_node = ForeignKeyField(
        ConcreteExperimentNodeModel, on_delete="CASCADE", backref="tasks", null=True
    )
    module = CharField()
    stage = ForeignKeyField(AmnesObjectModel, on_delete="CASCADE", backref="node_tasks")
    params = TextField()
    files = TextField()
    amnes_object = ForeignKeyField(
        AmnesObjectModel, on_delete="CASCADE", backref="node_tasks"
    )
