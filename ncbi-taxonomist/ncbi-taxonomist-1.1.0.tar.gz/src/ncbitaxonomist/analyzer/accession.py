"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import json
from typing import Type


import entrezpy.base.analyzer


import ncbitaxonomist.query.map.map
import ncbitaxonomist.entrezresult.accession
import ncbitaxonomist.convert.ncbiaccession

class AccessionMapAnalyzer(entrezpy.base.analyzer.EutilsAnalyzer):

  def __init__(self, query:Type[ncbitaxonomist.query.map.map.MapQuery],
               converter:Type[ncbitaxonomist.convert.ncbiaccession.NcbiAccessionConverter]):
    super().__init__()
    self.query = query
    self.converter = converter

  def init_result(self, response:dict, request:object) -> bool:
    if not self.result:
      self.result = ncbitaxonomist.entrezresult.accession.NcbiAccessionResult(request)
      return True
    return False

  def analyze_error(self, response:dict, request:object):
    print (json.dumps({__name__:{'Response-Error':{
                                   'request-dump' : request.dump_internals(),
                                   'error' : response}}}))

  def analyze_result(self, response:dict, request:object):
    self.init_result(request, request)
    uids = response['result'].pop('uids', None)
    if uids:
      for i in uids:
        model = self.converter.convert_to_model(response['result'].pop(i), request.db)
        if model:
          self.result.add_accession(model)
          self.query.map_query(model)
