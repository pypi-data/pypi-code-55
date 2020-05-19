from enum import Enum
from collections import OrderedDict, defaultdict
import functools
import csv

from .base import Node, Way, Relation, GenericElementQuery, CompoundQuery
from .settings import QuerySettings
from .filters import BboxFilter, TagFilter, IdFilter, UserFilter
from .formats import OutputFormatter, opf

import requests


__all__ = ["NodeQuery",
           "WayQuery",
           "RelationQuery",
           "NodeWayQuery",
           "NodeRelationQuery",
           "WayRelationQuery",
           "NodeWayRelationQuery",
           "QueryBuilder",
           "tagstring_to_oql",
           "nominatim_from_csv"]


class NodeQuery(GenericElementQuery):
    _element = Node


class WayQuery(GenericElementQuery):
    _element = Way


class RelationQuery(GenericElementQuery):
    _element = Relation


class NodeWayQuery(CompoundQuery):
    _elements = (Node, Way)


class NodeRelationQuery(CompoundQuery):
    _elements = (Node, Relation)


class WayRelationQuery(CompoundQuery):
    _elements = (Way, Relation)


class NodeWayRelationQuery(CompoundQuery):
    _elements = (Node, Way, Relation)



class QueryRegister:
    def __init__(self, qb):
        self.qb = qb
        self.qc = list()
        self.r = OrderedDict()

    def __getattr__(self, qname):
        try:
            return self.r[qname]
        except KeyError:
            raise NameError("Named query: {} does not exist".format(qname))

    def append(self, qs, name=None):
        if not self.qc:
            assert qs._input is None
        if not name:
            self.qc.append(qs)
        else:
            self.r[name] = qs
            self.qc.append(name)

    @property
    def _dset(self):
        _ = reversed(self.qc)
        while True:
            item = next(_)
            if item not in self.r.keys():
                return item

    @property
    def output(self):
        return self._dset._output

    def __repr__(self):
        return f'''{"".join(repr(qs) for qs in self.qc)}'''



class QueryBuilder:
    overpass_endpoint = 'http://overpass-api.de/api/interpreter'

    def __init__(self, name="default", basic_optimize=True, **kwargs):
        self.name = name
        self.settings = QuerySettings(**kwargs)
        self.output_mode = OutputFormatter()
        self.qsx = QueryRegister(self)
        if basic_optimize:
            self.output_mode.SORTORDER = opf.SortOrder.QUADTILE

    @property
    def GlobalBoundingBox(self):
        return self.settings.bbox

    @GlobalBoundingBox.setter
    def GlobalBoundingBox(self, bbox):
        self.settings.bbox = bbox

    def include_geometries(self):
        self.output_mode.GEOMETRY = opf.Geometry.FULL_GEOM

    def include_boundingboxes(self):
        self.output_mode.GEOMETRY = opf.Geometry.BOUNDING_BOX

    def include_centerpoints(self):
        self.output_mode.GEOMETRY = opf.Geometry.CENTER_POINT

    @property
    def raw_query_string(self):
        return f'''{self.settings}{self.qsx}{self.output_mode}'''

    @classmethod
    def from_query(cls, query, *args, **kwargs):
        inst = cls(*args, **kwargs)
        cls._query = query

    def request(self):
        return requests.get(self.overpass_endpoint, data=self.raw_query_string)


def tagstring_to_oql(tagstring):
    dd = defaultdict(list)
    s = [_.strip().split("=") for _ in tagstring.split("OR")]
    for k, v in s:
        dd[k].append(v)
    return functools.reduce(lambda x, y: x + y, [TagFilter(k,  vals=v) for k, v in dd.items()])

def nominatim_from_csv(path):
    d = dict()
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            d[row['word']] = row['query']
    return d



