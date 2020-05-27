"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Type


import ncbitaxonomist.ncbitaxonomist
import ncbitaxonomist.utils
from ncbitaxonomist.convert import ncbitaxon
import ncbitaxonomist.query.entrez
import ncbitaxonomist.payload.name
import ncbitaxonomist.payload.taxid
import ncbitaxonomist.analyzer.collect
import ncbitaxonomist.query.collect.name
import ncbitaxonomist.query.collect.taxid



class Collector:
  """Implements remote collection of taxa from Entrez."""

  def __init__(self, taxonomist:Type[ncbitaxonomist.ncbitaxonomist.NcbiTaxonomist]):
    self.logger = ncbitaxonomist.log.cmdlogger.CmdLogger('collect', cls=Collector, verbosity=taxonomist.verbosity)
    self.email = taxonomist.email
    self.cache = taxonomist.cache

  def collect(self, taxids:Type[ncbitaxonomist.payload.taxid.TaxidPayload],
              names:Type[ncbitaxonomist.payload.name.NamePayload]):
    """Collect given names and/or taxids from Entrez"""
    if names.has_data():
      self.logger.log(names, 'entrez')
      self.cache.cache_payload(self.collect_names(names, ncbitaxon.NcbiTaxonConverter()))
      self.cache.cache_payload(names)

    if taxids.has_data():
      self.logger.log(taxids, 'entrez')
      self.collect_taxids(taxids, ncbitaxon.NcbiTaxonConverter())
      self.cache.cache_payload(taxids)

    if taxids.has_data():
      self.logger.log_failed(taxids)
    if names.has_data():
      self.logger.log_failed(names)

  def collect_names(self, names:Type[ncbitaxonomist.payload.name.NamePayload],
                    converter:Type[ncbitaxon.NcbiTaxonConverter])->Type[ncbitaxonomist.payload.name.NamePayload]:
    """Collect names  from Entrez"""
    ncq = ncbitaxonomist.query.collect.name.NameCollectQuery(names)
    etq = ncbitaxonomist.query.entrez.EntrezTaxonomyQuery(self.email)
    etq.query_names(names.as_list(), ncbitaxonomist.analyzer.collect.CollectAnalyzer(ncq, converter))
    return ncq.payload

  def collect_taxids(self, taxids:Type[ncbitaxonomist.payload.taxid.TaxidPayload],
                     converter:Type[ncbitaxon.NcbiTaxonConverter])->Type[ncbitaxonomist.payload.taxid.TaxidPayload]:
    """Collect taxids  from Entrez"""
    tcq = ncbitaxonomist.query.collect.taxid.TaxidCollectQuery(taxids)
    etq = ncbitaxonomist.query.entrez.EntrezTaxonomyQuery(self.email)
    etq.query_taxids(taxids.as_list(), ncbitaxonomist.analyzer.collect.CollectAnalyzer(tcq, converter))
    return tcq.payload
