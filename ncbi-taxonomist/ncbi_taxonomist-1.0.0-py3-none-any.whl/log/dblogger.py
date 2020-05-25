"""
..
  Copyright 2020

.. moduleauthor:: Jan Piotr Buchmann <jpb@members.fsf.org>
"""

import ncbitaxonomist.log.logger

class DbLogger(ncbitaxonomist.log.logger.TaxonomistLogger):

  def __init__(self, cls, verbosity:int=0):
    super().__init__(cls=cls, verbosity=verbosity)

  def info_data(self, status, msg=None):
    if msg is not None:
      return [self.db, status, msg]
    return [self.db, status]

  def dbg_data(self, status, conn):
    data = self.info_data(status)
    if conn is not None:
      data.append(conn)
    return data

  def logfmt(self, data):
    return self.sep.join([str(x) for x in data])

  def log(self, status, conn=None, msg=None):
    self.logger.info(self.logfmt(self.info_data(status, msg)))
    self.logger.debug(self.logfmt(self.dbg_data(status, conn)))
