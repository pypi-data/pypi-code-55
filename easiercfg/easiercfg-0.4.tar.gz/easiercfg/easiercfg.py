from configparser import RawConfigParser
import os
import sys


class Config(RawConfigParser):
    """
    Class for easy config file usage.
    """

    def __init__(self):
        """
        Initialize Class.
        """
        # Parameter
        self.filename = 'config.ini'
        # Call parent constructor
        super(Config, self).__init__()
        # Load Config-File
        self.__LoadConfig()

    def __LoadConfig(self):
        """
        Load Config-File.
        """
        self.read(os.path.join(sys.path[0], self.filename))

    def Show(self):
        """
        Print all key and value pairs.
        """
        config_dict = {}
        for element in self.sections():
            config_dict[element] = {}
            for name, value in self.items(element):
                print('{:15} = {}'.format(name, value))
                config_dict[element][name] = value

    def __setitem__(self, key, value):
        """
        Set value of key-value-pair.
        """
        self.Set(key, value)

    def Set(self, key, value, section="settings"):
        """
        Set value of key-value-pair.
        """
        self.set(section, key, value)
        self.__Save()

    def __getitem__(self, key):
        """
        Get corresponding value of key-value-pair.
        """
        return self.Get(key)

    def Get(self, key, section="settings"):
        """
        Get corresponding value of key-value-pair.
        """
        return self.get(section, key)

    def __Save(self, filename=""):
        """
        Save current config to file.
        """
        # If no filename is specified use the one defined in parameters.
        if filename == "":
            filename = self.filename
        # Write config to file
        with open(filename, 'w') as configfile:
            self.write(configfile)
