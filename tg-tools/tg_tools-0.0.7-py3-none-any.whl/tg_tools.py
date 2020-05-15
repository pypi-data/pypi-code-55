from configparser import ConfigParser
from flask_pymongo import PyMongo


"""
Config Helper Class
"""


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
        self.parser.read(filename if filename else 'config.ini')

    def get(self, section, param):
        """
        Simply get any parameter within a given section.

        :param section: the config section of your ini file
        :param param: the parameter you want to get
        :return: parameter value as string
        """
        return self.parser.get(section, param)


def set_or_read_config(object_value, section, parameter, config_file):
    """
    Reads the config if no object value is given

    :param object_value:
    :param section:
    :param parameter:
    :param config_file:
    :return: returns the value either from parameter or from config file
    """
    return object_value if object_value else Config(config_file).get(section, parameter)


"""
FlaskPyMongo Helper Class
"""


class FlaskMongoDb:
    """
    This class handles MongoDb access in an easy way.
    Simply initialize your instance with Flask App, Service name which uses the DB and DB name, e.g.:
    mongo = FlaskMongoDb(app, 'seminar', 'tg_training')
    mongo.insert_many(data)
    """

    def __init__(self, app, container: str = None, port: str = '27017', database: str = None, collection: str = None, config_file = 'config.ini'):
        """
        Initialize DB connection for given service

        :param app: Flask app
        :param container: Container name of the MongoDB container
        :param port: Port of MongoDB, default '27017'
        :param database: Database name
        :param collection: Collection name
        :param config_file: Config file if different to standard (config.ini)
        """

        # Check if parameter is set or read in config
        section = 'DB'
        self.container = set_or_read_config(container, section, 'container', config_file)
        self.port = set_or_read_config(port, section, 'port', config_file)
        self.database = set_or_read_config(database, section, 'database', config_file)
        self.collection = set_or_read_config(collection, section, 'collection', config_file)

        app.config['MONGO_URI'] = 'mongodb://' + self.container + ':' + self.port + '/' + self.database
        self.mongo = PyMongo(app)
        self.db = self.mongo.db

    def insert(self, data, collection: str = None):
        """
        Inserts one new object to a specified collection

        :param data: a json object
        :param collection: collection to which the object shall be stored
        """
        col = collection if collection else self.collection
        try:
            self.db[col].insert(data)
        except Exception as e:
            raise e

    def insert_many(self, data, replace=False, collection: str = None):
        """
        Inserts a new object to a specified collection

        :param data: one of [seminar, customer, participant] object
        :param replace: replace old data? (true) or add new data (false)
        :param collection: collection to which the data shall be stored
        """
        col = collection if collection else self.collection
        try:
            if replace:
                self.db[col].drop()

            self.db[col].insert_many(data)

        except Exception as e:
            raise e

    def find(self, search_conditions: dict = None, collection: str = None):
        """
        Searches a set of results according to given search conditions.

        :param search_conditions: mongodb search conditions as dict
        :param collection: to overwrite the used collection
        :return: returns a result cursor from mongodb
        """
        col = collection if collection else self.collection

        return self.db[col].find(search_conditions)
