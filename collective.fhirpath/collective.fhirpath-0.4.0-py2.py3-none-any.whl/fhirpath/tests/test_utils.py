# _*_ coding: utf-8 _*_
from collective.fhirpath import utils
from collective.fhirpath.testing import COLLECTIVE_FHIRPATH_INTEGRATION_TESTING

import unittest


__author__ = "Md Nazrul Islam <email2nazrul@gmail.com>"


class UtilsIntegrationTest(unittest.TestCase):
    """ """

    layer = COLLECTIVE_FHIRPATH_INTEGRATION_TESTING

    def setUp(self):
        """ """
        self.portal = self.layer["portal"]

    def test_find_fhirfield_by_name(self):
        """ """
        fhirfield = utils.find_fhirfield_by_name("patient_resource")
        self.assertIsNotNone(fhirfield)
        self.assertEqual(fhirfield.get_resource_type(), "Patient")
        self.assertEqual(fhirfield.get_fhir_release(), "STU3")
        # Test with unknown
        fhirfield = utils.find_fhirfield_by_name("fake_fieldname")
        self.assertIsNone(fhirfield)

    def test_get_elasticsearch_mapping(self):
        """ """
        mapping = utils.get_elasticsearch_mapping("Patient")
        self.assertIsNotNone(mapping)

        mapping = utils.get_elasticsearch_mapping("Patient", "STU3")
        self.assertIsNotNone(mapping)

        try:
            utils.get_elasticsearch_mapping("FakeResource", "STU3")
            raise AssertionError("Code should not come here!")
        except LookupError:
            pass
