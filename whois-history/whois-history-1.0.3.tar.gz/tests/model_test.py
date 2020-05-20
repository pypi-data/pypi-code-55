from whoishistory.models.historic import *
import unittest


class ApiClientTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_parsing_audit(self):
        payload = {
            "createdDate": "2020-04-25T17:25:49+00:00",
            "updatedDate": "2020-04-25T17:25:49+00:00",
        }

        parsed = Audit(payload)

        valid = Audit()
        valid.created_date = datetime.datetime(2020, 4, 25, 17, 25, 49, 0, tzinfo=datetime.timezone.utc)
        valid.updated_date = datetime.datetime(2020, 4, 25, 17, 25, 49, 0, tzinfo=datetime.timezone.utc)

        if parsed != valid:
            self.assertTrue(False)
        else:
            self.assertEqual(parsed, valid)

    def test_parsing_contact(self):
        payload = {
            'name': 'name-value',
            'organization': 'organization-value',
            'street': 'street-value',
            'city': 'city-value',
            'state': 'state-value',
            'postalCode': 'postalCode-value',
            'country': 'country-value',
            'email': 'email-value',
            'telephone': 'telephone-value',
            'telephoneExt': 'telephoneExt-value',
            'fax': 'fax-value',
            'faxExt': 'faxExt-value',
            'rawText': 'rawText-value',
        }

        parsed = Contact(payload)

        valid = Contact()
        valid.name = 'name-value'
        valid.organization = 'organization-value'
        valid.street = 'street-value'
        valid.city = 'city-value'
        valid.state = 'state-value'
        valid.postal_code = 'postalCode-value'
        valid.country = 'country-value'
        valid.email = 'email-value'
        valid.telephone = 'telephone-value'
        valid.telephone_ext = 'telephoneExt-value'
        valid.fax = 'fax-value'
        valid.fax_ext = 'faxExt-value'
        valid.raw_text = 'rawText-value'

        if parsed != valid:
            self.assertTrue(False)
        else:
            self.assertEqual(parsed, valid)

    def test_parsing_whoisRecord(self):
        payload = {
            'domainName': 'domainName',
            'domainType': 'domainType',
            'createdDateISO8601': '2020-04-25T17:25:00+00:00',
            'updatedDateISO8601': '2020-04-25T17:25:01+00:00',
            'expiresDateISO8601': '2020-04-25T17:25:02+00:00',
            'createdDateRaw': 'createdDateRaw',
            'updatedDateRaw': 'updatedDateRaw',
            'expiresDateRaw': 'expiresDateRaw',
            'audit': {"createdDate": "2020-04-25T17:25:49+00:00"},
            'nameServers': ['nameServers'],
            'whoisServer': 'whoisServer',
            'registrarName': 'registrarName',
            'status': ['status'],
            'cleanText': 'cleanText',
            'rawText': 'rawText',
            'registrantContact': {'name': 'registrantContact'},
            'administrativeContact': {'name': 'administrativeContact'},
            'technicalContact': {'name': 'technicalContact'},
            'billingContact': {'name': 'billingContact'},
            'zoneContact': {'name': 'zoneContact'},
        }

        parsed = WhoisRecord(payload)

        valid = WhoisRecord()
        valid.domain_name = 'domainName'
        valid.domain_type = 'domainType'
        valid.created_date_iso8601 = datetime.datetime(2020, 4, 25, 17, 25, 0, 0, tzinfo=datetime.timezone.utc)
        valid.updated_date_iso8601 = datetime.datetime(2020, 4, 25, 17, 25, 1, 0, tzinfo=datetime.timezone.utc)
        valid.expires_date_iso8601 = datetime.datetime(2020, 4, 25, 17, 25, 2, 0, tzinfo=datetime.timezone.utc)
        valid.created_date_raw = 'createdDateRaw'
        valid.updated_date_raw = 'updatedDateRaw'
        valid.expires_date_raw = 'expiresDateRaw'
        valid.audit = Audit({"createdDate": "2020-04-25T17:25:49+00:00"})
        valid.name_servers = ['nameServers']
        valid.whois_server = 'whoisServer'
        valid.registrar_name = 'registrarName'
        valid.status = ['status']
        valid.clean_text = 'cleanText'
        valid.raw_text = 'rawText'
        valid.registrant_contact = Contact({'name': 'registrantContact'})
        valid.administrative_contact = Contact({'name': 'administrativeContact'})
        valid.technical_contact = Contact({'name': 'technicalContact'})
        valid.billing_contact = Contact({'name': 'billingContact'})
        valid.zone_contact = Contact({'name': 'zoneContact'})

        if parsed != valid:
            self.assertTrue(False)
        else:
            self.assertEqual(parsed, valid)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
