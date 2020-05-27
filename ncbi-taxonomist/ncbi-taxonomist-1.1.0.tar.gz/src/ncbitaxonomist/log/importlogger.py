"""
..
  Copyright 2020

.. moduleauthor:: Jan Piotr Buchmann <jpb@members.fsf.org>
"""

import ncbitaxonomist.log.logger

class ImportLogger(ncbitaxonomist.log.logger.TaxonomistLogger):

  def __init__(self, name, verbosity:int=0):
    super().__init__(name=name, verbosity=verbosity)

  def log_data(self, operation, db, msg):
    if msg is not None:
      return [operation, db, msg]
    return [operation, db]

  def log(self, operation, db, msg:str=None):
    self.logger.info(self.logfmt(self.log_data(operation, db, msg)))
    #self.logger.debug(self.sep.join([str(x) for x in data+pload.as_list()]))
    #self.logger.error(self.sep.join([str(x) for x in data+[msg]]))
