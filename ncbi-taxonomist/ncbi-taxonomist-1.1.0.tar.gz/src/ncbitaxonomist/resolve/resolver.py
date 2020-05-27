"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import sys
from typing import Dict, Type


import ncbitaxonomist.analyzer.resolve
import ncbitaxonomist.cache.cache
import ncbitaxonomist.convert.taxadb
import ncbitaxonomist.convert.ncbitaxon
import ncbitaxonomist.log.cmdlogger
import ncbitaxonomist.model.accession
import ncbitaxonomist.model.taxon
import ncbitaxonomist.payload.accession
import ncbitaxonomist.payload.name
import ncbitaxonomist.payload.taxid
import ncbitaxonomist.payload.accessionmap
import ncbitaxonomist.query.entrez
import ncbitaxonomist.query.resolve.accession
import ncbitaxonomist.query.resolve.name
import ncbitaxonomist.query.resolve.taxid
import ncbitaxonomist.utils

class Resolver:
  """
    Resolve lineages for names and taxids. If a local database is given, it
    will be checked first, followed by checking Entrez remotely if requested.
    Lineages are JSON arrays. Queries are initially queried in cache before
    querying the local and/or remote sources. Because every query from a
    preceding lineage is already present cache should be faster.

    Resolving accessions requires a mapping step beforehand which results are
    read from STDIN by :class:`ncbitaxonomist.resolve.resolverResolver`.
  """

  def __init__(self, taxonomist):
    self.db = taxonomist.db
    self.email = taxonomist.email
    self.cache = taxonomist.cache
    self.logger = ncbitaxonomist.log.cmdlogger.CmdLogger(
      'resolve', cls=Resolver, verbosity=taxonomist.verbosity)
    if taxonomist.db is not None:
      self.logger.add_db(taxonomist.db.path)

  def resolve(self, taxids:Type[ncbitaxonomist.payload.taxid.TaxidPayload],
              names:Type[ncbitaxonomist.payload.name.NamePayload],
              mapping:bool=False, remote:bool=False):
    """Resolve individual payloads"""

    if mapping:
      accessions = ncbitaxonomist.payload.accessionmap.AccessionMap()
      if self.db:
        self.cache.cache_payload(self.resolve_accession_map(accessions))
      if remote and accessions.has_data():
        accessions = self.resolve_accession_map_remote(accessions)

    if not taxids.has_data() and not names.has_data():
      self.resolve_stdin()

    if self.db and names.has_data():
      self.cache.cache_payload(self.resolve_names(names))

    if self.db and taxids.has_data():
      self.cache.cache_payload(self.resolve_from_cache(taxids, names))
      if taxids.has_data():
        self.cache.cache_payload(self.resolve_taxids(taxids))

    if remote and names.has_data():
      self.cache.cache_payload(self.resolve_from_cache(taxids, names))
      if names.has_data():
        self.cache.cache_payload(self.resolve_names_remote(names))

    if remote and taxids.has_data():
      self.cache.cache_payload(self.resolve_from_cache(taxids, names))
      if taxids.has_data():
        self.cache.cache_payload(self.resolve_taxids_remote(taxids))

  def resolve_taxids(self, taxids:Type[ncbitaxonomist.payload.taxid.TaxidPayload])->Type[ncbitaxonomist.payload.taxid.TaxidPayload]:
    """
    Resolve taxids in local database using a taxid payload for
    class:`ncbitaxonomist.query.resolve.taxid.TaxidResolveQuery`.
    """
    self.logger.log(taxids)
    trq = ncbitaxonomist.query.resolve.taxid.TaxidResolveQuery(taxids)
    self.db.get_taxid_lineages(
      taxids.as_list(), ncbitaxonomist.convert.taxadb.TaxaDbConverter(), trq)
    return taxids

  def resolve_taxids_remote(self, taxids:Type[ncbitaxonomist.payload.taxid.TaxidPayload])->Type[ncbitaxonomist.payload.taxid.TaxidPayload]:
    """Resolve taxids on Entrez remotely using a taxid payload for
    class:`ncbitaxonomist.query.entrez.EntrezTaxonomyQuery`."""
    self.logger.log(taxids, 'entrez')
    trq = ncbitaxonomist.query.resolve.taxid.TaxidResolveQuery(taxids)
    etq = ncbitaxonomist.query.entrez.EntrezTaxonomyQuery(self.email)
    etq.query_taxids(
      taxids.as_list(), ncbitaxonomist.analyzer.resolve.ResolverAnalyzer(
        trq, ncbitaxonomist.convert.ncbitaxon.NcbiTaxonConverter()))
    return taxids

  def resolve_names(self, names:Type[ncbitaxonomist.payload.name.NamePayload])->Type[ncbitaxonomist.payload.name.NamePayload]:
    """Resolve taxa names in local database using a name payload for
    class:`ncbitaxonomist.query.resolve.taxid.TaxidResolveQuery`."""
    self.logger.log(names)
    taxa = self.db.get_taxa_by_name(
      names.as_list(), ncbitaxonomist.convert.taxadb.TaxaDbConverter())
    nrq = ncbitaxonomist.query.resolve.name.NameResolveQuery(names)
    self.db.get_taxid_lineages(
      list(taxa), ncbitaxonomist.convert.taxadb.TaxaDbConverter(), nrq)
    return names

  def resolve_names_remote(self, names:Type[ncbitaxonomist.payload.name.NamePayload])->Type[ncbitaxonomist.payload.name.NamePayload]:
    """Resolve names on Entrez remotely using a name payload for
    class:`ncbitaxonomist.query.entrez.EntrezTaxonomyQuery`."""
    self.logger.log(names, 'entrez')
    nrq = ncbitaxonomist.query.resolve.name.NameResolveQuery(names)
    etq = ncbitaxonomist.query.entrez.EntrezTaxonomyQuery(self.email)
    etq.query_names(
      names.as_list(),
      ncbitaxonomist.analyzer.resolve.ResolverAnalyzer(
        nrq, ncbitaxonomist.convert.ncbitaxon.NcbiTaxonConverter()))
    return names

  def resolve_accession_map(self, accs:Type[ncbitaxonomist.payload.accessionmap.AccessionMap])->Type[ncbitaxonomist.payload.accessionmap.AccessionMap]:
    """Resolves taxa lineages for accessions in a local database. Accessions
    need to be mapped beforehand and are read from STDIN."""
    self.logger.log(accs)
    arq = ncbitaxonomist.query.resolve.accession.AccessionResolveQuery(accs)
    self.db.get_taxid_lineages(
      accs.get_taxid_list(), ncbitaxonomist.convert.taxadb.TaxaDbConverter(), arq)
    return accs

  def resolve_accession_map_remote(self, accs:Type[ncbitaxonomist.payload.accessionmap.AccessionMap])->Type[ncbitaxonomist.payload.accessionmap.AccessionMap]:
    """Resolves taxa lineages for accessions remotely on Entrez. Accessions
    need to be mapped beforehand and are read from STDIN."""
    self.logger.log(accs, 'entrez')
    arq = ncbitaxonomist.query.resolve.accession.AccessionResolveQuery(accs)
    rtq = ncbitaxonomist.query.entrez.EntrezTaxonomyQuery(self.email)
    rtq.query_taxids(
      accs.get_taxid_list(), ncbitaxonomist.analyzer.resolve.ResolverAnalyzer(
        arq, ncbitaxonomist.convert.ncbitaxon.NcbiTaxonConverter()))
    return accs

  def resolve_stdin(self):
    """Resolve lineages for taxa piped via STDIN from a preceding taxonomist
    command."""
    self.logger.log_msg('Parsing STDIN')
    taxa:Dict[int,Type[ncbitaxonomist.model.taxon.Taxon]] = {} # Dict to store taxa
    taxids = parse_taxa(taxa)
    if not taxids.has_data():
      return taxids
    trq = ncbitaxonomist.query.resolve.taxid.TaxidResolveQuery(taxids)
    trq.resolve(taxids.as_list(), taxa)
    return taxids

  def resolve_from_cache(self, taxids=None, names=None):
    """Resolve lineage from cache."""
    if names:
      self.logger.log(taxids, 'cache')
      nrq = ncbitaxonomist.query.resolve.name.NameResolveQuery(names)
      nrq.resolve(
        list(self.cache.union_taxid_names(taxids.as_list(), names.as_list())),
        self.cache.get_taxa())
      return names
    self.logger.log(names, 'cache')
    trq = ncbitaxonomist.query.resolve.taxid.TaxidResolveQuery(taxids)
    trq.resolve(list(self.cache.union_taxid_names(taxids, names)),
                self.cache.get_taxa())
    return taxids

def parse_taxa(taxa:Dict)->[ncbitaxonomist.payload.taxid.TaxidPayload]:
  """Resolve lineages from taxa read from STDIN. The input is expected to be
  class:`ncbitaxonomist.model.taxon.Taxon` attributes in JSON, one per line."""
  parents = set()
  for i in sys.stdin:
    t = ncbitaxonomist.model.taxon.Taxon().new_from_json(i.strip())
    parents.add(t.parent_id)
    if t.taxon_id not in taxa:
      taxa[t.taxon_id] = t

  pload = ncbitaxonomist.payload.taxid.TaxidPayload(parse=False)
  for i in taxa:
    if i not in parents:
      pload.add(taxa[i].taxon_id)
  return pload
