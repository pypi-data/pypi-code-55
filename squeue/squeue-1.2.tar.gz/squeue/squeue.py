"""
squeue: A simple SQLite Queue
"""
import os
import sqlite3
from pickle import loads, dumps
from time import sleep

try:
    from thread import get_ident
except ImportError:
    try:
        from dummy_thread import get_ident
    except ImportError:
        from threading import get_ident

try:
    buffer = buffer
except NameError:
    buffer = memoryview

class ObjectQueue():
    """
    Object Queue Interface.
    """

    def __len__(self):
        return 0

    def __iter__(self):
        yield None

    def enqueue(self, obj, **kwargs):
        "Add an item to the queue."

    def dequeue(self, **kwargs):
        "Remove the first item off the queue."

    def peek(self):
        "See if we have another item."

class SqliteQueue(ObjectQueue):
    """
    SQLite Queue Implementation.
    """

    _create = (
        'CREATE TABLE IF NOT EXISTS queue '
        '('
        '  id INTEGER PRIMARY KEY AUTOINCREMENT,'
        '  item BLOB'
        ')'
    )
    _count = 'SELECT COUNT(*) FROM queue'
    _iterate = 'SELECT id, item FROM queue'
    _append = 'INSERT INTO queue (item) VALUES (?)'
    _write_lock = 'BEGIN IMMEDIATE'
    _popleft_get = (
        'SELECT id, item FROM queue '
        'ORDER BY id LIMIT 1'
    )
    _popleft_del = 'DELETE FROM queue WHERE id = ?'
    _peek = (
        'SELECT item FROM queue '
        'ORDER BY id LIMIT 1'
    )

    def __init__(self, path):
        self.created = False
        self.path = os.path.abspath(path)
        self._connection_cache = {}

    def __create(self):
        if not self.created:
            if not os.path.exists(self.path):
                with self.__get_conn() as conn:
                    conn.execute(self._create)
            self.created = True

    def __get_conn(self):
        id_item = get_ident()
        if id_item not in self._connection_cache:
            self._connection_cache[id_item] =\
                sqlite3.Connection(self.path, timeout=60)
        return self._connection_cache[id_item]

    def __len__(self):
        self.__create()
        with self.__get_conn() as conn:
            for length in conn.execute(self._count):
                return length
        return 0

    def __iter__(self):
        self.__create()
        with self.__get_conn() as conn:
            for _, obj_buffer in conn.execute(self._iterate):
                yield loads(bytes(obj_buffer))

    def enqueue(self, obj, **kwargs):
        obj_buffer = buffer(dumps(obj, 2))
        self.__create()
        with self.__get_conn() as conn:
            conn.execute(self._append, (obj_buffer,))

    def dequeue(self, **kwargs):
        sleep_wait = kwargs.get('sleep_wait', True)
        wait = 0.1
        max_wait = 2
        tries = 0
        self.__create()
        with self.__get_conn() as conn:
            id_item = None
            while True:
                try:
                    cursor = conn.execute(self._popleft_get)
                    conn.execute(self._write_lock)
                    id_item, obj_buffer = cursor.fetchone()
                    break
                except StopIteration:
                    conn.commit() # Unlock the database
                    if not sleep_wait:
                        break
                    tries += 1
                    try:
                        sleep(wait)
                        wait = min(max_wait, tries/10 + wait)
                    except Exception:
                        return None
                except Exception:
                    return None
            if id_item:
                conn.execute(self._popleft_del, (id_item,))
                return loads(bytes(obj_buffer))
        return None

    def peek(self):
        self.__create()
        with self.__get_conn() as conn:
            cursor = conn.execute(self._peek)
            try:
                obj_buffer = cursor.fetchone()[0]
                return loads(bytes(obj_buffer))
            except StopIteration:
                return None
