"""
..
  Copyright 2020

.. moduleauthor:: Jan Piotr Buchmann <jpb@members.fsf.org>
"""

import sys
from typing import Iterable, List, Type

import ncbitaxonomist.model.taxon
import ncbitaxonomist.payload.payload


class NamePayload(ncbitaxonomist.payload.payload.Payload):
  """
  Implements a name payload for taxonomist queries using names.
  """

  class Update(ncbitaxonomist.payload.payload.Payload.Update):

    def __init__(self, processed:bool=False, value:str=None):
      super().__init__(processed, value)

  def __init__(self, args:Iterable[str]=None, parse:bool=True):
    super().__init__('name', args, parse)

  def parse_args(self, args:Iterable[str]):
    """Parses expected name arguments"""
    while args:
      for i in filter(bool, [x.strip() for x in args.pop().split(',') if x]):
        self.data[str(i)] = []
        self.data[str(i).lower()] = []

  def parse_stdin(self):
    """Reads standard input expecting names.Expecting one name per line or
    comma delimited names."""
    for i in sys.stdin:
      for j in filter(bool, [x.strip() for x in i.strip().split(',') if x]):
        self.data[str(j).lower()] = []

  def process(self, model:Type[ncbitaxonomist.model.taxon.Taxon], result:List=None):
    for i in model.get_names():
      if i in self.data and result is not None:
        self.data[i] += result
        return NamePayload.Update(True, i)
      if i.lower() in self.data and result is not None:
        self.data[i] += result
        return NamePayload.Update(True, i)
      if i in self.data:
        self.data[i].append(model)
        return NamePayload.Update(True, i)
    return NamePayload.Update()

  def as_list(self)->List[str]:
    """Gets the requested names  as list."""
    if self.data:
      return list(self.data)
    return []

  def is_processed(self, name):
    """Tests if the name has been processed."""
    if not self.data.get(str(name)):
      return False
    return True

  def get_data(self, name):
    return self.data.get(str(name))

  def remove(self, name):
    """Removes name from payload."""
    if self.data.get(str(name)):
      return self.data.pop(str(name))
    return None

  def update_from_cache(self, cache:Type[ncbitaxonomist.cache.cache.Cache]):
    if cache.names.is_empty():
      return
    for i in self.as_list():
      if cache.names.incache(name=i):
        self.data.pop(i)
