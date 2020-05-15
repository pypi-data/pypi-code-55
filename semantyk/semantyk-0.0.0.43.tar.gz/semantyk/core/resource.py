# -*- coding: utf-8 -*-
##################################################
#
# resource 
# Module | Resource
#
# Author: Daniel Bakas Amuchastegui
# March 18, 2020
# 
# Copyright © Semantyk 2020. All rights reserved. 
##################################################

from semantyk.namespace.namespace import RDF, RDFS, SMTK
from semantyk.uuid_generator import generate_uuid 
from rdflib import Namespace, URIRef

class Resource(object):
    dictionary:dict
    id:str
    uri:URIRef

    def _get_isDefinedBy(self):
        return self.get_values(str(RDFS.isDefinedBy))
    isDefinedBy = property(_get_isDefinedBy)

    def _get_label(self):
        return self.get_values(str(RDFS.label))
    label = property(_get_label)

    def _get_type(self):
        return self.get_values(str(RDF.type))
    type = property(_get_type)

    def _get_properties(self):
        for p in self.dictionary: yield p
    properties = property(_get_properties)

    def _get_subClassOf(self):
        return self.get_values(str(RDFS.subClassOf))
    subClassOf = property(_get_subClassOf)

    def _get_values(self):
        return self.get_values()
    values = property(_get_values)

    def add_property(self, p:str):
        if p not in self.dictionary: self.dictionary[p] = set()

    def add_value(self, p:str, o):
        self.add_property(p)
        self.dictionary[p].add(o)

    def delete_property(self, p:str):
        if p in self.dictionary: del self.dictionary[p]

    def delete_value(self, p:str, o):
        if p in self.dictionary: self.dictionary[p].remove(o)

    def from_triples(self, triples:set = None):
        dictionary = dict()
        if triples:
            for triple in triples:
                if str(triple[1]) not in dictionary:
                    dictionary[str(triple[1])] = set()
                dictionary[str(triple[1])].add(triple[2])
        return dictionary
            
    def get_values(self, p:str):
        if p in self.dictionary:
            for o in self.dictionary[p]: yield o

    def to_triples(self):
        triples = set()
        for p in self.dictionary:
            for o in self.dictionary[p]:
                triples.add((self.uri, URIRef(p), o))
        return triples

    def update_property(self, old_p:str, new_p:str):
        self.dictionary[new_p] = self.dictionary[old_p]
        self.delete_property(old_p)

    def update_value(self, p:str, old_o, new_o):
        self.delete_value(p, old_o)
        self.add_value(p, new_o)

    def _generate_id(self, uri:URIRef = None):
        if uri and self.dictionary and str(RDFS.isDefinedBy) in self.dictionary:
            return str(uri).replace(list(self.dictionary[str(RDFS.isDefinedBy)])[0], '')
        return generate_uuid()

    def _generate_uri(self):
        if self.dictionary and str(RDFS.isDefinedBy) in self.dictionary:
            result = URIRef(str(next(self.isDefinedBy)) + self.id)
        return URIRef(SMTK) + self.id or self._generate_id()

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.dictionary == other.dictionary and self.id == other.id and self.uri == other.uri

    def __init__(self, id:str = None, dictionary:dict = None, triples:set = None, uri:URIRef = None):
        self.dictionary = dictionary or self.from_triples(triples)
        self.id = id or self._generate_id(uri)
        self.uri = uri or self._generate_uri()

    def __iter__(self):
        return self.properties

    def __hash__(self):
        return hash(self.uri)

    def __str__(self):
        result = self.id
        if self.dictionary:
            result += ':'
            for p in self.dictionary:
                result += '\n - ' + str(p)
                if self.dictionary[p]:
                    result += ':'
                    for o in self.dictionary[p]:
                        result += '\n  - ' + str(o)
        return result