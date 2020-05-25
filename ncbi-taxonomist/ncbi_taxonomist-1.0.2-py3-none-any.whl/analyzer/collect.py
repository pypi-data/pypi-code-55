"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import json
from typing import Type


import entrezpy.base.analyzer

from ncbitaxonomist.convert import ncbitaxon
import ncbitaxonomist.cache.cache
import ncbitaxonomist.query.collect.collect
import ncbitaxonomist.entrezresult.taxonomy
import ncbitaxonomist.parser.ncbi.taxonomy


class CollectAnalyzer(entrezpy.base.analyzer.EutilsAnalyzer):

  taxa = {}
  cache = ncbitaxonomist.cache.cache.Cache()

  def __init__(self, query:Type[ncbitaxonomist.query.collect.collect.CollectQuery],
              converter:Type[ncbitaxon.NcbiTaxonConverter]):
    super().__init__()
    self.query = query
    self.converter = converter
    self.taxonomy_parser = ncbitaxonomist.parser.ncbi.taxonomy.TaxoXmlParser(CollectAnalyzer.taxa)

  def init_result(self, response, request:object)->bool:
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
      self.result.add_taxon(m)
      self.query.collect(m)
      CollectAnalyzer.cache.taxa.cache(m)
