#####################################################################################
#
#  Copyright (c) 2020 - Mad Penguin Consulting Ltd
#
#####################################################################################

__version__ = '2.1.0'

from .manager import Manager
from .database import Database
from .table import Table, FilterResult
from .index import Index
from .doc import Doc
from .compression import CompressionType
from .objectid import ObjectId
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
    ObjectId,
    FilterResult,
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
