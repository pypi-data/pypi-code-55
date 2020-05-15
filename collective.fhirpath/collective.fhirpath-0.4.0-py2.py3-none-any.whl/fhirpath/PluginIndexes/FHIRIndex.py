# -*- coding: utf-8 -*-
# @Date    : 2018-04-30 20:10:43
# @Author  : Md Nazrul Islam (email2nazrul@gmail.com)
# @Link    : http://nazrul.me/
# @Version : $Id$
# All imports here
from App.special_dtml import DTMLFile
from collective.fhirpath.utils import find_fhirfield_by_name
from collective.fhirpath.utils import get_elasticsearch_mapping
from plone.app.fhirfield.interfaces import IFhirResourceValue
from Products.PluginIndexes.FieldIndex.FieldIndex import FieldIndex

import json
import six
import warnings


__author__ = "Md Nazrul Islam <email2nazrul@gmail.com>"


def make_fhir_index_datum(mapping, fhir_json):
    """ """
    container = dict()
    for key, meta in six.iteritems(mapping):
        if key not in fhir_json:
            continue

        if "properties" in meta and fhir_json.get(key):
            # nested value
            container[key] = make_fhir_index_datum(
                meta.get("properties"), fhir_json.get(key)
            )

        else:
            if meta["type"] == "string":
                container[key] = (
                    fhir_json.get(key) and six.text_type(fhir_json.get(key)) or None
                )

            elif meta["type"] == "datetime":
                # XXX: make DateTime object again?
                container[key] = fhir_json.get(key)
    return container


class FhirFieldIndex(FieldIndex):
    """ """

    meta_type = "FhirFieldIndex"
    query_options = ("query", "not")
    manage = manage_main = DTMLFile("dtml/manageFhirFieldIndex", globals())
    manage_main._setName("manage_main")
    default_mapping = dict(
        properties={
            "id": {"type": "string"},
            "meta": {
                "properties": {
                    "lastUpdated": {"type": "datetime"},
                    "versionId": {"type": "string"},
                }
            },
            "resourceType": {"type": "string"},
        }
    )

    def __init__(self, id, ignore_ex=None, call_methods=None, extra=None, caller=None):
        """ """
        super(FhirFieldIndex, self).__init__(
            id, ignore_ex=None, call_methods=None, extra=None, caller=None
        )

    def _get_object_datum(self, obj, attr, es_datum=False):
        """Extra param `es_datum` has been added to working
        Elasticsearch mapping"""
        datum = super(FhirFieldIndex, self)._get_object_datum(obj, attr)

        if es_datum:
            # No Filter
            return datum

        if not datum:
            # Nothing to do
            return datum

        fhir_value = None
        if IFhirResourceValue.providedBy(datum):
            fhir_value = datum.as_json()

        if isinstance(datum, six.string_types):
            try:
                fhir_value = json.loads(datum)
            except ValueError:
                warnings.warn(
                    "{0}'s value must be valid "
                    "FHIR Resource json. But got-> {1}".format(attr, fhir_value),
                    UserWarning,
                )
                return
        if fhir_value:
            # we make datum very tiny version! do we need whole doc? but stored in ES
            datum = make_fhir_index_datum(
                self.default_mapping.get("properties"), fhir_value
            )
            # issue: https://github.com/zopefoundation/BTrees/issues/109
            datum = json.dumps(datum, sort_keys=True)
            # https://stackoverflow.com/questions/10844064/items-in-json-object-are-out-of-order-using-json-dumps

        return datum

    def unindex_object(self, documentId):
        """ """
        return super(FhirFieldIndex, self).unindex_object(documentId)

    def index_object(self, documentId, obj, threshold=None):
        """ """
        return super(FhirFieldIndex, self).index_object(documentId, obj, threshold=None)

    @property
    def mapping(self):
        """Minimal mapping for all kind of fhir models"""
        if len(self.indexed_attrs):
            fieldname = self.indexed_attrs[0]
        else:
            fieldname = self.id

        fhirfield = find_fhirfield_by_name(fieldname)

        try:
            mapping = fhirfield.get_mapping()
            if mapping:
                return mapping
        except AttributeError:
            pass

        mapping = get_elasticsearch_mapping(
            fhirfield.get_resource_type(), fhir_release=fhirfield.get_fhir_release()
        )
        if mapping:
            return mapping
        else:
            warnings.warn(
                "No mapping found for `{0}`, instead minimal "
                "mapping has been used.".format(fieldname),
                UserWarning,
            )

        # Return the base/basic mapping
        return self.default_mapping


def manage_addFhirFieldIndex(
    self, id, extra=None, REQUEST=None, RESPONSE=None, URL3=None
):
    """Add a fhir field index"""
    return self.manage_addIndex(
        id, "FhirFieldIndex", extra=extra, REQUEST=REQUEST, RESPONSE=RESPONSE, URL1=URL3
    )


manage_addFhirFieldIndexForm = DTMLFile(
    "dtml/addFhirFieldIndexForm", globals()
)  # noqa: E305


REGISTRABLE_CLASSES = [
    # index, form, action
    (FhirFieldIndex, manage_addFhirFieldIndexForm, manage_addFhirFieldIndex)
]
