"""
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Namespace
Module | `namespace.py`

Daniel Bakas Amuchastegui\
May 21, 2020

Copyright © Semantyk 2020. All rights reserved.\
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
"""

__all__ = [
    'DC',
    'DCTERMS',
    'DOAP',
    'FOAF',
    'Namespace',
    'OWL',
    'RDF',
    'RDFS',
    'SMTK',
    'SKOS',
    'XSD',
    'VOID'
]

from .identifier.uriref import URIRef
from rdflib import Namespace

class Namespace(str):
    __slots__ = ()

    @property
    def title(self):
        return URIRef(self + 'title')

    def term(self, name):
        return URIRef(self + name) if isinstance(name, str) else self

    def __getattr__(self, name):
        if name.startswith('__'):
            raise AttributeError
        return self.term(name)

    def __getitem__(self, key):
        return self.term(key)

    def __new__(cls, value):
        return str.__new__(cls, value)

    def __repr__(self):
        return "Namespace('%s')" % self

DC = Namespace('http://purl.org/dc/elements/1.1/')
DCTERMS = Namespace('http://purl.org/dc/terms/')
DOAP = Namespace('http://usefulinc.com/ns/doap#')
FOAF = Namespace('http://xmlns.com/foaf/0.1/')
OWL = Namespace('http://www.w3.org/2002/07/owl#')
RDF = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
SMTK = Namespace('https://raw.githubusercontent.com/semantyk/Semantyk/master/Archive/archive.ttl/')
SKOS = Namespace('http://www.w3.org/2004/02/skos/core#')
XSD = Namespace('http://www.w3.org/2001/XMLSchema#')
VOID = Namespace('http://rdfs.org/ns/void#')