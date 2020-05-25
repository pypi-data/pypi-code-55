"""
..
  Copyright 2020

.. moduleauthor:: Jan Piotr Buchmann <jpb@members.fsf.org>
"""


from typing import List, Type


import ncbitaxonomist.log.logger
import ncbitaxonomist.payload.payload


class CmdLogger(ncbitaxonomist.log.logger.TaxonomistLogger):

  def __init__(self, cmd, cls, verbosity:int=0):
    super().__init__(cls=cls, verbosity=verbosity)
    self.cmd = cmd

  def log_data(self, pload:Type[ncbitaxonomist.payload.payload.Payload], src:str=None, msg:str=None)->List:
    if src is None:
      src = self.db
    if msg is None:
      return [self.cmd, pload.cast, pload.size(), src]
    return [self.cmd, pload.cast, msg, pload.size(), src]

  def log(self, pload, src:str=None, msg:str=None):
    self.logger.info(self.logfmt(self.log_data(pload, src, msg)))
    self.logger.debug(self.logfmt(self.log_data(pload, src, msg)+pload.as_list()))
    #self.logger.error(self.sep.join([str(x) for x in data+[msg]]))

  def log_failed(self, pload, src:str=None):
    self.logger.info(self.logfmt([self.cmd, pload.cast, 'failed',pload.as_list()]))

  def log_msg(self, msg):
    self.logger.info(self.logfmt([self.cmd, msg]))
