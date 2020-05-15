# -*- coding: utf-8 -*-
"""Init and utils."""
from collective.fhirpath.EsIndexes import monkey_patch


__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"


def initialize(context):
    """ """
    import logging

    log = logging.getLogger("collective.fhirpath")

    # Registering Pluggable indexes for FHIR
    from collective.fhirpath.PluginIndexes import REGISTRABLE_CLASSES

    for index, form, action in REGISTRABLE_CLASSES:

        context.registerClass(
            index,
            permission="Add Pluggable Index",
            constructors=(form, action),
            icon="indexes/PluginIndexes/index.gif",
            visibility=None,
        )
        log.info("`{0}`  pluggable index has been registered".format(index.__name__))


monkey_patch()
