"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Type


import ncbitaxonomist.cache.cache
import ncbitaxonomist.db.dbimporter
import ncbitaxonomist.db.dbmanager

class NcbiTaxonomist:
  """
  Setup taxonomist run. Instantiate the cache, connect to a local database
  and store verbosity.
  """

  cache = ncbitaxonomist.cache.cache.Cache()

  def __init__(self, dbpath:str=None, email:str=None, verbosity:int=None):
    """Ctor to setup local database and create logger"""
    self.email:str = email
    self.db:Type[ncbitaxonomist.db.dbmanager.TaxonomyDb] = None
    if dbpath:
      self.db = ncbitaxonomist.db.dbmanager.TaxonomyDb(dbpath)
    self.verbosity = verbosity

  def import_to_db(self, out_attrib:str):
    """Import data to local taxonomy database. Attribute names can be passed to
      filter them for piped processing."""
    ncbitaxonomist.db.dbimporter.import_stdin(self.db, out_attrib)
