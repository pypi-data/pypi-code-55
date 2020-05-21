import numpy as np

from ..datetime.Date import Date
from .DataParserUtils import _decode_xml_value_element, _parse_covariance

covariance_keys = [
    ["CX_X"],
    ["CY_X", "CY_Y"],
    ["CZ_X", "CZ_Y", "CZ_Z"],
    ["CX_DOT_X", "CX_DOT_Y", "CX_DOT_Z", "CX_DOT_X_DOT"],
    ["CY_DOT_X", "CY_DOT_Y", "CY_DOT_Z", "CY_DOT_X_DOT", "CY_DOT_Y_DOT"],
    [
        "CZ_DOT_X",
        "CZ_DOT_Y",
        "CZ_DOT_Z",
        "CZ_DOT_X_DOT",
        "CZ_DOT_Y_DOT",
        "CZ_DOT_Z_DOT",
    ],
]


class CommonOrbitData:
    def __init__(self):
        pass

    def _parse_spacecraft_parameters(self, object_name, element):
        self.spacecraft_parameters = self._parse_section_xml(element)

    def _parse_covariance_xml(self, object_name, element):
        if object_name not in self.covariance.keys():
            self.covariance[object_name] = {}
            self.covariance[object_name]["matrix"] = []

        self.covariance[object_name]["COV_REF_FRAME"] = element.find(
            "COV_REF_FRAME"
        ).text

        epoch = None
        epoch_element = element.find("EPOCH")
        if epoch_element:
            epoch = Date(epoch_element.text)
        covariance = {"EPOCH": epoch, "matrix": []}
        mat = np.array([[0.0] * 6] * 6)
        for row in range(0, 6):
            for col in range(0, row + 1):
                key = covariance_keys[row][col]
                mat[row][col] = _decode_xml_value_element(element, key, None)
                mat[col][row] = mat[row][col]
        covariance["matrix"] = mat
        self.covariance[object_name]["matrix"].append(covariance)

    def _parse_covariance_kvn(self, object_name, data):
        if object_name not in self.covariance.keys():
            self.covariance[object_name] = {}
            self.covariance[object_name]["matrix"] = []

        self.covariance[object_name]["COV_REF_FRAME"] = data["COV_REF_FRAME"]
        covariance = {"EPOCH": None, "matrix": _parse_covariance(data, covariance_keys)}
        self.covariance[object_name]["matrix"].append(covariance)
