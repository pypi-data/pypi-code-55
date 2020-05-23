from sms import parse_xml_response
from signup import SAMPLE


def test_signup():
    print(parse_xml_response(SAMPLE))
