"""This module contains the Model for the ExperimentTemplate class.

Classes:
    ExperimentTemplateModel: This Model persists data, equivalent to the
                             ExperimentTemplate class.
"""
from peewee import ManyToManyField

from ..amnes_object import AmnesObjectModel
from .base import ExperimentModel


class ExperimentTemplateModel(ExperimentModel):
    """Model for the ExperimentTemplate class.

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
    """

    stages = ManyToManyField(
        AmnesObjectModel, on_delete="CASCADE", backref="template_experiments"
    )


EXPERIMENTTEMPLATEMODEL_AMNESOBJECTMODEL_THROUGH = (
    ExperimentTemplateModel.stages.get_through_model()
)
