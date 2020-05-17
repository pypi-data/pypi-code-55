"""This module contains all base models for a Data-Model.

Classes:
    BaseModel: The base of all models, from which all concrete model classes inherit.
    AnnotationModel: This Model consists of a description and labels, to make
                      a DataModel more descriptiv.
    LabelModel: This Model contains labels for tagging and adding context to data.
"""
from peewee import CharField, DatabaseProxy, ManyToManyField, Model, TextField

DATABASE_PROXY = DatabaseProxy()


# pylint: disable=too-few-public-methods
class BaseModel(Model):
    """Abstract BaseModel, from which all concrete model classes inherit.

    Attributes:
        database (DatabaseProxy): Defines database and is set by
                                  DataManager
    """

    # pylint: disable=missing-class-docstring
    class Meta:  # noqa: D106
        database = DATABASE_PROXY


class LabelModel(BaseModel):
    """Model for labels.

    This Model describes a label. It is intended to be used mostly by the
    AnnotationLabelModel.

    Attributes:
        name (CharField): Name of the label.
        annotations (ModelSelect): References to the related annotations.
    """

    name = CharField(unique=True)


class AnnotationModel(BaseModel):
    """Model for annotations with a description and a list of labels.

    This Model is mostly used as a base by other Models, with the need of
    a description and labels. It can be used as a reference by other Models with
    the ForeignKeyField.
    One AnnotationModel object has one description and n LabelModel-references.

    Attributes:
        description (TextField): Custom description.
        labels (ModelSelect): References to the related labels.
    """

    description = TextField()
    labels = ManyToManyField(LabelModel, on_delete="CASCADE", backref="annotations")


ANNOTATIONMODEL_LABELMODEL_THROUGH = AnnotationModel.labels.get_through_model()
