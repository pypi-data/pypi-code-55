import json


class Fixture:
    """ Fixture handler object """

    json_converter = json

    def __init__(self):
        self.__fixture_full_path = None
        self.__fixture_data = None
        self.__fixture_extension = None

    @classmethod
    def build_(cls, full_path, extension):
        """
            Method should build fixture
            with path
            :path - str representation of path
            :rtype - instance of self
        """
        instance = cls()
        instance.set_path(full_path)
        instance.set_extension(extension)
        instance.fetch()
        return instance

    @property
    def extension(self):
        return self.__fixture_extension

    def set_path(self, path):
        """
            Method should set path for fetch fixture
            :path - str representation of path
            :rtype - instance of self
        """

        self.__fixture_full_path = path
        return self

    def set_extension(self, extension):
        """
            Method should set extension
            :extension - str with file extensions
            :rtype - instance of self
        """
        self.__fixture_extension = extension
        return self

    def to_dict(self):
        """
            Method should convert json fixture to dict
        """
        self.should_be_json()
        return self.json_converter.loads(self.__fixture_data)

    def should_be_json(self):
        assert self.extension == 'json'

    # connect validation mixin
    def fetch(self):
        """
            Method should fetch fixture
            rtype - self
        """
        try:
            with open(self.__fixture_full_path, 'r') as file:
                self.__fixture_data = file.read()
                file.close()

        except Exception as e:
            raise Exception("File not found")
