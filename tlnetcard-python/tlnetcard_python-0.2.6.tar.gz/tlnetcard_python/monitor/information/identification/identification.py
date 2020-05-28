# identification.py
# Ethan Guthrie
# DATE TBD
""" Allows UPS identifying information to be read. """

# Required internal classes/functions.
from tlnetcard_python.login import Login

class Identification:
    """ Class for the Identification object. """
    def __init__(self, login_object: Login) -> None:
        """ Initializes the Identification object. """
