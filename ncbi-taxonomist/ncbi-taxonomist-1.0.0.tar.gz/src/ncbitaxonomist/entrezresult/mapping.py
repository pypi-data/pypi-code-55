"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import entrezpy.base.result

class NcbiMappingResult(entrezpy.base.result.EutilsResult):

  def __init__(self, request):
    super().__init__(request.eutil, request.query_id, request.db)
    self.mappings = {}

  def size(self):
    return len(self.mappings)

  def get_link_parameter(self, reqnum=0):
    del reqnum #Unused
    print("{}: Entrez links not supported".format(__name__))

  def isEmpty(self):
    if not self.mappings:
      return True
    return False

  def dump(self):
    return {'db':self.db, 'size' : self.size(), 'function' : self.function,
            'mapping': list(self.mappings)}

  def add_mapping(self, mapping):
    self.mappings.update(mapping)
