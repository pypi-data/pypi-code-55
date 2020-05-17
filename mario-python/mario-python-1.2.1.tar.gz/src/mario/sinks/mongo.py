from mario.sinks.base import Sink
from pymongo import MongoClient
from pymongo.results import InsertOneResult
from typing import Dict


class MongoSink(Sink):
    """MongoSink
    Very basic Mongo connection and insert capability
    """
    def __init__(self, host: str, port: int, database: str = "mario", collection: str = "executions", **kwargs):
        super().__init__(name="Mongo")
        self.client = MongoClient(host=host, port=port, **kwargs)
        self._database = self.client[database]
        self._collection = self._database[collection]

    def read(self, query: Dict):
        records = []
        for record in self._collection.find(query):
            records.append(record)
        return records

    def write(self, record: Dict) -> InsertOneResult:
        self._collection.create_index("id")
        object_id = self._collection.insert_one(record)
        return object_id
