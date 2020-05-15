# -*- coding: utf-8 -*-
##################################################
#
# graph
# Module | Graph
#
# Daniel Bakas Amuchastegui
# March 16, 2020
# 
# Copyright © Semantyk 2020. All rights reserved.
##################################################

from semantyk.core.resource import Resource
from semantyk.namespace.namespace import RDFS, SMTK
from semantyk.uuid_generator import generate_uuid
from rdflib import Literal, URIRef

class Graph(Resource):
    id:str
    triples:set
    uri:URIRef

    def add_triple(self, s, p:URIRef, o):
        self.triples.add((s,p,o))

    def add_triples(self, *triples:tuple):
        for triple in triples:
            self.triples.add(triple)
        
    def add_triples(self, triples:set):
        for triple in triples:
            self.triples.add(triple)

    def get(self, s = None, p:URIRef = None, o = None):
        for _s,_p,_o in self.triples:
            if (not(s) and not(p) and not(o)) or \
            (s and _s == s) or \
            (p and _p == p) or \
            (o and _o == o):
                yield (_s,_p,_o)

    def get_objects(self, s = None, p:URIRef = None, o = None):
        for _s,_p,_o in self.triples:
            if (not(s) and not(p) and not(o)) or \
            (s and _s == s) or \
            (p and _p == p) or \
            (o and _o == o):
                yield _o

    def get_object_predicates(self, s = None, p:URIRef = None, o = None):
        for _s,_p,_o in self.triples:
            if (not(s) and not(p) and not(o)) or \
            (s and _s == s) or \
            (p and _p == p) or \
            (o and _o == o):
                yield (_o,_p)

    def get_object_subjects(self, s = None, p:URIRef = None, o = None):
        for _s,_p,_o in self.triples:
            if (not(s) and not(p) and not(o)) or \
            (s and _s == s) or \
            (p and _p == p) or \
            (o and _o == o):
                yield (_o,_s)

    def get_predicates(self, s = None, p:URIRef = None, o = None):
        for _s,_p,_o in self.triples:
            if (not(s) and not(p) and not(o)) or \
            (s and _s == s) or \
            (p and _p == p) or \
            (o and _o == o):
                yield _p

    def get_predicate_objects(self, s = None, p:URIRef = None, o = None):
        for _s,_p,_o in self.triples:
            if (not(s) and not(p) and not(o)) or \
            (s and _s == s) or \
            (p and _p == p) or \
            (o and _o == o):
                yield (_p,_o)

    def get_predicate_subjects(self, s = None, p:URIRef = None, o = None):
        for _s,_p,_o in self.triples:
            if (not(s) and not(p) and not(o)) or \
            (s and _s == s) or \
            (p and _p == p) or \
            (o and _o == o):
                yield (_p,_s)

    def get_subjects(self, s = None, p:URIRef = None, o = None):
        for _s,_p,_o in self.triples:
            if (not(s) and not(p) and not(o)) or \
            (s and _s == s) or \
            (p and _p == p) or \
            (o and _o == o):
                yield _s

    def get_subject_objects(self, s = None, p:URIRef = None, o = None):
        for _s,_p,_o in self.triples:
            if (not(s) and not(p) and not(o)) or \
            (s and _s == s) or \
            (p and _p == p) or \
            (o and _o == o):
                yield (s,o)

    def get_subject_predicates(self, s = None, p:URIRef = None, o = None):
        for _s,_p,_o in self.triples:
            if (not(s) and not(p) and not(o)) or \
            (s and _s == s) or \
            (p and _p == p) or \
            (o and _o == o):
                yield (_s,_p)
    
    def linked(self, s = None, p:URIRef = None, o = None):
        triples = set()
        for _s,_p,_o in self.triples:
            if isinstance(_o, URIRef) and \
            (not(s) and not(p) and not(o)) or \
            (s and _s == s) or \
            (p and _p == p) or \
            (o and _o == o):
                triples.add((_s,_p,_o))
        return Graph(self.id, triples = triples)

    def mirror(self, s = None, p:URIRef = None, o = None):
        for _s,_p,_o in self.triples:
            if (not(s) and not(p) and not(o)) or \
            (s and _s == s) or \
            (p and _p == p) or \
            (o and _o == o):
                yield (_o,_p,_s)

    def qualitative(self, s = None, p:URIRef = None, o = None, linked:bool = False):
        triples = set()
        for _s,_p,_o in self.triples:
            if isinstance(_o, Literal) and \
            (isinstance(_o.value, bool) or not(isinstance(_o.value, (int, float)))) and \
            (not(s) and not(p) and not(o)) or \
            (s and _s == s) or \
            (p and _p == p) or \
            (o and _o == o):
                triples.add((s,p,o.value))
            if linked and isinstance(o, URIRef):
                triples.add((s,p,o.value))
        return Graph(self.id, triples = triples)

    def quantitative(self, s = None, p:URIRef = None, o = None, linked:bool = False):
        triples = set()
        for _s,_p,_o in self.triples:
            if (isinstance(o, Literal) and \
            isinstance(o.value, (int, float)) and \
            not(isinstance(o.value, bool))) and \
            (not(s) and not(p) and not(o)) or \
            (s and _s == s) or \
            (p and _p == p) or \
            (o and _o == o):
                triples.add((s,p,o.value))
            if linked and isinstance(o, URIRef):
                triples.add((s,p,o.value))
        return Graph(self.id, triples = triples)

    def remove_triple(self, s = None, p:URIRef = None, o = None):
        for _s,_p,_o in self.triples:
            if (not(s) and not(p) and not(o)) or \
            (s and _s == s) or \
            (p and _p == p) or \
            (o and _o == o):
                self.triples.remove((_s,_p,_o))

    def remove_triples(self, triples:set):
        for triple in triples:
            self.triples.remove(triple)

    def to_dict(self):
        dictionary = dict()
        for s,p,o in self.triples:
            if str(s) not in dictionary:
                dictionary[str(s)] = dict()
            if str(p) not in dictionary[str(s)]:
                dictionary[str(s)][str(p)] = set()
            dictionary[str(s)][str(p)].add(o)
        return dictionary

    def to_resources(self, s = None, p:URIRef = None, o = None):
        resources = set()
        for _s,_p,_o in self.triples:
            if (not(s) and not(p) and not(o)) or \
            (s and _s == s) or \
            (p and _p == p) or \
            (o and _o == o):
                if not resources:resources.add(Resource(dictionary = {str(_p): {_o}}, uri = _s))
                for resource in resources:
                    if _s == resource.uri:
                        resource.add_value(str(_p), _o)
        return resources
    resources = property(to_resources)

    def update_triples(self, new_triple:tuple, old_triple:tuple):
        self.triples.remove(old_triple)
        self.triples.add(new_triple)

    def __eq__(self, other):
        return super().__eq__(other) and self.triples == other.triples

    def __init__(self, id:str = None, dictionary:dict = None, triples:set = None, uri:URIRef = None):
        super().__init__(id, dictionary, uri = uri)
        self.triples = triples

    def __iter__(self):
        for triple in self.triples:
            yield triple

    def __str__(self):
        result = str(self.uri)
        if self.triples:
            result += ':'
            triples = self.to_dict()
            for s in triples:
                result += '\n - ' + str(s) + ':'
                for p in triples[s]:
                    result += '\n  - ' + str(p)
                    for o in triples[s][p]:
                        result += '\n   - ' + str(o)
        return result