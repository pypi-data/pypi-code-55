#####################################################################################
#
#  Copyright (c) 2020 - Mad Penguin Consulting Ltd
#
#####################################################################################
from __future__ import annotations
from sys import maxsize as MAXSIZE
from collections import UserDict
from typing import Generator, Optional, TYPE_CHECKING, List, Union, Callable
from lmdb import Transaction as TXN
from .index import Index
from .doc import Doc
from .compression import Compression, CompressionType
from .cursor import Cursor
from .filterresult import FilterResult
from .decorators import wrap_writer, wrap_reader, wrap_reader_yield
from .exceptions import IndexAlreadyExists, \
    DocumentDoesntExist, InvalidKeySpecifier, NoSuchIndex
from .types_ import Config, OID, OIDS

if TYPE_CHECKING:
    from .database import Database  # pragma: no cover


class Table(UserDict, Compression):
    """
    The Table class is used to wrap access to individual database tables and
    incorporates semi-transparent compression / decompression on a per table
    basis. Compression libraries are pluggable and implemented in the
    Compression class.

    o APPEND_MODE - when appending a record we know that the new key will be the
                    highest value in the table so we can take advantage of LMDB's
                    "append" mode. If you never want to use this option, set
                    pynndb2.Table.APPEND_MODE to False.

                    NOTE: compatibility issue, we've switched to our own version
                    of "ObjectId", if you set this to True and have data that
                    uses both BSON/ObjectId and the new ObjectId, you will have
                    a problem. (data loss)
    """
    APPEND_MODE = False

    def __init__(self, database: Database, name: str) -> None:
        """
        Intantiate a table instance bases on the name of the table required. A
        reference to the containing database is also required so the table
        can back-reference the database environment.

        database - a reference to the containing database object
        name - the name of the table to reference
        """
        self.name = name
        self.env = database.env
        self._database = database
        self._db = None
        self._meta = database.meta
        UserDict.__init__(self)
        Compression.__init__(self)

    def __setitem__(self, name: str, conf: Config) -> None:
        """
        Create an entry for an index with the specified name

        name - the name of the index to create
        conf - configuration options for the index we're creating
        """
        if name in self.data:
            raise IndexAlreadyExists(name)
        self.data[name] = Index(self, name, conf)

    def __repr__(self) -> str:
        """
        Generate a string representation of this object, by default we include the
        table name and the table status, i.e. whether it is open or not.
        """
        return f'<{__name__}.Table instance> name="{self.name}" status={"open" if self.isopen else "closed"}'

    @property
    def isopen(self) -> bool:
        """
        Return True if this table is open
        """
        return True if self._db else False

    @wrap_reader
    def records(self, txn: Optional[TXN]=None) -> int:
        """
        Return the number of records in this table

        txn - an transaction to wrap the operation
        """
        return txn.stat(self._db).get('entries', 0)

    @property
    def read_transaction(self) -> TXN:
        """
        Use with "with" to begin a Read-Only transaction
        """
        return self.env.begin()

    @property
    def write_transaction(self) -> TXN:
        """
        Use with "with" to begin a Read-Write transaction
        """
        return self.env.begin(write=True)

    @wrap_reader
    def storage_used(self, txn: Optional[TXN]=None) -> int:
        """
        Return the amount of storage space used by data contained within this table

        txn - optional transaction to wrap this operation
        """
        stat = txn.stat(self._db)
        return stat['psize'] * (stat['leaf_pages'] + stat['branch_pages'] + stat['overflow_pages'] + 2)

    @wrap_writer
    def open(
            self,
            compression_type: Optional[CompressionType]=None,
            compression_level: Optional[int]=None,
            txn: Optional[TXN]=None) -> Table:
        """
        Open this table and make it available for use, if the compression type is set to
        anything other than NONE, the following the call the table will be set to read and
        write data using the selected compression mechanism, and any data in the table will
        be compressed.

        compression_type - the type of compression to use
        compression_level - the compression level to set
        txn - an optional transaction to wrap this request
        """
        if self.isopen:
            return self
        self._db = self.env.open_db(self.name.encode(), txn=txn)
        if not self._meta:
            return self
        for index_name in self.indexes(txn=txn):
            doc = self._meta.fetch_index(self.name, index_name, txn=txn)
            self.__setitem__(index_name, doc['conf'])
            self.data[index_name].open(txn=txn)

        if compression_type and compression_type != CompressionType.NONE:
            do_compress = self.compression_select(compression_type, compression_level, txn=txn)
            Compression.open(self, txn=txn)
            if do_compress and self.records(txn=txn):
                self.compress_existing_data(txn=txn)
        else:
            Compression.open(self, txn=txn)
        return self

    def close(self) -> None:
        """
        Close a table by essentially losing all references to it
        """
        self._db = None
        self.data.clear()
        Compression.close(self)

    @wrap_writer
    def droptable(self, txn: Optional[TXN]=None) -> None:
        """
        Drop the current table, this will empty the table, remove all the indexes,
        remote the table itself, and remove all associated metadat.

        txn - a write transaction to wrap this operation
        """
        for index_name in self.data:
            self.data[index_name].drop(txn=txn)
        txn.drop(self._db, True)
        self._meta.remove(self.name, txn=txn)

    @wrap_reader_yield
    def indexes(self, txn: Optional[TXN]=None) -> List[str]:
        """
        Generate a list if indexs (names) available for this table

        txn - an optional transaction
        """
        index_key = Index.index_path(self.name, '')
        offset = len(index_key)
        with txn.cursor(db=self._database._db) as cursor:
            if cursor.set_range(index_key.encode()):
                while True:
                    name = cursor.key().decode()
                    if not name.startswith(index_key) or not cursor.next():
                        break
                    yield name[offset:]

    @wrap_writer
    def ensure(
            self,
            index_name: str,
            func: str,
            duplicates: bool=False,
            force: bool=False,
            txn: Optional[TXN]=None) -> Index:
        """
        Ensure that the specified index exists, if it does by default do nothing. If the
        index does not exist, or if the 'force' flag is true, the index will be (re)created
        using the new index function.

        index_name - the name of the required index
        func - a description of how index keys should be generated
        duplicates - whether this is a duplicate index or not
        force - whether to re-index the index if it already exists
        txn - an optional transaction

        The "func" parameter can take one of two forms, it can either be a Python format
        string (the only option in v1) or it can be a complete python function if prefixed
        with a 'def'. So for example as a format string;
        ```
        func = '{name}'         # index by name
        func = '{name}|{age}'   # index by name + age
        func = '{age:03d}'      # index by age with leading zero for correct numerical sort order
        ```
        Or if you want to use a function which allows for more flexibility;
        ```
        func = 'def func(doc): return "{:03d}".format(doc["age"]).encode()'
        ```
        For a complete working example, the natural order is in descending on age,
        but when iterating using either of the example indexes, you should see the order
        as ascending order of age.
        ```
        #!/usr/bin/env python
        from pynndb import Manager, Doc
        from shutil import rmtree
        rmtree('.database')
        db = Manager().database('database', '.database')
        people = db.table('people')
        people.append(Doc({'name': 'Tom', 'age': 21}))
        people.append(Doc({'name': 'Harry', 'age': 19}))
        people.ensure('by_age_fs', '{age:03d}')
        people.ensure('by_age_func', 'def func(doc): return "{:03d}".format(doc["age"]).encode()')
        [print(person.doc) for person in people.find()]
        print('--')
        [print(person.doc) for person in people.find('by_age_fs')]
        print('--')
        [print(person.doc) for person in people.find('by_age_func')]
        ```
        """
        if force and index_name in self.data:
            self.drop(index_name, txn=txn)
        if index_name in self.data:
            return self.data[index_name]
        index_path = Index.index_path(self.name, index_name)
        conf = {
            'key': index_path,
            'dupsort': duplicates,
            'create': True,
            'func': func
        }
        self.__setitem__(index_name, conf)
        self.data[index_name].open(txn=txn)
        self._meta.store_index(self.name, index_name, Doc({'conf': conf}), txn=txn)
        self.reindex(index_name, txn=txn)
        return self.data[index_name]

    @wrap_writer
    def reindex(self, index_name: str, txn: Optional[TXN]=None) -> None:
        """
        Reindex the named index, assuming the index exists. The index is first emptied
        and then each record is reindexed, for a large table this can take some time
        and will lock the database while in progress.

        index_name - the name of the index to reindex
        txn - a write transaction to wrap the operation
        """
        if index_name not in self.data:
            raise NoSuchIndex
        self.data[index_name].empty(txn=txn)
        with txn.cursor(self._db) as cursor:
            while cursor.next():
                self.data[index_name].put_cursor(cursor, txn=txn)

    @wrap_writer
    def append(self, doc: Doc, txn: Optional[TXN]=None) -> Doc:
        """
        Append a new record to this table

        doc - the data to append
        txn - an optional transaction object
        """
        doc.put(self, append=False if doc.oid else self.APPEND_MODE, txn=txn)
        for index_name in self.data:
            self.data[index_name].put(doc, txn=txn)
        return doc

    @wrap_writer
    def save(self, doc: Doc, txn: Optional[TXN]=None) -> None:
        """
        Update the current record in the table

        doc - the record to update
        txn - an optional transaction
        """
        if not doc.oid:
            raise DocumentDoesntExist
        old_doc = Doc(None, doc.oid).get(self, txn=txn)
        doc.put(self, append=False, txn=txn)
        for index_name in self.data:
            self.data[index_name].save(old_doc, doc, txn=txn)

    @wrap_reader_yield
    def find(
            self,
            index_name: str=None,
            expression: str=None,
            limit: int = MAXSIZE,
            txn: Optional[TXN]=None) -> Generator[Doc, None, None]:
        """
        Find records in this table either in natural (date) order, or in index order

        index_name - an optional index name for ordering
        expression - the expression to filter the sort on
        limit - the maximum number of records to return
        txn - an optional transaction
        """
        if index_name:
            if index_name not in self.data:
                raise NoSuchIndex(index_name)
            db = self.data[index_name]._db
        else:
            db = self._db
        #
        with txn.cursor(db) as cursor:
            count = 0
            while count < limit and cursor.next():
                count += 1
                record = cursor.value()
                if index_name:
                    key = record
                    record = txn.get(record, db=self._db)
                else:
                    key = cursor.key()

                record = self._decompressor(record)
                if callable(expression) and not expression(record):
                    continue
                yield Doc(record, key)

    @wrap_reader
    def get(self, oid: [bytes, str], txn: Optional[TXN]=None) -> Doc:
        """
        Recover a single record from the database based on it's primary key

        oid - primary key of record to recover
        txn - an optional active transaction
        """
        return Doc(None, oid).get(self, txn=txn)

    @wrap_writer
    def delete(self, keyspec: Union[OID, OIDS, Doc], txn: Optional[TXN]=None) -> None:
        """
        Delete one or more records from the database based on a key specification that
        should reference one or more records by primary key.

        keyspec - we accept either a key, a list of keys or a Doc, keys may be str or bytes
        txn - an optional transaction
        """
        if isinstance(keyspec, str):
            keys = [keyspec]
        elif isinstance(keyspec, list):
            keys = keyspec
        elif isinstance(keyspec, Doc):
            keys = [keyspec.oid]
        elif isinstance(keyspec, bytes):
            keys = [keyspec]
        else:
            raise InvalidKeySpecifier(keyspec)

        for key in keys:
            if isinstance(key, str):
                key = key.encode()
            doc = self.get(key, txn=txn)
            doc.delete(self, txn=txn)
            for index_name in self.data:
                self.data[index_name].delete(doc, txn=txn)

    @wrap_writer
    def empty(self, txn: Optional[TXN]=None) -> None:
        """
        Remove all data from the current table leaving the indexing structure in-tact

        txn - an optional transaction
        """
        for index_name in self.data:
            self.data[index_name].empty(txn)
        txn.drop(self._db, False)

    @wrap_writer
    def drop(self, index_name: str, txn: Optional[TXN]=None) -> None:
        """
        Drop an index from the current table

        index_name - the name of the index to drop
        txn - an optional transaction
        """
        if index_name not in self.data:
            raise NoSuchIndex(index_name)
        self.data[index_name].drop(txn=txn)
        self._meta.remove_index(self.name, index_name, txn=txn)
        del self.data[index_name]

    @wrap_reader_yield
    def tail(self, key: Optional[OID]=None, txn: Optional[TXN]=None) -> Generator[Doc, None, None]:
        """
        Generates a sequence of records starting from the key after the primary key supplied. If no
        key is supplied, all records are returned, if a misssing key is supplied, no records are
        returned. Typically use this against the last-seen key to access new keys since the last
        check.

        key - the key to start from
        txn - an optional transaction

        TODO: add index to allow tailing based on indexes
        """
        with txn.cursor(db=self._db) as cursor:
            if key:
                if not isinstance(key, bytes):
                    key = key.encode()
                #
                #   We need this behaviour, when someone empties the table, tail needs to know
                #   to go back to the start of the table and continue, rather then being left
                #   on a non-existant key forever ...
                #
                if not cursor.get(key):
                    if not cursor.first():
                        return None
                elif not cursor.next():
                    return None

            for key, val in cursor.iternext(keys=True, values=True):
                yield Doc(self._decompressor(val), key)

    @wrap_reader
    def first(self, index_name: Optional[str]=None, txn: Optional[TXN]=None) -> Optional[Doc]:
        """
        Return the first record in the table or None if there are no records

        index_name - the name of the index to use (defaults to primary)
        txn - an optional transaction
        """
        if index_name:
            if index_name not in self.data:
                raise NoSuchIndex(index_name)
            db = self.data[index_name]._db
        else:
            db = self._db
        with txn.cursor(db=db) as cursor:
            if not cursor.first():
                return None
            if index_name:
                doc = txn.get(cursor.value(), db=self._db)
                return Doc(self._decompressor(doc), cursor.value())
            else:
                return Doc(self._decompressor(cursor.value()), cursor.key())

    @wrap_reader
    def last(self, index_name: Optional[str]=None, txn: Optional[TXN]=None) -> Optional[Doc]:
        """
        Return the last record in the table or None if there are no records

        index_name - the name of the index to use (defaults to primary)
        txn - an optional transaction
        """
        if index_name:
            if index_name not in self.data:
                raise NoSuchIndex(index_name)
            db = self.data[index_name]._db
        else:
            db = self._db
        with txn.cursor(db=db) as cursor:
            if not cursor.last():
                return None
            if index_name:
                doc = txn.get(cursor.value(), db=self._db)
                return Doc(self._decompressor(doc), cursor.value())
            else:
                return Doc(self._decompressor(cursor.value()), cursor.key())

    @wrap_reader_yield
    def range(
            self,
            index_name: Optional[str]=None,
            lower: Optional[Doc]=None,
            upper: Optional[Doc]=None,
            keyonly: bool=False,
            inclusive: bool=True,
            limit: int=MAXSIZE,
            page_number: int=0,
            nodups: bool=False,
            txn: Optional[TXN]=None) -> Generator[Doc, None, None]:
        """
        Find all records within a range of keys, optionally including keys at each end
        and optionally returning just the keys rather than the entire record.

        index_name - an optional index name, if no index is supplied, use primary keys
        lower - the record at the lower end of the range
        upper - the record at the upper end of the range
        keyonly - if set to True, only returns keys rather than the entire records
        inclusive - if set to True, include the keys at each end, i.e. use <=|=> rather than <|>
        limit - maximum number of records to return
        page_number - index of the page (starts from 0) with a size `limit` to return results from
        nodups - no duplicate keys, return only unique key values and ignore duplicates
        txn - an optional transaction
        """
        if index_name:
            if index_name not in self.data:
                raise NoSuchIndex
            index = self.data[index_name]
            db = index._db

            lower_keys = index.map_key(lower) if lower else [None]
            upper_keys = index.map_key(upper) if upper else [None]

            if not isinstance(lower_keys, list):
                lower_keys = [lower_keys]
            if not isinstance(upper_keys, list):
                upper_keys = [upper_keys]

        else:
            db = self._db
            lower_keys = [lower.oid] if lower else [None]
            upper_keys = [upper.oid] if upper else [None]

        skip = page_number * limit

        with txn.cursor(db) as cursor:
            for lower_key in lower_keys:
                upper_key = upper_keys.pop(0)
                next_record = cursor.next_nodup if nodups else cursor.next
                cursor.set_range(lower_key) if lower_key else cursor.first()
                if cursor.key() == lower_key and not inclusive:
                    next_record()
                count = 0
                while cursor.key() and count < limit:
                    if upper_key and (cursor.key() > upper_key or (cursor.key() == upper_key and not inclusive)):
                        break
                    if skip:
                        skip -= 1
                    else:
                        count += 1
                        if not index_name:
                            yield cursor.key().decode() if keyonly else Doc(
                                self._decompressor(cursor.value()), cursor.key())
                        else:
                            yield Cursor(index, cursor) if keyonly else Doc(
                                None, cursor.value()).get(self, txn=txn)
                    next_record()

    @wrap_reader
    def seek_one(self, index_name: str, doc: Doc, txn: Optional[TXN]=None) -> Doc:
        """
        Find the first matching record from an index

        index_name - the name of the index to search
        doc - the template record to find
        txn - an optional transaction
        """
        if index_name not in self.data:
            raise NoSuchIndex
        index_entry = self.data[index_name].get(doc, txn=txn)
        return Doc(None, index_entry).get(self, txn=txn) if index_entry else None

    def seek(
            self,
            index_name: str,
            doc: Doc,
            limit: int=MAXSIZE,
            page_number: int=0,
            keyonly: bool = False,
            txn: Optional[TXN]=None) -> Generator[Doc, None, None]:
        """
        Return a selection of records from the selected table matching the template record provided in "doc".
        Should return a maximum of 1 record for unique indexes.
        index_name - the name of the index to search
        doc - the template record to find
        limit - the maximum number of results to return
        page_number - index of the page (starts from 0) with a size `limit` to return results from
        keyonly - return a Cursor object relating to the key instead of the data item
        txn - an optional transaction
        """
        return self.range(
            index_name=index_name,
            lower=doc,
            upper=doc,
            limit=limit,
            page_number=page_number,
            keyonly=keyonly,
            txn=txn)

    @wrap_reader_yield
    def filter(
            self,
            index_name: Optional[str]=None,
            lower: Optional[Doc]=None,
            upper: Optional[Doc]=None,
            expression: Optional[Callable[Doc], bool]=None,
            context: Optional[FilterResult]=None,
            page_size: Optional[int]=0,
            inclusive: Optional[bool]=True,
            suppress_duplicates: Optional[bool]=False,
            txn: Optional[TXN]=None) -> Generator[Doc, None, None]:
        """
        Filter the table specified based on a criteria defined by the parameters passed.

        * Paging  To use the paging function, you need to supply both a page_size and context. If the
                  context is None and the page_size is positive, paging will start from the begininning
                  of theindex, and if the context is None and the page size is negative, paging will start
                  from the end. A positive page_size moves forwards through the index based on the context
                  and a negative page size moves backwards. For forward paging, the context will be the
                  last result from the previous page, and for moving backwards, the context will be the
                  first result from the previous page.
        * lambda  The "expression" parameter should be a lambda (or function) which will receive the
                  document and return a True/False based on whether the document should be included in
                  the search results. For example;
        ```
            filter(expression=lambda doc: doc['age'] > 19)
        ```

        index_name - the name of an index to search on, or None to use the primary key
        lower - the record at the lower end of the range
        upper - the record at the upper end of the range
        expression - an lambda expression to filter the results
        context - a paging context to determine where to start tge next page (see comments)
        page_size - maximum number of records to return
        inclusive - if set to True, include the keys at each end, i.e. use <=|=> rather than <|>
        suppress_duplicates - no duplicate keys, return only unique key values and ignore duplicates
        txn - an optional transaction
        """
        results = 0
        if index_name:
            if index_name not in self.data:
                raise NoSuchIndex
            index = self.data[index_name]
            db = index._db

            lower_keys = index.map_key(lower) if lower else [None]
            upper_keys = index.map_key(upper) if upper else [None]

            if not isinstance(lower_keys, list):
                lower_keys = [lower_keys]
            if not isinstance(upper_keys, list):
                upper_keys = [upper_keys]
        else:
            db = self._db
            index = None
            lower_keys = [lower.oid] if lower else [None]
            upper_keys = [upper.oid] if upper else [None]

        with txn.cursor(db) as cursor:
            for lower_key in lower_keys:
                upper_key = upper_keys.pop(0)
                next_record = cursor.next_nodup if suppress_duplicates else cursor.next
                prev_record = cursor.prev_nodup if suppress_duplicates else cursor.prev
                if page_size:
                    if index is None:
                        if not context:
                            if page_size > 0:
                                cursor.first()
                            else:
                                cursor.last()
                        else:
                            cursor.set_key(context._oid)
                            if page_size > 0:
                                if not next_record():
                                    return
                    else:
                        if context:
                            if index.duplicates:
                                cursor.set_key_dup(context.key, context._oid)
                            else:
                                cursor.set_key(context.key)
                            if page_size > 0:
                                if not next_record():
                                    return
                        else:
                            if page_size > 0:
                                cursor.set_range(lower_key) if lower_key else cursor.first()
                            else:
                                cursor.set_range(upper_key) if upper_key else cursor.last()

                    if page_size < 0:
                        page_size = abs(page_size)
                        for step in range(page_size):
                            if lower_key and (cursor.key() < lower_key or (
                                    cursor.key() == lower_key and not inclusive)):
                                break
                            if not step and not context:
                                continue
                            if not prev_record():
                                cursor.first()
                                if step:
                                    page_size = step
                                    break
                                else:
                                    return
                        else:
                            page_size = step + 1
                else:
                    cursor.set_range(lower_key) if lower_key else cursor.first()

                if cursor.key() == lower_key and not inclusive:
                    next_record()

                while cursor.key():
                    if (page_size and results == page_size) or (
                        upper_key and (cursor.key() > upper_key or (
                            cursor.key() == upper_key and not inclusive))):
                        break
                    result = FilterResult(self, index, cursor, txn=txn)
                    if not callable(expression) or expression(result.doc):
                        results += 1
                        yield result
                    next_record()
