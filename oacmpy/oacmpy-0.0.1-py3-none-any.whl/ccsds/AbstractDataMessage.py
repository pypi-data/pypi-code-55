import re
import xml.etree.ElementTree as et
from abc import abstractmethod

from . import CommonMetadataParser as m
from . import enumerates, exceptions
from .DataParserUtils import _decode_kvn, _decode_xml_value


class AbstractDataMessage:
    """Class for loading Orbit Data Message: OPM, OMM, EOM"""

    def __init__(self, fmt):
        self.fmt = enumerates.FileFormat(fmt.upper())
        self.metadata_keys = ["OBJECT_NAME", "OBJECT_ID", "REF_FRAME", "CENTER_NAME"]
        self.sections = {}
        self.common_blocks = {}
        self.metadata_parser = m.CommonMetadataParser()
        self.ephemeris_state_key = None
        self.set_metadata_keys(self.metadata_keys)
        pass

    def set_xml_ephemeris_state_key(self, state_key):
        self.ephemeris_state_key = state_key

    def set_metadata_keys(self, keys):
        """Set the mandatory metadata keys"""
        self.metadata_keys = keys
        self.metadata_parser = m.CommonMetadataParser(self.metadata_keys)

    def set_common_blocks(self, blocks):
        """Declare all common blocks of the KVN or XML file"""
        self.common_blocks = blocks

    def set_segment_blocks(self, blocks):
        """Declare all segment blocks of the KVN or XML file, except METADATA and DATA"""
        self.sections = blocks

    def load_from_file(self, filename, fmt):
        """Load from file
        Args:
            filename (str): File name
            fmt (enum): enum from Enumerates.FileFormat, {"XML", "KVN"}"""
        with open(filename) as f:
            out = self.load_from_string(f.read(), fmt)
        return out

    def load_from_string(self, string, fmt):
        """
        Args:
            string (str): String containing the data message
            fmt (enum): enum from Enumerates.FileFormat, {"XML", "KVN"}
        """

        if fmt == enumerates.FileFormat.KVN:  # Key-Value Notation
            metadata, data = self._loads_kvn(string)
        elif fmt == enumerates.FileFormat.XML:  # XML
            metadata, data = self._loads_xml(string)
        else:  # pragma: no cover
            raise exceptions.CcsdsError("Unknown file format '{}'".format(fmt))

        return metadata, data

    @abstractmethod
    def _set_metadata(self, object_name, meta):
        """Set general file metadata"""
        self.metadata = meta

    @abstractmethod
    def _set_property(self, key, value):
        """Set general file property"""
        self.properties[key] = value

    def process_properties(self, line):
        key, value = _decode_kvn(line)
        self._set_property(key, value)

    @abstractmethod
    def _parse_state_vector_kvn(self, object_name, metadata, line):
        pass

    @abstractmethod
    def _parse_state_vector_xml(self, object_name, state_vector):
        """Decode the state vector"""
        pass

    @abstractmethod
    def _parse_section_xml(self, tree):
        """Decode the XML element of a section"""
        dict_data = {}
        for element in tree:
            dict_data[element.tag] = _decode_xml_value(element, None)
        return dict_data

    def _loads_xml(self, string):
        """Load XML file"""
        xml = et.fromstring(string.encode())

        idstr = xml.attrib.get("id")
        verstr = xml.attrib.get("version")
        self._set_property(idstr, verstr)

        body = xml.find("body")
        if body is None:
            raise exceptions.CcsdsError("Missing body in XML")

        for section_key, section_fcn in self.common_blocks.items():
            for state in body.iter(section_key):
                section_fcn(state)

        metadata = {}
        ephems = {}
        # try:
        for segment in body.iter("segment"):
            meta = self.metadata_parser.decode_metadata_xml(segment.find("metadata"))

            object_name = meta["OBJECT_NAME"]
            self._set_metadata(object_name, meta)

            for data in segment.iter("data"):
                sv = []
                if self.ephemeris_state_key:
                    for state in data.iter(self.ephemeris_state_key):
                        sv.append(self._parse_state_vector_xml(object_name, state))
                    ephems[object_name] = sv

                for section_key, section_fcn in self.sections.items():
                    for state in data.iter(section_key):
                        section_fcn(object_name, state)

        # except KeyError as e:
        #    raise CcsdsError("Missing mandatory parameter {}".format(e))

        return metadata, ephems

    def _loads_kvn(self, string):
        data = {}
        ephem = []
        lines = string.splitlines()
        metadata = {}
        in_metadata_block = False
        metadata_lines = []
        current_object = ""
        in_data_block = False
        current_block_name = ""
        block_data = []
        for line in lines:
            line = line.rstrip()
            if line:
                if line == "META_START":
                    in_metadata_block = True
                    metadata_lines = []
                    if in_data_block:
                        # OEM data are not in a block, so we have to assume it is state vector
                        data[current_object]["DATA"] = ephem
                        ephem = []
                        in_data_block = False
                elif line == "META_STOP":
                    data = self.metadata_parser.decode_metadata_kvn(metadata_lines)
                    current_object = data["OBJECT_NAME"]
                    metadata[current_object] = data
                    in_metadata_block = False

                    if current_object not in data:
                        data[current_object] = {}
                elif in_metadata_block:
                    metadata_lines.append(line)
                elif "_START" in line:
                    if in_data_block:
                        # OEM data are not in a block, so we have to assume it is state vector
                        data[current_object]["DATA"] = self._parse_state_vector_kvn(
                            current_object, metadata[current_object], block_data
                        )
                        in_data_block = False

                    current_block_name = line[0 : line.index("_START")]
                    fcn = self.sections[current_block_name]
                    if fcn is None:
                        raise ValueError(
                            "Not driver for reading data of block ", current_block_name
                        )
                    in_data_block = True
                    block_data = []
                elif line == current_block_name + "_STOP":
                    in_data_block = False
                    fcn = self.sections[current_block_name]
                    block_data_dict = fcn(
                        current_object, metadata[current_object], block_data
                    )
                    data[current_object][current_block_name] = block_data_dict
                    current_block_name = ""
                elif in_data_block:
                    block_data.append(line)
                elif "COMMENT" in line:
                    # no use
                    pass
                elif line.find("=") >= 0:
                    self.process_properties(line)
                else:
                    # OEM data are not in a block, so we have to assume it is state vector
                    in_data_block = True
                    block_data.append(line)

        if in_data_block:
            # OEM data are not in a block, so we have to assume it is state vector
            data[current_object]["DATA"] = self._parse_state_vector_kvn(
                current_object, metadata[current_object], block_data
            )

        return metadata, data
