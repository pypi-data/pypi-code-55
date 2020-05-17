"""This module contains the Model for the Experiment module.

Classes:
    ExperimentModel: The Model is an abstraction model for
                     `ExperimentTemplateModel` and `ConcreteExperimentModel`.
"""
from peewee import ForeignKeyField, IntegerField, TextField

from amnes.data.models.amnes_object import AmnesObjectModel
from amnes.data.models.base import BaseModel


class ExperimentModel(BaseModel):
    """Model for the Experiment module.

    Attributes:
        states (TextField): Stores a stringified dict of ExperimentStates for
                            all repetitions.
        repetitions (IntegerField): Positive number of repetitions, this
                                    ConcreteExperiment should run.
        amnes_object (ForeignKeyField): A reference to the AmnesObject for the
                                        WorkerEndpoint class.
        nodes (peewee.ModelSelect): List of ExperimentNodes for this experiment.

    """

    states = TextField(null=True, default=None)
    repetitions = IntegerField(null=True, default=None)
    amnes_object = ForeignKeyField(
        AmnesObjectModel, on_delete="CASCADE", backref="experiments"
    )
