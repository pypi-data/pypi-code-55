class CommonMetadataParser:
    def __init__(self, metadata_keys=None):
        self.metadata_keys = metadata_keys
        self.dict_metadata = {}
        pass

    def decode_metadata_xml(self, tree):
        """Decode the XML metadata"""
        dict_metadata = {}
        for element in tree:
            dict_metadata[element.tag] = element.text
        return dict_metadata

    def decode_metadata_kvn(self, metadata):
        """Decode the KVN metadata"""
        for line in metadata:
            if "COMMENT" not in line:
                key_value = line.split("=")
                key = key_value[0].rstrip()
                value = key_value[1].strip()
                self.dict_metadata[key] = value
        for key in self.metadata_keys:
            if not self.dict_metadata[key]:
                raise ValueError("Missing key: ", key)
        return self.dict_metadata
