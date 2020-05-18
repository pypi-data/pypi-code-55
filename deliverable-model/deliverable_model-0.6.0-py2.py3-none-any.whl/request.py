from typing import List, Any

from deliverable_model.batch_like_dict import BatchLikeDict


class Request(BatchLikeDict):
    """
    Represent a list of request object
    """

    def __init__(self, query: List[Any]):
        self.query_history = []
        self["data"] = query

    @classmethod
    def from_dict(cls, data) -> "Request":
        self = cls(None)
        for k, v in data.items():
            self[k] = v

        return self

    @property
    def query(self):
        return self["data"]

    @query.setter
    def query(self, data):
        self["data"] = data

    def update_query(self, query):
        self.query_history.append(self.query)
        self["data"] = query
