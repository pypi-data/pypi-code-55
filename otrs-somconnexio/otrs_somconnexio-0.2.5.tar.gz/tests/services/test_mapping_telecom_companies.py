import unittest

from otrs_somconnexio.services.mapping_telecom_companies import ServiceMappingTelecomCompanies


class ServiceMappingTelecomCompaniesTestCase(unittest.TestCase):
    def test_mapping_other(self):
        self.assertEqual("Other", ServiceMappingTelecomCompanies.telecom_company('BananaPhone'))

    def test_mapping_existent_telecom_company(self):
        self.assertEqual("Nubip", ServiceMappingTelecomCompanies.telecom_company('Aire / Nubip'))
