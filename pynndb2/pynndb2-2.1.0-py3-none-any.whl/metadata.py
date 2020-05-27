#####################################################################################
#
#  Copyright (c) 2020 - Mad Penguin Consulting Ltd
#
#####################################################################################
from __future__ import annotations
from typing import TYPE_CHECKING, Tuple, Generator
from lmdb import Transaction as TXN
from ujson import loads, dumps
from .doc import Doc
from .decorators import wrap_writer, wrap_reader_yield

if TYPE_CHECKING:
    from .database import Database  # pragma: no cover


class MetaData:
    """
    This is a wrapper for the __metadata__ table, for which there should be
    'one' per database. This contains additional information including index
    definitions and other persistent information pertaining to tables or
    indeed to the database itself. This can also be used to store user defined
    information, however be careful to avoid key namespace overlaps. Currently
    we are using keys of the form;

    o _(table_name)_(index_name)_  to store information about indexes
    o _(table_name)@config         to store table specific conguration
    o _(table_name)!zstd_cdict     to store the zstd training dictionary
    """

    def __init__(self, database: Database):
        """
        The MetaData class is initialised with a database reference so it can get access
        to the current working environment and metadata table.

        database - the database that holds the metadata table we'll be working with
        """
        self._table = None
        self._database = database
        self.env = database.env

    def open(self):
        """
        Open the __metadata__ table and make it available for IO
        """
        if self._table:
            return self  # pragma: no cover

        self._table = self._database.table('__metadata__')
        return self

    def fetch_index(self, table_name: str, index_name: str, txn: TXN=None) -> Doc:
        """
        Fetch the index definition for the index in the named table. This is an internal
        routine primarily used when opening a table to recover the names of the indexes
        associated with that table.

        table_name - name of the table the index is associated with
        index_name - the name of the index to recover information on
        txn - a read or write transaction to wrap the operation

        Returns a Doc object containing a 'conf' key
        """
        return Doc(loads(txn.get(self.path_index(table_name, index_name), db=self._table._db)))

    def store_index(self, table_name: str, index_name: str, value: Doc, txn: TXN=None) -> None:
        """
        Store the index definition for the index in the named table. This is an internal
        routine primarily used when creating an index store index and names and definitions
        for the index being created.

        table_name - name of the table the index is associated with
        index_name - the name of the index
        txn - a write transaction to wrap the operation
        """
        txn.put(self.path_index(table_name, index_name), dumps(value.doc).encode(), db=self._table._db)

    def remove_index(self, table_name: str, index_name: str, txn: TXN=None) -> None:
        """
        Remove an index definition, used either when a table or an index is dropped

        table_name - name of the table the index is associated with
        index_name - the name of the index
        txn - a write transaction to wrap the operation
        """
        txn.delete(self.path_index(table_name, index_name), db=self._table._db)

    def path_index(self, table_name: str, index_name: str) -> bytes:
        """
        Build a key for the __metadata__ table to access an index definition

        table_name - name of the table the index is associated with
        index_name - the name of the index

        Returns the assembled key in bytes format ready to be used by get/put
        """
        return f'_{table_name}_{index_name}'.encode()

    def fetch_config(self, table_name: str, txn: TXN=None) -> Doc:
        """
        Fetch the configuration dictionary from the metadata table for the named table. This
        dictionary will contain table specific settings such as the compression mechanism
        currently being employed on the table.

        table_name - the name of the table we want the configuration for
        txn - a transaction to wrap the operation
        """
        raw = txn.get(self.path_config(table_name), db=self._table._db)
        return Doc(loads(raw) if raw else {})

    def store_config(self, table_name: str, value: Doc, txn: TXN=None) -> None:
        """
        Store the configuration dictionary back in the metadata table for the named table.
        Typically this is handled internally for example when compression is enabled on
        the table.

        table_name - the name of the table we're storing the configuration for
        txn - a transaction to wrap the operation
        """
        txn.put(self.path_config(table_name), dumps(value.doc).encode(), db=self._table._db)

    def path_config(self, table_name: str) -> bytes:
        """
        This is used to generate a key for methods that operate on configuration metadata. On
        being passed a table name, this routine returns the key associated with the config
        item in the metadata table for the named table.

        table_name - the name of the table we need to generate a key for
        """
        return f'_{table_name}@config'.encode()

    def fetch_tag(self, table_name: str, tag: str, txn: TXN=None) -> Doc:
        """
        Recover a tag from the metadata table for a given table and tag name. It works against
        binary blobs as opposed to formatted JSON so is suited to 1storing things like
        compression dictionaries. (which was initially why it was added)

        table_name - the name of the table we're fetching tags for
        tag - the name of the specific tag we want
        txn - a transaction to wrap the operation
        """
        return txn.get(self.path_tag(table_name, tag), db=self._table._db)

    def store_tag(self, table_name: str, tag: str, value: Doc, txn: TXN=None) -> None:
        """
        Store a tag in the metadata table for a given table and tag name. This was initially
        added to facilitate the storage of compression dict's (as binary blobs).

        table_name - the name of the table we're fetching tags for
        tag - the name of the specific tag we want
        txn - a transaction to wrap the operation
        """
        txn.put(self.path_tag(table_name, tag), value, db=self._table._db)

    def path_tag(self, table_name: str, tag: str) -> bytes:
        """
        Return the primary key for a given tag in the metadata table. Tags are based on
        or relative to a table name and a tag name.

        table_name - the name of the table we're fetching tags for
        tag - the name of the specific tag we want
        """
        return f'_{table_name}!{tag}'.encode()

    @wrap_writer
    def remove(self, name: str, txn: TXN=None) -> None:
        """
        Remove all keys from the database for the current table. This is used by
        'droptable' to clean any latent meta data from the metadata table when
        a table is dropped.

        name - name of the table to remove keys from
        txn - a write transaction to wrap the operation
        """
        keys = []
        match = [f'_{name}_', f'_{name}@', f'_{name}!']
        with txn.cursor(db=self._table._db) as cursor:
            while cursor.next():
                key = cursor.key().decode()
                for m in match:
                    if key.startswith(m):
                        keys.append(key.encode())
            for key in keys:
                txn.delete(key, db=self._table._db)

    @wrap_reader_yield
    def fetch(self, name: str, txn: TXN=None) -> Generator[Tuple[str, bytes], None, None]:
        """
        Fetch all the keys (and values) from the metadata table that match the name
        of the table supplied.

        name - name of the table to recover keys from
        txn - a read or write transaction to wrap the operation
        """
        match = [f'_{name}_', f'_{name}@', f'_{name}!']
        with txn.cursor(db=self._table._db) as cursor:
            while cursor.next():
                key = cursor.key().decode()
                for m in match:
                    if key.startswith(m):
                        yield (key, cursor.value())
