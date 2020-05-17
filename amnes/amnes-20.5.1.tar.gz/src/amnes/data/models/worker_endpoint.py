"""This module contains the Model for the WorkerEndpoint class.

Classes:
    WorkerEndpointModel: The Model for the equivalent WorkerEndpoint class.
"""
from peewee import ForeignKeyField, IntegerField, TextField

from .amnes_object import AmnesObjectModel
from .base import BaseModel


class WorkerEndpointModel(BaseModel):
    """Model for equivalent WorkerEndpoint class.

    Attributes:
        address (TextField): Valid IPv4 or IPv6 address to be used for management
                             communication.
        port (IntegerField): Valid port number to be used for management communication.
        amnes_object (ForeignKeyField): A reference to the AmnesObject for the
                                        WorkerEndpoint class.
    """

    address = TextField()
    port = IntegerField()
    amnes_object = ForeignKeyField(
        AmnesObjectModel, on_delete="CASCADE", backref="worker_endpoints"
    )
