import warnings
import os
import sys
from mrsdb2.exceptions import *
from mrsdb2.cache import Cache
from http.server import HTTPServer, ThreadingHTTPServer, BaseHTTPRequestHandler
import itertools
import time
import random
import json
from mrsdb2.atomicwrite import atomic_write
import pickle
import binascii
import urllib.parse
import base64
installbsonmsg = 'bson is not installed. (https://pypi.org/project/bson/)'
try:
    import bson
except ModuleNotFoundError:
    raise ModuleNotFoundError(installbsonmsg)
import bson as jsn
import uuid
dbi = {}


class Database:
    # DATABASE MANAGMENT
    def __init__(self, location, **kwargs): 
        """
        Create database object.
        """
        # Args:
        #     - location: DB File location (ex. "./databases/app")
        #     Optional:
        #       - name: Name of database (Generated from file name if not given) (ex. "app")
        self.cache = kwargs.get('cache', True) # Set cache to True if none
        if self.cache == True: 
            self.cache = Cache() # Use default cache if cache is set to True
        self.ver = "2.1.1" # mrsdb version
        self.db_loc = location # Location of database file
        self.db_dir = os.path.dirname(os.path.realpath(self.db_loc)) # Directory of database file
        self.db_name = kwargs.get('name', os.path.splitext(os.path.basename(self.db_loc))[0]) # Name of database (passed or from file)
        self.db = None # DB must be loaded using load function to be used
        self.store_loc = os.path.join(self.db_dir, f'{self.db_name}_store') # Location of database "store" folder
        global dbi
        dbi[self.db_name] = self


    def format(self):
        """
        Format/create database
        """
        with open(self.db_loc, 'wb') as f:
            db = {"_summation": {"c_ver": self.ver, "e_ver":self.ver}}
            f.write(jsn.dumps(db)) # Write blank database to file
   

    def init(self, check=None): 
        """ 
        Initiate database by creating "store" folder 
        """
        # Args:
        #     Optional:
        #         - check: Whether to check if directory already exists and skip if so (ex. True)
        loc = self.store_loc
        if check:
            if os.path.isdir(loc): # Check if store folder already exists
                return True # Return True if so
        return os.mkdir(loc) # Otherwise, make directory
    

    def cleanup(self): 
        """
        Empty "store" folder and remove unneccesary database items created by mrsdb
        """
        fl = [ f for f in os.listdir(self.store_loc) ]
        for f in fl: 
            os.remove(os.path.join(self.store_loc, f))


    def load(self): 
        """
        Load database from file into memory
        """
        with open(self.db_loc, 'rb') as f: 
            try: 
                self.db = jsn.loads(f.read())
            except json.decoder.JSONDecodeError as e: 
                er = f'Could not load database.\n{e}'
                raise DecodeError(er)
            self.db['_summation']['e_ver'] = self.ver
            if self.db['_summation']['c_ver'] == '2.1.0':
                warnings.warn('This database was created on a version with security vulnerabilities.')
    
    
    def commit(self): 
        """
        Push in-memory database to file
        """
        self.cleanup()
        dumps = jsn.dumps(self.db)
        if not dumps or dumps == '':
            raise CommitError('Could not commit database.')
        with atomic_write(self.db_loc, text=False, suffix='.mrsdb.bak', store_loc=self.store_loc) as f:
            f.write(dumps)


    def make_table(self, name): 
        """
        Create a new table, raises Exists if none.
        """
        # Args:
        #     - name: Table name (ex. "Users")
        if self.db.get(name, None) is None: 
            self.db[name] = {}
        else: 
            raise Exists(name)


    # QUERIES
    def get(self, table, **item): 
        """
        Get an item from the Database (returns tuple)
        """
        # Args:
        #     - table: Table to search (ex. "Users")
        #     - item: Item to search for (ex. name="abcdefg")
        return tuple(self.gget(table, **item))


    def gget(self, table, **item): 
        """"
        Get an item from the Database (returns generator)
        """
        # Args:
        #     - table: Table to search (ex. "Users")
        #     - item: Item to search for (ex. name="abcdefg")
        tn = table
        table = self.db[tn]
        for ik in table: 
            key, value = tuple(itertools.islice(item.items(), 1))[0]
            if self.cache: 
                if f'{tn}:{ik}' in self.cache.cache: 
                    if self.cache.cache[f'{tn}:{ik}'].get(key) == value:
                        yield self.cache.cache[f'{tn}:{ik}']
                        continue
            i = table[ik]
            if not type(i) == dict: 
                continue
            if not key in i.keys(): 
                continue
            if value == i[key]: 
                if self.cache: 
                    self.cache.cache[f'{tn}:{ik}'] = Item(tn, ik, i, self.db_name)
                yield Item(tn, ik, i, self.db_name)


    def add(self, table, value, commit=None): 
        """
        Add item to the database (tuples are converted to dicts if possible)
        """
        if type(value) == tuple: 
            try: 
                value = dict(value)
            except ValueError: 
                pass
        if type(value) == dict:
            for v in value:
                if type(value[v]) == str:
                    value[v] = urllib.parse.quote(value[v])
                if type(value[v]) == tuple and len(value[v]) == 2:
                    value[v] = f'${value[v][0]}:{value[v][1]}'
        uid = uuid.uuid4().hex
        self.db[table][uid] = value
        if commit: 
            self.commit()


    def aadd(self, table, value, commit=None): 
        """
        Asyncronously call add function
        """
        p = Process(target=self.add, args=(table, value, commit))
        p.start()
        return p

    def rollback(self):
        with open(self.db_loc, 'rb'):
            self.db = jsn.loads()
    def __repr__(self): 
        return f'<Database {self.db_name}>'


class Item(dict): 
    """
    Readable and Updatable database item
    """
    def __init__(self, table, ik, i, n): 
        self.__db_name__ = n
        self.__ik__ = ik
        self.__i__ = i
        self.__table__ = table
        self.mrsdb_uid = ik

    
    def __getattr__(self, name): 
        return self[name]
    
    
    def __setattr__(self, attr, value): 
        self[attr] = value
        if not attr.startswith('__'): 
            dbi[self['__db_name__']].db[self['__table__']][self['__ik__']][attr] = value
        if '__i__' in self: 
            for x in self['__i__']: 
                if type(self['__i__'][x]) == str:
                    if self['__i__'][x].startswith('$BIGINT:'): 
                        self['__i__'][x] = "%.0f" % int(self['__i__'][x][8: ])
                    if self['__i__'][x].startswith('$BIGFLT:'):
                        self['__i__'][x] = "%.8f" % float(self['__i__'][x][8: ])
                    if self['__i__'][x].startswith('$PYCKLE:'):
                        self['__i__'][x] = pickle.loads(binascii.unhexlify(self['__i__'][x][8:]))
                if type(self['__i__'][x]) == str:
                    self[x] = urllib.parse.unquote(self['__i__'][x])
                else:
                    self[x] = self['__i__'][x]


    def __repr__(self): 
        return f'<Item {self.mrsdb_uid}>'