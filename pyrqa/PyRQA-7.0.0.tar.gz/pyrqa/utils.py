#!/usr/bin/env python

"""
Collection of utilities.
"""

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2020 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"


class SettableSettings(object):
    """
    Base settings.

    :ivar settings: Recurrence analysis settings.
    """
    def __init__(self,
                 settings):
        self.settings = settings


class SettableMatrixRuntimes(object):
    """
    Base matrix runtimes.

    :ivar matrix_runtimes: Computing runtimes.
    """
    def __init__(self,
                 matrix_runtimes):
        self.matrix_runtimes = matrix_runtimes


class Verbose(object):
    """
    Base verbose.

    :ivar verbose: Boolean value indicating the verbosity of print outs.
    """
    def __init__(self, verbose):
        self.verbose = verbose

    def print_out(self, obj):
        """
        Print string if verbose is true.
        """

        if self.verbose:
            print(obj)
