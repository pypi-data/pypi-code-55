"""This module contains the Model for the ExperimentSequence class.

Classes:
    ExperimentSequenceModel: The Model persists an instance of ExperimentSequence.
"""
from peewee import ForeignKeyField

from .amnes_project import AmnesProjectModel
from .base import BaseModel
from .parameter_set import ParameterSetModel


class ExperimentSequenceModel(BaseModel):
    """Model for the ExperimentSequence module.

    Attributes:
        parameter_set (ForeignKeyField): Corresponding ParameterSet instance.
        amnes_project (ForeignKeyField): Parent AmnesProjectModel
        experiments (peewee.ModelSelect): List of ConcreteExperiment instances.
    """

    parameter_set = ForeignKeyField(
        ParameterSetModel, on_delete="CASCADE", backref="experiment_sequences"
    )
    amnes_project = ForeignKeyField(
        AmnesProjectModel,
        on_delete="CASCADE",
        backref="experiment_sequences",
        null=True,
    )
