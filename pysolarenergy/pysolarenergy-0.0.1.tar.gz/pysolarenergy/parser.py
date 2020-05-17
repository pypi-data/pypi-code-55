"""Response Parser for SolarEnergy."""
import xmltodict
import json
from typing import Any


def parse_xml_to_json(data: Any) -> json:
    """Parse xml."""
    return json.loads(json.dumps(xmltodict.parse(data)))
