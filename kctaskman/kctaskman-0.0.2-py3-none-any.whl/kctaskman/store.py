import socket

from pymongo import MongoClient

import kctaskman.util
from kctaskman.log import logger


class Store:

    def __init__(self, connect_str, coll_prefix=None, coll_suffix=None):
        self._coll_prefix = coll_prefix
        self._coll_suffix = coll_suffix
        self._client = MongoClient(connect_str, maxPoolSize=1)
        self._hostname = socket.gethostname()
        self._db = self._client.get_default_database()
        self._type = type

    def getColl(self, name):
        return self._db.get_collection(name)

    def _getCollectionName(self, name):
        coll_name = ''
        if self._coll_prefix:
            coll_name += self._coll_prefix + '_'
        coll_name += name
        if self._coll_suffix:
            coll_name += '_' + self._coll_suffix
        return coll_name

    def __getattr__(self, name):
        if name in self.__dict__:
            return object.__getattribute__(self, name)
        return self._db.get_collection(self._getCollectionName(name))

    def db(self, name):
        return self._db.get_collection(name)

    def saveVar(self, field, value):
        self.cfg.update_one(
            {'_id': field},
            {'$set': self._withMeta(value=value)},
            upsert=True)

    def pushVar(self, field, value):
        self.cfg.update(
            {'_id': field},
            {
                '$push': {'value': value},
                '$set': self._withMeta(),
            },
            upsert=True)

    def loadVar(self, field):
        result = self.cfg.find_one({'_id': field})
        if result:
            return result['value']
        return None

    def delVar(self, field):
        return self.cfg.remove({'_id': field})

    def _withMeta(self, **kwargs):
        kwargs['hostname'] = self._hostname
        kwargs['update_at'] = kctaskman.util.strtime()
        return kwargs

    def loadVarOrSave(self, field, default):
        doc = self.cfg.find_one_and_update(
            {'_id': field},
            {
                '$set': self._withMeta(),
                '$setOnInsert': dict(value=default),
            },
            upsert=True, new=True)
        return doc['value']

    def error(self, **kwargs):
        kwargs['create_at'] = kctaskman.util.strtime()
        self.err.insert_one(kwargs)
        logger.error('saved error. error=%s', kwargs)

