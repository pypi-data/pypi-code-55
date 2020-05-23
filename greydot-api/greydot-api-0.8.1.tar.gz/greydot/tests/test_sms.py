from sms import parse_xml_response
from sms import SAMPLE


def test_sms():
    print(parse_xml_response(SAMPLE))
