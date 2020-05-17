"""This module contains the Model for the ParameterSet class.

Classes:
    ParameterSetModel: The Model for the equivalent ParameterSet class.
"""
from peewee import ForeignKeyField, TextField

from .amnes_object import AmnesObjectModel
from .amnes_project import AmnesProjectModel
from .base import BaseModel


class ParameterSetModel(BaseModel):
    """Model for equivalent ParameterSet class.

    Attributes:
        parameters (TextField): A list of parameters stored as the string of json.
        assignments (TextField): A dict of assignments stored as the string of json.
                                 Where the keys are the parameter and the value the
                                 explicit value of that parameter.
        amnes_project (ForeignKeyField): Reference to parent, AmnesProjectModel.
        amnes_object (ForeignKeyField): Reference to the AmnesObject for the
                                        ParameterSet class.
    """

    parameters = TextField()
    assignments = TextField()
    amnes_project = ForeignKeyField(
        AmnesProjectModel,
        on_delete="CASCADE",
        backref="parameter_sets",
        null=True,
        default=None,
    )
    amnes_object = ForeignKeyField(
        AmnesObjectModel, on_delete="CASCADE", backref="parameter_sets"
    )
