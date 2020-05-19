"""
    _    ____ ___   ____
   / \\  |  _ \\_ _| |  _ \\  ___   ___ ___
  / _ \\ | |_) | |  | | | |/ _ \\ / __/ __|
 / ___ \\|  __/| |  | |_| | (_) | (__\\__ \\
/_/   \\_\\_|  |___| |____/ \\___/ \\___|___/

Copyright &copy;2020 - Mad Penguin Consulting Limited
"""
from collections import UserDict
from typing import Optional
from .database import Database
from .types_ import Config


class Manager(UserDict):
    """
    Manager is a dictionary like object the holds references to all the databases currently
    registered with the running instance. If you only ever reference one database then
    technically you can skip this object and just use the Database object.
    """

    def __getitem__(self, name: str) -> Database:
        """
        Get a reference to an already open database

        name - the name of database

        Returns the Database object associated with the supplied name
        """
        if name not in self.data:
            self.data[name] = Database()
        return self.data[name]

    def database(self, name: str, path: Optional[str]=None, config: Optional[Config]=None) -> Database:
        """
        Open a database creating it if necessary

        name - an arbitrary name to reference the database by
        path - the path to the database files
        config - a dictionary containing configuration specifics for this database

        Returns a reference to an open Database
        """
        db = self.__getitem__(name)
        if config:
            db.configure(config)
        return db.open(path if path else name)
