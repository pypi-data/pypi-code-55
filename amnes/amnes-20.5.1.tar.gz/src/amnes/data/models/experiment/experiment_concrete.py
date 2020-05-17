"""This module contains the Model for the ConcreteExperiment class.

Classes:
    ConcreteExperimentModel: This Model persists data, equivalent to the
                             ConcreteExperiment class.
"""
from peewee import ForeignKeyField, ManyToManyField

from ..amnes_object import AmnesObjectModel
from ..experiment_sequence import ExperimentSequenceModel
from .base import ExperimentModel


class ConcreteExperimentModel(ExperimentModel):
    """Model for the ConcreteExperimentModel class.

    Attributes:
        states (TextField): Stores a stringified dict of ExperimentStates for
                            all repetitions.
        repetitions (IntegerField): Positive number of repetitions, this
                                    ConcreteExperiment should run.
        amnes_object (ForeignKeyField): A reference to the AmnesObject for the
                                        WorkerEndpoint class.
        nodes (peewee.ModelSelect): List of ExperimentNodes for this experiment.
        stages (ManyToManyField): All ExperimentStage instances defined for
                                  this experiment.
        experiment_sequence (ForeignKeyField): Parent ExperimentSequence
        stored_files (peewee.ModelSelet): List of files, stored by FileSerializer.
    """

    stages = ManyToManyField(
        AmnesObjectModel, on_delete="CASCADE", backref="concrete_experiments"
    )
    experiment_sequence = ForeignKeyField(
        ExperimentSequenceModel, on_delete="CASCADE", backref="experiments", null=True
    )


CONCRETEEXPERIMENTMODEL_AMNESOBJECTMODEL_THROUGH = (
    ConcreteExperimentModel.stages.get_through_model()
)
