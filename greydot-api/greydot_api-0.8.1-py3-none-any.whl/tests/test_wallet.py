from sms import parse_xml_response
from wallet import SAMPLE


def test_wallet():
    print(parse_xml_response(SAMPLE))
