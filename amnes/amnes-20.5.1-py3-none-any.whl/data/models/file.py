"""This module contains the Model for files.

Classes:
    FileModel: This Model saves a reference of a File in the filesystem.
"""
from datetime import datetime

from peewee import CharField, DateTimeField, ForeignKeyField, IntegerField, TextField

from .amnes_object import AmnesObjectModel
from .base import BaseModel
from .experiment.experiment_concrete import ConcreteExperimentModel


class FileModel(BaseModel):
    """Model for persisting files in filesystem.

    Persists files through the DataManager/ FileSerializer to a predefined location.
    A file's content is not stored in the database. The DataManager/ FileSerializer
    stores the file at a static location in the filesystem and saves a reference to
    the path ìn the database.

    Attributes:
        file_type (CharField): Filetype of the given file. Filetype may be None.
        path (TextField): Absolute path of persisted file in filesystem.
        checksum_sha256 (CharField): Contains the sha256 hash of the data/ file.
        date_inserted (DateTimeField): Date and time when file was persisted.
        amnes_object (AmnesObjectModel): Contains a slug, name, description and labels.
        concrete_experiment (ForeignKeyField): Optional reference to a parent
                                               ConcreteExperiment.
        repetition (IntegerField): Optional repetition, referring to
                                   `concrete_experiment`
    """

    file_type = CharField(null=True)
    path = TextField()
    checksum_sha256 = CharField()
    date_inserted = DateTimeField(default=datetime.now)
    amnes_object = ForeignKeyField(
        AmnesObjectModel, on_delete="CASCADE", null=True, backref="files"
    )
    concrete_experiment = ForeignKeyField(
        ConcreteExperimentModel,
        on_delete="CASCADE",
        null=True,
        default=None,
        backref="stored_files",
    )
    repetition = IntegerField(null=True, default=None)
