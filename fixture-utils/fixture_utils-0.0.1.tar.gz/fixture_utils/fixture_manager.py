
from os import walk
from .fixture import Fixture
from .exceptions import FixtureNotFound


class FixtureManager:
    """
        Manager for get fixtures
        from fixtures folder
    """

    fixture_class = Fixture

    def __init__(self):
        self.__fixture_path = None
        self.__fixtures_map = dict()

    @classmethod
    def build_(cls, fixture_path):
        """
            Method should build
            fuxture manager with
            directories
            :root_fixture - root path fixture
            :fixture_path  - fixture path
        """
        instance = cls()
        instance.__fixture_path = fixture_path
        instance.autodiscover()
        return instance

    def autodiscover(self):
        """
            Method should get fixtures from folder
        """
        for root, dirs, files in walk(self.__fixture_path):

            for file in files:

                extension = self.__get_extension(file)
                file_name = self.__get_name(file)
                full_path = f"{root}/{file}"
                fixture_instance = self.fixture_class.build_(full_path, extension)

                self.__add_fixture_to_map(file_name, fixture_instance)

    def __add_fixture_to_map(self, file_name, fixture_instance):
        """
            Method should add fixture to map
            :fixture instance of self.fixture_class
            :rtype - instance of self
        """
        assert (
            isinstance(fixture_instance, self.fixture_class),
            f"Fixture should be {self.fixture_class}"
        )
        self.__fixtures_map.update({file_name: fixture_instance})
        return self

    def __get_extension(self, file_name):
        """
            Method should get extension from file name
            :file_name - string representation of file name
            :rtype - string with extension
        """
        return self.__dot_split(file_name)[1]

    def __get_name(self, file_name):
        """
            Method should get name without extension
            :file_name - string representation of name
            :rtype - string
        """
        return self.__dot_split(file_name)[0]

    def __dot_split(self, string):
        """
            Method should split string with dot
            :string - simple python string
            :rtype - list<str>
        """

        splitted_string = string.split(".")
        assert (
            len(splitted_string) == 2,
            f"File name should have only one dot, not {string}"
        )

        return splitted_string

    def __from_fixture_map(self, key):
        """
            Method should check if fixture key
            exist in map
            :key - string representation
            :rtype - bool value
        """
        return key in self.__fixtures_map

    def __getattr__(self, key):
        if self.__from_fixture_map(key):
            return self.__fixtures_map[key]

        attr = self.__dict__.get('key')
        if not attr:
            raise FixtureNotFound

        return attr
