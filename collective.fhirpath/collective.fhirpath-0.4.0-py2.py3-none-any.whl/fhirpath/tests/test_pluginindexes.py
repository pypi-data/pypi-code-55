# _*_ coding: utf-8 _*_
from collective.fhirpath import utils
from collective.fhirpath.testing import COLLECTIVE_FHIRPATH_INTEGRATION_TESTING

import unittest


__author__ = "Md Nazrul Islam <email2nazrul@gmail.com>"


class PluginIndexesIntegrationTest(unittest.TestCase):
    """ """

    layer = COLLECTIVE_FHIRPATH_INTEGRATION_TESTING

    def setUp(self):
        """ """
        self.portal = self.layer["portal"]

    def test_get_mapping(self):
        """ """
        catalogtool = getattr(self.portal, "portal_catalog")
        catalogtool._catalog.getIndex("organization_resource")
        mapping1 = catalogtool._catalog.getIndex("organization_resource").mapping
        mapping2 = utils.get_elasticsearch_mapping("Organization", "STU3")

        self.assertEqual(mapping1, mapping2)
