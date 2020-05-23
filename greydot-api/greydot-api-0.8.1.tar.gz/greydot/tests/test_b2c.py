from sms import parse_xml_response
from b2c import SAMPLE


def test_b2c():
    print(parse_xml_response(SAMPLE))
