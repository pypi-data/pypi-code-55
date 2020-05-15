# _*_ coding: utf-8 _*_
from fhirpath.enums import FHIR_VERSION
from fhirpath.storage import MemoryStorage
from plone import api
from plone.app.fhirfield.interfaces import IFhirResource
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility
from zope.schema import getFields

import json
import os


__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"

FHIR_ES_MAPPINGS_CACHE = MemoryStorage()
releases = [member.name for member in FHIR_VERSION if member.name != "DEFAULT"]
for release in releases:
    if not FHIR_ES_MAPPINGS_CACHE.exists(release):
        FHIR_ES_MAPPINGS_CACHE.insert(release, MemoryStorage())
del releases

FHIRFIELD_NAMES_MAP = MemoryStorage()


def get_elasticsearch_mapping(
    resource, fhir_release="R4", mapping_dir=None, cache=True
):
    """Elastic search mapping for FHIR resources"""
    fhir_release = FHIR_VERSION[fhir_release].name
    if mapping_dir is None:
        mapping_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "browser",
            "static",
            "ES_MAPPINGS",
            fhir_release,
        )
    storage = FHIR_ES_MAPPINGS_CACHE.get(fhir_release)

    if resource not in storage or cache is False:
        file_location = None
        expected_filename = "{0}.mapping.json".format(resource)
        for root, dirs, files in os.walk(mapping_dir, topdown=True):
            for filename in files:
                if filename == expected_filename:
                    file_location = os.path.join(root, filename)
                    break

        if file_location is None:
            raise LookupError(
                "Mapping files {0}/{1} doesn't exists.".format(
                    mapping_dir, expected_filename
                )
            )

        with open(os.path.join(root, file_location), "r") as f:
            content = json.load(f)
            assert filename.split(".")[0] == content["resourceType"]

            storage[resource] = content

    return storage[resource]["mapping"]


def find_fhirfield_by_name(fieldname):
    """  """
    if fieldname in FHIRFIELD_NAMES_MAP:
        return FHIRFIELD_NAMES_MAP.get(fieldname)

    types_tool = api.portal.get_tool("portal_types")
    field_ = None

    def _from_schema(schema):
        for name, field in getFields(schema).items():
            if IFhirResource.providedBy(field) and name == fieldname:
                return field

    def _from_factory(factory):
        schema = factory.lookupSchema() or factory.lookupModel().schema
        field = _from_schema(schema)
        if field:
            return field
        for behavior in factory.behaviors:
            schema = getUtility(IBehavior, name=behavior).interface
            if schema is None:
                continue
            field = _from_schema(schema)
            if field:
                return field

    for type_name in types_tool.listContentTypes():
        factory = types_tool.getTypeInfo(type_name)
        if factory.meta_type != "Dexterity FTI":
            continue
        field_ = _from_factory(factory)
        if field_ is not None:
            break
    if field_:
        FHIRFIELD_NAMES_MAP.insert(fieldname, field_)
    return field_
