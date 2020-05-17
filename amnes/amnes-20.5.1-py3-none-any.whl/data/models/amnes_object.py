"""This module contains the Model for the AmnesObject class.

Classes:
    AmnesObjectModel: The Model for the equivalent AmnesObject class.
"""

from peewee import CharField, ForeignKeyField

from .base import AnnotationModel, BaseModel


class AmnesObjectModel(BaseModel):
    """Model for equivalent AmnesObject class.

    Persists the data of an AmnesObject instance in core.amnes_object into a database,
    defined and initialized by the DataManager.

    Attributes:
        slug (CharField): Short identifier for the AMNES object,
                          which must be a valid, non-empty string.
        name (CharField): Full name for the AMNES object.
        annotation (int): Reference to an AnnotationModel entry.
    """

    slug = CharField()
    name = CharField()
    annotation = ForeignKeyField(
        AnnotationModel, on_delete="CASCADE", backref="amnes_objects"
    )
