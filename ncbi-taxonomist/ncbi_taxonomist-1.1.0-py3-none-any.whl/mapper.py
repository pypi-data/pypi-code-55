"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import sys
from typing import Dict, Type


import ncbitaxonomist.ncbitaxonomist
import ncbitaxonomist.analyzer.accession
import ncbitaxonomist.analyzer.mapping
import ncbitaxonomist.convert.taxadb
import ncbitaxonomist.convert.accessiondb
import ncbitaxonomist.db.dbmanager
import ncbitaxonomist.log.cmdlogger
import ncbitaxonomist.payload.accession
import ncbitaxonomist.payload.name
import ncbitaxonomist.payload.taxid
import ncbitaxonomist.query.entrez
import ncbitaxonomist.query.map.taxid
import ncbitaxonomist.query.map.name
import ncbitaxonomist.query.map.accession
import ncbitaxonomist.utils

from ncbitaxonomist.convert import ncbitaxon
from ncbitaxonomist.convert import ncbiaccession

class Mapper:
  """Implements mapping commands for taxids, names, and accessions."""

  def __init__(self, taxonomist:Type[ncbitaxonomist.ncbitaxonomist.NcbiTaxonomist]):
    self.db = taxonomist.db
    self.email = taxonomist.email
    self.cache = taxonomist.cache
    self.logger = ncbitaxonomist.log.cmdlogger.CmdLogger('map', cls=Mapper, verbosity=taxonomist.verbosity)
    if taxonomist.db is not None:
      self.logger.add_db(taxonomist.db.path)

  def map(self, taxids:Type[ncbitaxonomist.payload.taxid.TaxidPayload],
          names:Type[ncbitaxonomist.payload.name.NamePayload],
          accessions:Type[ncbitaxonomist.payload.accession.AccessionPayload],
          entrezdb:str, remote:bool=False):

    if self.db and names.has_data():
      self.logger.log(names)
      self.cache.cache_payload(self.map_names(names))

    self.map_taxa_from_cache(taxids)
    if self.db and taxids.has_data():
      self.logger.log(taxids)
      self.cache.cache_payload(self.map_taxids(taxids))

    self.map_taxa_from_cache(names)
    if remote and names.has_data():
      self.logger.log(names, 'entrez')
      self.cache.cache_payload(self.map_names_remote(names))

    self.map_taxa_from_cache(taxids)
    if remote and taxids.has_data():
      self.logger.log(taxids, 'entrez')
      self.cache.cache_payload(self.map_taxids_remote(taxids))

    if self.db and accessions.has_data():
      self.logger.log(accessions)
      self.cache.cache_payload(self.map_accessions(accessions, entrezdb))

    self.map_taxa_from_cache(accessions)
    if remote and accessions.has_data():
      self.logger.log(accessions, 'entrez')
      self.cache.cache_payload(self.map_accessions_remote(accessions, entrezdb))
      self.map_taxa_from_cache(accessions)

    if taxids.has_data():
      self.logger.log_failed(taxids)
    if names.has_data():
      self.logger.log_failed(names)
    if accessions.has_data():
      self.logger.log_failed(accessions)

  def map_names(self, names:Type[ncbitaxonomist.payload.name.NamePayload]):
    nmq = ncbitaxonomist.query.map.name.NameMapQuery(names)
    self.db.get_taxa_by_name(names.as_list(), ncbitaxonomist.convert.taxadb.TaxaDbConverter(), nmq)
    return names

  def map_names_remote(self, names:Type[ncbitaxonomist.payload.name.NamePayload])->Type[ncbitaxonomist.payload.payload.Payload]:
    nmq = ncbitaxonomist.query.map.name.NameMapQuery(names)
    etq = ncbitaxonomist.query.entrez.EntrezTaxonomyQuery(self.email)
    etq.query_names(names.as_list(),
                    ncbitaxonomist.analyzer.mapping.MapAnalyzer(nmq, ncbitaxon.NcbiTaxonConverter()))
    return names

  def map_taxids(self, taxids:Type[ncbitaxonomist.payload.taxid.TaxidPayload]):
    tmq = ncbitaxonomist.query.map.taxid.TaxidMapQuery(taxids)
    self.db.get_taxa_by_taxids(taxids.as_list(), ncbitaxonomist.convert.taxadb.TaxaDbConverter(), tmq)
    return taxids

  def map_taxids_remote(self, taxids:Type[ncbitaxonomist.payload.taxid.TaxidPayload]):
    tmq = ncbitaxonomist.query.map.taxid.TaxidMapQuery(taxids)
    etq = ncbitaxonomist.query.entrez.EntrezTaxonomyQuery(self.email)
    etq.query_taxids(taxids.as_list(),
                     ncbitaxonomist.analyzer.mapping.MapAnalyzer(tmq, ncbitaxon.NcbiTaxonConverter()))
    return taxids

  def map_accessions(self, accessions:Type[ncbitaxonomist.payload.accession.AccessionPayload], entrezdb:str)->Dict:
    amq = ncbitaxonomist.query.map.accession.AccessionMapQuery(accessions)
    self.db.get_taxa_by_accessions(accessions.as_list(),entrezdb,
                                   ncbitaxonomist.convert.accessiondb.DbAccessionConverter(),
                                   amq)
    return accessions

  def map_accessions_remote(self, accessions:Type[ncbitaxonomist.payload.accession.AccessionPayload],
                            entrezdb:str)->Type[ncbitaxonomist.payload.accession.AccessionPayload]:
    amq = ncbitaxonomist.query.map.accession.AccessionMapQuery(accessions)
    etq = ncbitaxonomist.query.entrez.EntrezTaxonomyQuery(self.email)
    etq.query_accessions(
      accessions.as_list(), entrezdb,
      ncbitaxonomist.analyzer.accession.AccessionMapAnalyzer(amq, ncbiaccession.NcbiAccessionConverter()))
    return accessions

  def map_taxa_from_cache(self, pload:Type[ncbitaxonomist.payload.payload.Payload]):
    """
    Map queries from cache. Not the best loop but don't like to loop over
      different casts at once.

      .. note Unify cache retrieval. Along the lines of get_cache(cast).retrieve()
    """
    if not pload.has_data():
      return
    qry = None
    if pload.cast == 'taxid':
      qry = ncbitaxonomist.query.map.taxid.TaxidMapQuery(pload)
    elif pload.cast == 'name':
      qry = ncbitaxonomist.query.map.name.NameMapQuery(pload)
    elif pload.cast == 'acc':
      qry = ncbitaxonomist.query.map.accession.AccessionMapQuery(pload)
    else:
      sys.exit("Unknown payload cast: {}.Abort".format(pload.cast))
    self.logger.log(pload, 'cache')
    if pload.cast == 'taxid':
      for i in pload.as_list():
        if self.cache.taxid_is_cached(i):
          qry.map_query(self.cache.get_taxon(i))
          if pload.is_processed(i):
              pload.remove(i)
    elif pload.cast == 'acc':
      for i in pload.as_list():
        if self.cache.accession_is_cached(i):
          qry.map_query(self.cache.get_accession(i))
          if pload.is_processed(i):
              pload.remove(i)
    else:
      for i in pload.as_list():
        if self.cache.name_is_cached(i):
          qry.map_query(self.cache.get_taxon_by_name(i))
          if pload.is_processed(i):
            pload.remove(i)
