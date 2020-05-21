# -*- coding: utf-8 -*-
##################################################
#
# namespace 
# Module | Namespace
#
# Author: Daniel Bakas Amuchastegui
# August 31, 2017
# 
# Copyright © Semantyk 2020. All rights reserved.
##################################################

__all__ = [
    'DC',
    'DCTERMS',
    'DOAP',
    'FOAF',
    'OWL',
    'RDF',
    'RDFS',
    'SMTK',
    'SKOS',
    'XSD',
    'VOID'
]

from rdflib import Namespace

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