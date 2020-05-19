#####################################################################################
#
#  Copyright (c) 2020 - Mad Penguin Consulting Ltd
#
#####################################################################################

__version__ = '2.0.8'

from .manager import Manager
from .database import Database
from .table import Table
from .index import Index
from .doc import Doc
from .compression import CompressionType
from .exceptions import IndexAlreadyExists, FailedToWriteMetadata, DocumentAlreadyExists, FailedToWriteData, \
    DocumentDoesntExist, InvalidKeySpecifier, NoSuchIndex, NotDuplicateIndex, NoSuchTable, \
    DuplicateKey, IndexWriteError, TableNotOpen, TrainingDataExists


__all__ = [
    Manager,
    Database,
    Table,
    Index,
    Doc,
    CompressionType,
    IndexAlreadyExists,
    FailedToWriteMetadata,
    DocumentAlreadyExists,
    FailedToWriteData,
    DocumentDoesntExist,
    InvalidKeySpecifier,
    NoSuchIndex,
    NotDuplicateIndex,
    NoSuchTable,
    DuplicateKey,
    IndexWriteError,
    TableNotOpen,
    TrainingDataExists
]
