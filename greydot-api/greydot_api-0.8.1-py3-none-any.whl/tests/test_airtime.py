from sms import parse_xml_response
from airtime import SAMPLE


def test_airtime():
    print(parse_xml_response(SAMPLE))
