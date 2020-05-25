"""
..
  Copyright 2020

.. moduleauthor:: Jan Piotr Buchmann <jpb@members.fsf.org>
"""


import sys
import logging


logger = logging.getLogger('ncbi-taxonomist')
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s::%(name)s:%(message)s'))
logger.addHandler(ch)

def resolve_nspace(cls, rootlogger='ncbi-taxonomist'):
  """Resolves proper namespace for logger"""
  return "{}.{}.{}".format(rootlogger, cls.__module__, cls.__qualname__)

class TaxonomistLogger:

  def __init__(self, cls=None, name=None, verbosity:int=0):
    if cls is None and name is None:
      sys.exit("No required class or module name given. Abort.")
    self.logger = None
    self.db = None
    self.sep = ':'
    if cls is not None:
      self.logger = logging.getLogger(resolve_nspace(cls))
    else:
      self.logger = logging.getLogger(name)
    self.set_level(verbosity)

  def add_db(self, db):
    self.db = db

  def logfmt(self, data):
    return self.sep.join([str(x) for x in data])

  def set_level(self, verbosity):
    if verbosity == 0:
      self.logger.removeHandler(ch)
    elif verbosity == 1:
      self.logger.setLevel(20)
      ch.setLevel(20)
    else:
      self.logger.setLevel(10)
      ch.setLevel(10)
