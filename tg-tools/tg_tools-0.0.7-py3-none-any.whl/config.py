from configparser import ConfigParser


class Config:
    """
    This class handles configuration files.
    As default procedure you can simply add a config.ini file to your source root
    an call the get method of this class, e.g.:
    Config().get('section', 'parameter')
    Config('other-filename.ini').get('section', 'parameter')
    """

    def __init__(self, filename='config.ini'):
        """
        Initializes the config class with creating the parser.

        :param filename: add your config file name here, default: config.ini
        """
        self.parser = ConfigParser()
        self.parser.read(filename)

    def get(self, section, param):
        """
        Simply get any parameter within a given section.

        :param section: the config section of your ini file
        :param param: the parameter you want to get
        :return: parameter value as string
        """
        return self.parser.get(section, param)
