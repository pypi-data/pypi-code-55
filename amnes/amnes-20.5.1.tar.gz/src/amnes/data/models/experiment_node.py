"""This module contains the Model for the ExperimentNode module.

Classes:
    ExperimentNodeModel: The Model represents the ExperimentNodeTemplate and
                         ConcreteExperimentNode classes and distinguishes by the
                         boolean `is_template`.
"""
from peewee import ForeignKeyField

from .amnes_object import AmnesObjectModel
from .base import BaseModel
from .experiment.experiment_concrete import ConcreteExperimentModel
from .experiment.experiment_template import ExperimentTemplateModel
from .worker_endpoint import WorkerEndpointModel


class ExperimentNodeModel(BaseModel):
    """Model for the ExperimentNode module.

    Attributes:
        endpoint (WorkerEndpointModel): Management communication endpoint of
                                        the worker.
        amnes_object (ForeignKeyField): A reference to the AmnesObject for the
                                        WorkerEndpoint class.
    """

    endpoint = ForeignKeyField(
        WorkerEndpointModel, on_delete="CASCADE", backref="experiment_nodes"
    )
    amnes_object = ForeignKeyField(
        AmnesObjectModel, on_delete="CASCADE", backref="experiment_nodes"
    )


class ExperimentNodeTemplateModel(ExperimentNodeModel):
    """Model for ExperimentNodeTemplate.

    Attributes:
        experiment (ForeignKeyField): Parent Experiment
        endpoint (WorkerEndpointModel): Management communication endpoint of
                                        the worker.
        tasks (peewee.ModelSelect): List of NodeTasks references that an experiment
                                    node should execute during an experiment.
        amnes_object (ForeignKeyField): A reference to the AmnesObject for the
                                        WorkerEndpoint class.
    """

    experiment = ForeignKeyField(
        ExperimentTemplateModel,
        on_delete="CASCADE",
        backref="nodes",
        null=True,
        default=None,
    )


class ConcreteExperimentNodeModel(ExperimentNodeModel):
    """Model for ConcreteExperimentNode.

    Attributes:
        experiment (ForeignKeyField): Parent Experiment
        endpoint (WorkerEndpointModel): Management communication endpoint of
                                        the worker.
        tasks (peewee.ModelSelect): List of NodeTasks references that an experiment
                                    node should execute during an experiment.
        amnes_object (ForeignKeyField): A reference to the AmnesObject for the
                                        WorkerEndpoint class.
    """

    experiment = ForeignKeyField(
        ConcreteExperimentModel,
        on_delete="CASCADE",
        backref="nodes",
        null=True,
        default=None,
    )
