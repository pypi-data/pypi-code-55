# coding: utf-8
# Distributed under the terms of the MIT License.

""" The db module provides all the submodules that touch the database,
with functionality to connect, add or refine database objects, and observe
changes.

"""


__all__ = ['Spatula', 'DatabaseChanges', 'Refiner', 'make_connection_to_collection']
__author__ = 'Matthew Evans'
__maintainer__ = 'Matthew Evans'

from matador.db.connect import make_connection_to_collection
from matador.db.importer import Spatula
from matador.db.changes import DatabaseChanges
from matador.db.refine import Refiner
