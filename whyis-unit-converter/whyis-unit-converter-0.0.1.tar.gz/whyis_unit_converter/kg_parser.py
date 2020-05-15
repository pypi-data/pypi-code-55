""" Provides an interface for rdflib Resources for Nanomine unit converter."""

import rdflib
import re
from .dictionary import read_dictionary

sio = rdflib.Namespace("http://semanticscience.org/resource/")

def measurement_attribute(unit_URI, new_value, unit_type):
    """ Creates a new sio:hasAttribute object."""
    new_meas = rdflib.resource.Resource(rdflib.Graph(), rdflib.BNode())
    new_meas.add(sio.hasUnit, rdflib.URIRef(unit_URI))
    new_meas.add(sio.hasValue, rdflib.Literal(new_value))
    new_meas.add(rdflib.RDF.type, unit_type)
    new_meas.add(rdflib.RDF.type, rdflib.URIRef("http://nanomine.org/nm/ConvertedUnit"))
    return new_meas

def attr_type(attr):
    """ Returns the slug of the URI for the object of RDF.type for the given subject."""
    try:
        temp = attr_type_URI(attr)
        type_slug = re.split("[/#]", temp)[-1].strip()
        return type_slug
    except IndexError:
        return temp
    except StopIteration:
        return ""

def attr_type_URI(attr):
    """ Returns the raw URI for the object of RDF.type for the given subject.
        Only returns the URI if it appears in the Nanomine dictionary of 
        allowed types"""
    try:
        type_URI = next(attr.objects(rdflib.RDF.type)).identifier
        return type_URI
    except StopIteration:
        return ""

def attr_unit(attr):
    """ Returns the slug of the URI for the object of sio.hasUnit for the given subject."""
    try:
        unit = next(attr.objects(sio.hasUnit)).identifier
        return re.split("[/#]", unit)[-1].strip()
    except IndexError:
        return unit
    except StopIteration:
        return ""

def attr_value(attr):
    """ Returns the object of sio.hasValue for the given subject."""
    try:
        return next(attr.objects(sio.hasValue)).value
    except StopIteration:
        return ""

def attr_preferred_units(attr):
    """ Returns the given attribute's preferred units, if any.
        Expects well-formed attribute for querying."""
    pref_unit_query = '''SELECT ?prefUnit WHERE {
    ?type <http://semanticscience.org/resource/hasPreferredUnit> ?prefUnit .
}'''
    pref_units = []
    ut_URI = attr_type_URI(attr)
    
    if ut_URI is None:
        return []

    for result in attr.graph.query(pref_unit_query, initBindings={"type":ut_URI}):
        try:
            pref_units.append(re.split("[/#]", result.prefUnit.value)[-1].strip())
        except IndexError:
            pref_units.append(result.prefUnit.value)
    return pref_units
