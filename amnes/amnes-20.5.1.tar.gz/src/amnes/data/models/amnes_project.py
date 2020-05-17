"""This module contains the Model for the AmnesProject class.

Classes:
    AmnesProjectModel: The Model persists an instance of AmnesProject.
"""
from peewee import ForeignKeyField, IntegerField

from .amnes_object import AmnesObjectModel
from .base import BaseModel
from .experiment.experiment_template import ExperimentTemplateModel


class AmnesProjectModel(BaseModel):
    """Model for the AmnesProject class.

    Attributes:
        template (ForeignKeyField): ExperimentModel instance defined for this
                                    AmnesProject.
        repetitions (IntegerField): Number of repetitions for a concrete experiment.
        parameter_sets (peewee.ModelSelect): List of ParameterSet instances defined for
                                             this AmnesProject.
        experiment_sequences (peewee.ModelSelect): List of ExperimentSequence instances
                                                   defined for this AmnesProject.
        amnes_object (ForeignKeyField): A reference to the AmnesObject for the
                                        AmnesProject class.
    """

    template = ForeignKeyField(
        ExperimentTemplateModel, on_delete="CASCADE", backref="amnes_projects"
    )
    repetitions = IntegerField()
    amnes_object = ForeignKeyField(
        AmnesObjectModel, on_delete="CASCADE", backref="amnes_projects"
    )
