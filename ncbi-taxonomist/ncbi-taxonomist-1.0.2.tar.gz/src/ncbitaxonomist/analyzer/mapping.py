"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import json
from typing import Type


import entrezpy.base.analyzer


import ncbitaxonomist.parser.ncbi.taxonomy
from ncbitaxonomist.convert import ncbitaxon
import ncbitaxonomist.entrezresult.taxonomy
import ncbitaxonomist.query.map.map


class MapAnalyzer(entrezpy.base.analyzer.EutilsAnalyzer):
  """
  Implements an entrezpy analyzer to parse taxonomy XML data from NCBI and runs
  the otbained taxa through a map query.
  """
  taxa = {}

  def __init__(self, query:Type[ncbitaxonomist.query.map.map.MapQuery],
               converter:Type[ncbitaxon.NcbiTaxonConverter]):
    super().__init__()
    self.query = query
    self.converter = converter
    self.taxonomy_parser = ncbitaxonomist.parser.ncbi.taxonomy.TaxoXmlParser(MapAnalyzer.taxa)

  def init_result(self, response, request:object) -> bool:
    if not self.result:
      self.result = ncbitaxonomist.entrezresult.taxonomy.NcbiTaxonomyResult(request)
      return True
    return False

  def analyze_error(self, response, request:object):
    print (json.dumps({__name__:{'Response-Error':{
                                   'request-dump' : request.dump_internals(),
                                   'error' : response.getvalue()}}}))

  def analyze_result(self, response, request:object):
    self.init_result(response, request)
    results = self.taxonomy_parser.parse(response)
    self.result.add_queries(results.queries)
    for i in results.taxa:
      m = self.converter.convert_to_model(results.taxa[i].attribute_dict())
      self.query.map_query(m)
