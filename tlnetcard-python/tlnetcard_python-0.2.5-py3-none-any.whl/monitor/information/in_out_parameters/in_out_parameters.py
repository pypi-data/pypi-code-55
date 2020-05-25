# in_out_parameters.py
# Ethan Guthrie
# DATE TBD
""" Allows UPS input and output power levels to be read. """

# Required internal classes/functions.
from tlnetcard_python.login import Login

class InOutParameters:
    """ Class for the InOutParameters object. """
    def __init__(self, login_object: Login) -> None:
        """ Initializes the InOutParameters object. """
