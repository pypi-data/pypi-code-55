# -*- coding: utf-8 -*-
# @Date    : 2018-05-19 17:18:14
# @Author  : Md Nazrul Islam (email2nazrul@gmail.com)
# @Link    : http://nazrul.me/
# @Version : $Id$
# All imports here
from .EsFhirFieldIndex import EsFhirFieldIndex
from collective.elasticsearch.indexes import INDEX_MAPPING as CIM
from collective.fhirpath.PluginIndexes import FhirFieldIndex


def monkey_patch():
    """ """
    INDEX_MAPPING = {FhirFieldIndex: EsFhirFieldIndex}
    # Tiny patch
    CIM.update(INDEX_MAPPING)
