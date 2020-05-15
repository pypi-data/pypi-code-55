# -*- coding: utf-8 -*-
# @Date    : 2018-04-29 17:09:46
# @Author  : Md Nazrul Islam <email2nazrul@gmail.com>
# @Link    : http://nazrul.me/
# @Version : $Id$
# All imports here
from collective.elasticsearch import logger
from collective.elasticsearch.indexes import BaseIndex
from collective.fhirpath.utils import find_fhirfield_by_name
from Missing import MV
from plone.app.fhirfield.interfaces import IFhirResourceValue
from zope.interface import Invalid


__author__ = "Md Nazrul Islam <email2nazrul@gmail.com>"


class EsFhirFieldIndex(BaseIndex):
    """ """

    filter_query = True

    def validate_name(self, name):
        """"About validation of index/field name convention """
        attrs = self.index.indexed_attrs
        if len(attrs) > 0:
            attr = attrs[0]
        else:
            attr = name
        fhirfield = find_fhirfield_by_name(attr)
        if fhirfield is None:
            raise Invalid

    def create_mapping(self, name):
        """Minimal mapping for all kind of fhir models"""
        self.validate_name(name)
        return self.index.mapping

    def get_value(self, object):
        """ """
        value = None
        attrs = self.index.getIndexSourceNames()
        if len(attrs) > 0:
            attr = attrs[0]
        else:
            attr = self.index.id

        if getattr(self.index, "index_object", None):
            value = self.index._get_object_datum(object, attr, es_datum=True)
        else:
            logger.info(
                "catalogObject was passed bad index " "object {0!s}.".format(self.index)
            )
        if value == MV:
            return None

        if IFhirResourceValue.providedBy(value):
            value = value.as_json()

        return value

    def get_query(self, name, value):
        """Only prepared fhir query is acceptable
        other query is building here"""
        self.validate_name(name)
        value = self._normalize_query(value)
        if value in (None, ""):
            return
        raise NotImplementedError
