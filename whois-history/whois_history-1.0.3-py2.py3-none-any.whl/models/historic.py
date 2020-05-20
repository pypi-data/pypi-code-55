import datetime
import re

re_offset = re.compile(r'(\d\d):(\d\d)$')


def _datetime_value(values: dict, key: str) -> datetime.datetime or None:
    if key in values:
        if values[key] is None:
            return None
        v = str(values[key])
        v = re_offset.sub(r"\1\2", v)
        return datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S%z')

    return None


def _integer_value(values: dict, key: str) -> int:
    if key in values:
        return int(values[key])
    return 0


def _string_value(values: dict, key: str) -> str:
    if key in values:
        return str(values[key])
    return ''


def _string_list_value(values: dict, key: str) -> list:
    str_list = list()

    if key in values and isinstance(values[key], list):
        for v in values[key]:
            str_list.append(str(v))

    return str_list


# Audit is a part of whois API response. It represents dates
# when whois record was added and updated in our database.
class Audit:
    created_date: datetime.datetime or None
    updated_date: datetime.datetime or None

    def __init__(self, values: dict = None):
        self.created_date = None
        self.updated_date = None

        if values is None:
            return

        self.created_date = _datetime_value(values, 'createdDate')
        self.updated_date = _datetime_value(values, 'updatedDate')

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return isinstance(other, Audit) and \
               self.created_date == other.created_date and \
               self.updated_date == other.updated_date


# Contact is a part of the API response
class Contact:
    name: str
    organization: str
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    email: str
    telephone: str
    telephone_ext: str
    fax: str
    fax_ext: str
    raw_text: str

    def __init__(self, values: dict = None):
        self.name = ''
        self.organization = ''
        self.street = ''
        self.city = ''
        self.state = ''
        self.postal_code = ''
        self.country = ''
        self.email = ''
        self.telephone = ''
        self.telephone_ext = ''
        self.fax = ''
        self.fax_ext = ''
        self.raw_text = ''

        if values is None:
            return

        self.name = _string_value(values, 'name')
        self.organization = _string_value(values, 'organization')
        self.street = _string_value(values, 'street')
        self.city = _string_value(values, 'city')
        self.state = _string_value(values, 'state')
        self.postal_code = _string_value(values, 'postalCode')
        self.country = _string_value(values, 'country')
        self.email = _string_value(values, 'email')
        self.telephone = _string_value(values, 'telephone')
        self.telephone_ext = _string_value(values, 'telephoneExt')
        self.fax = _string_value(values, 'fax')
        self.fax_ext = _string_value(values, 'faxExt')
        self.raw_text = _string_value(values, 'rawText')

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return isinstance(other, Contact) and \
               self.name == other.name and \
               self.organization == other.organization and \
               self.street == other.street and \
               self.city == other.city and \
               self.state == other.state and \
               self.postal_code == other.postal_code and \
               self.country == other.country and \
               self.email == other.email and \
               self.telephone == other.telephone and \
               self.telephone_ext == other.telephone_ext and \
               self.fax == other.fax and \
               self.fax_ext == other.fax_ext and \
               self.raw_text == other.raw_text


# WhoisRecord is a whois record returned by the API
class WhoisRecord:
    domain_name: str
    domain_type: str
    created_date_iso8601: datetime.datetime or None
    updated_date_iso8601: datetime.datetime or None
    expires_date_iso8601: datetime.datetime or None
    created_date_raw: str
    updated_date_raw: str
    expires_date_raw: str
    audit: Audit or None
    name_servers: list
    whois_server: str
    registrar_name: str
    status: list
    clean_text: str
    raw_text: str
    registrant_contact: Contact or None
    administrative_contact: Contact or None
    technical_contact: Contact or None
    billing_contact: Contact or None
    zone_contact: Contact or None

    def __init__(self, values=None):
        self.domain_name = ''
        self.domain_type = ''
        self.created_date_iso8601 = None
        self.updated_date_iso8601 = None
        self.expires_date_iso8601 = None
        self.created_date_raw = ''
        self.updated_date_raw = ''
        self.expires_date_raw = ''
        self.audit = ''
        self.name_servers = []
        self.whois_server = ''
        self.registrar_name = ''
        self.status = []
        self.clean_text = ''
        self.raw_text = ''
        self.registrant_contact = None
        self.administrative_contact = None
        self.technical_contact = None
        self.billing_contact = None
        self.zone_contact = None

        if values is None:
            return

        self.domain_name = _string_value(values, 'domainName')
        self.domain_type = _string_value(values, 'domainType')
        self.created_date_iso8601 = _datetime_value(values, 'createdDateISO8601')
        self.updated_date_iso8601 = _datetime_value(values, 'updatedDateISO8601')
        self.expires_date_iso8601 = _datetime_value(values, 'expiresDateISO8601')
        self.created_date_raw = _string_value(values, 'createdDateRaw')
        self.updated_date_raw = _string_value(values, 'updatedDateRaw')
        self.expires_date_raw = _string_value(values, 'expiresDateRaw')
        if 'audit' in values:
            self.audit = Audit(values['audit'])
        self.name_servers = _string_list_value(values, 'nameServers')
        self.whois_server = _string_value(values, 'whoisServer')
        self.registrar_name = _string_value(values, 'registrarName')
        self.status = _string_list_value(values, 'status')
        self.clean_text = _string_value(values, 'cleanText')
        self.raw_text = _string_value(values, 'rawText')
        if 'registrantContact' in values:
            self.registrant_contact = Contact(values['registrantContact'])
        if 'administrativeContact' in values:
            self.administrative_contact = Contact(values['administrativeContact'])
        if 'technicalContact' in values:
            self.technical_contact = Contact(values['technicalContact'])
        if 'billingContact' in values:
            self.billing_contact = Contact(values['billingContact'])
        if 'zoneContact' in values:
            self.zone_contact = Contact(values['zoneContact'])

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return isinstance(other, WhoisRecord) and \
               self.domain_name == other.domain_name and \
               self.domain_type == other.domain_type and \
               self.created_date_iso8601 == other.created_date_iso8601 and \
               self.updated_date_iso8601 == other.updated_date_iso8601 and \
               self.expires_date_iso8601 == other.expires_date_iso8601 and \
               self.created_date_raw == other.created_date_raw and \
               self.updated_date_raw == other.updated_date_raw and \
               self.expires_date_raw == other.expires_date_raw and \
               self.audit == other.audit and \
               self.name_servers == other.name_servers and \
               self.whois_server == other.whois_server and \
               self.registrar_name == other.registrar_name and \
               self.status == other.status and \
               self.clean_text == other.clean_text and \
               self.raw_text == other.raw_text and \
               self.registrant_contact == other.registrant_contact and \
               self.administrative_contact == other.administrative_contact and \
               self.technical_contact == other.technical_contact and \
               self.billing_contact == other.billing_contact and \
               self.zone_contact == other.zone_contact


class ErrorMessage(Exception):
    code: int
    message: str

    def __init__(self, values=None):
        self.code = 0
        self.message = ''

        if values is None:
            return

        self.code = _integer_value(values, 'code')
        self.message = _string_value(values, 'messages')

    def __str__(self):
        return '[' + str(self.code) + '] ' + self.message
