"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import sqlite3
from typing import Iterable, Dict, List, Mapping, Tuple, Type


from ncbitaxonomist.convert import converter
from ncbitaxonomist.convert import taxadb
from ncbitaxonomist.model import datamodel
from ncbitaxonomist.query.resolve import resolve
import ncbitaxonomist.log.dblogger
import ncbitaxonomist.subtree.subtree
import ncbitaxonomist.db.table.taxa
import ncbitaxonomist.db.table.names
import ncbitaxonomist.db.table.accessions
import ncbitaxonomist.db.table.groups
import ncbitaxonomist.query.map.map

class TaxonomyDb:
  """
  Implements the taxonomist database. It manages all operation to add, modify,
  and retrieve taxonomic data.
  """

  def __init__(self, dbpath:str, verbosity:int=0):
    self.logger = ncbitaxonomist.log.dblogger.DbLogger(cls=TaxonomyDb, verbosity=verbosity)
    self.logger.add_db(dbpath)
    self.path = dbpath
    self.connection = self.init_connection()
    self.taxa = ncbitaxonomist.db.table.taxa.TaxaTable(self.path).create(self.connection)
    self.names = ncbitaxonomist.db.table.names.NameTable(self.path).create(self.connection)
    self.accs = ncbitaxonomist.db.table.accessions.AccessionTable(self.path).create(self.connection)
    self.groups = ncbitaxonomist.db.table.groups.GroupTable(self.path).create(self.connection)

  def init_connection(self)->sqlite3.Connection:
    """Setup connection to local database"""
    self.logger.log("Connecting")
    connection = sqlite3.connect(self.path)
    connection.execute("PRAGMA foreign_keys=1")
    connection.row_factory = sqlite3.Row
    self.logger.log("Connected", connection)
    return connection

  def connect(self) -> sqlite3.Connection:
    """Connect to local database"""
    if self.connection is None:
      return self.init_connection(self.path)
    return self.connection

  def close_connection(self)->None:
    """Close connection to local database"""
    self.logger.log("Closing connection")
    self.connection.close()

  def add_taxa(self, values:Iterable[Tuple[int,str,int]])->None:
    """Add taxa into taxa table"""
    self.taxa.insert(self.connection, values)

  def add_taxids(self, taxids:Iterable[Tuple[int,]])->None:
    """Add taxids into taxa table"""
    self.taxa.insert_taxids(self.connection, taxids)

  def add_names(self, values:Iterable[Tuple[int,str,str]])->None:
    """Add names into taxa table"""
    self.names.insert(self.connection, values)

  def add_accessions(self, values:Iterable[Tuple[str,str,str,int]])->None:
    """Add accessions into accesssion table"""
    self.accs.insert(self.connection, values)

  def add_group(self, values:[Iterable[Tuple[int,str]]]):
    """Add group into group table"""
    self.groups.insert(self.connection, values)

  def collect_subtree(self, taxid:int, conv:Type[taxadb.TaxaDbConverter],
                      subtree=None)->List:
    """ Collect subtree for given taxon ids. """
    if subtree is None:
      subtree = ncbitaxonomist.subtree.subtree.Subtree()
    if not subtree.isCollected(taxid):
      for i in self.taxa.get_subtree(self.connection, taxid):
        if not subtree.has_taxon(i['taxon_id']):
          subtree.add_taxon(conv.convert_to_model({'taxon_id': i['taxon_id'],
                                                   'parent_id':i['parent_id'],
                                                   'rank':i['rank']}))
        subtree.taxa[i['taxon_id']].update_names({i['name']:i['type']})
    return subtree

  def get_taxa_by_name(self, names:Iterable[str],
                       conv:Type[converter.ModelConverter],
                       query:Type[ncbitaxonomist.query.map.map.MapQuery]=None,
                       taxa:Mapping[int,datamodel.DataModel]=None)->Dict[int,datamodel.DataModel]:
    """Collect taxa by name and converter to appropriate model.

    .. todo:: Test if n.name='man' OR n.name='Bacteria OR ...' is better approach
    """
    if taxa is None:
      taxa = {}
    taxidqry = """SELECT taxon_id FROM names  WHERE name=?"""
    for i in names:
      taxid = self.connection.cursor().execute(taxidqry, (i,)).fetchone()
      if taxid is not None and taxid[0] not in taxa:
        taxa[taxid[0]] = None
    qry = """SELECT n.name, n.type, t.taxon_id, t.rank, t.parent_id FROM taxa t
             JOIN names n on t.taxon_id=n.taxon_id WHERE t.taxon_id=?"""
    for i in taxa:
      for j in self.connection.cursor().execute(qry, (i,)):
        if taxa[j['taxon_id']] is None:
          taxa[j['taxon_id']] = conv.convert_to_model({'taxon_id':j['taxon_id'],
                                                       'parent_id':j['parent_id'],
                                                       'rank':j['rank']})
        taxa[j['taxon_id']].update_names({j['name']:j['type']})
      if query and taxa:
        query.map_query(taxa[i])
    return taxa

  def names_to_taxid(self, names:Iterable[str])->Dict[str,int]:
    """Return mapping of given name to correspondong taxid."""
    mapping = {}
    for i in names:
      row = self.names.name_to_taxid(self.connection, i).fetchone()
      if row:
        mapping[row['name']] = int(row['taxon_id'])
    return mapping

  def get_taxa_by_accessions(self, accs:Iterable[str], db:str, conv:Type[converter.ModelConverter],
                             query:Type[ncbitaxonomist.query.map.map.MapQuery]=None)->Dict[int,datamodel.DataModel]:
    """Collect taxa by accession and converter to appropriate model."""
    uids = {}
    uidqry =  """SELECT db, uid FROM accessions WHERE accession=? AND db=?"""
    if not db:
      uidqry = """SELECT db, uid FROM accessions WHERE accession=? AND db LIKE ?)"""
    for i in accs:
      row = self.connection.cursor().execute(uidqry, (i, db)).fetchone()
      if row is not None:
        if row['db'] not in uids:
          uids[row['db']] = []
        uids[row['db']].append(int(row['uid']))
    stmt = """SELECT a.uid, a.accession, a.db, a.type, t.taxon_id
              FROM accessions a JOIN taxa t on a.taxon_id=t.taxon_id
              WHERE a.uid=? and a.db=?"""
    mappings = {}
    for i in uids:
      for j in uids[i]:
        for k in self.connection.cursor().execute(stmt, (j, i)):
          if int(k['uid']) not in mappings:
            mappings[int(k['uid'])] = conv.convert_to_model({'accessions':{k['type']:k['accession']},
                                                             'taxon_id':k['taxon_id'], 'db':k['db'],
                                                             'uid': k['uid']})
          mappings[int(k['uid'])].update_accessions({k['type']:k['accession']})
        if query and mappings:
          query.map_query(mappings[j])
    return mappings

  def get_taxa_by_taxids(self, taxids:Iterable[int], conv:Type[converter.ModelConverter],
                         query:Type[ncbitaxonomist.query.map.map.MapQuery]=None)->Dict[int, datamodel.DataModel]:
    """Collect taxa by taxid and converter to appropriate model."""
    qry = """SELECT t.taxon_id, t.rank, t.parent_id, n.name, n.type
             FROM taxa t JOIN names n on t.taxon_id=n.taxon_id WHERE t.taxon_id=?"""
    taxa = {}
    for i in taxids:
      for j in self.connection.cursor().execute(qry, (i,)):
        if int(j['taxon_id']) not in taxa:
          taxa[int(j['taxon_id'])] = conv.convert_to_model({'taxon_id': j['taxon_id'],
                                                            'parent_id':j['parent_id'],
                                                            'rank':j['rank']})
        taxa[int(j['taxon_id'])].update_names({j['name']:j['type']})
      if query and taxa:
        query.map_query(int(i))
    return taxa

  def get_taxid_lineages(self, taxids:Iterable[int], conv:Type[converter.ModelConverter],
                         query:Type[resolve.ResolveQuery]=None)->Dict[int, datamodel.DataModel]:
    """Collect lineage taxa for multiple taxid."""
    taxa = {}
    for i in taxids:
      if i not in taxa:
        self.get_lineage(i, conv, taxa)
      if query and taxa:
        query.resolve([i], taxa)
    return taxa

  def get_taxid_lineage(self, taxid:int, conv:Type[converter.ModelConverter],
                        query:Type[resolve.ResolveQuery]=None,
                        taxa:Mapping[int,datamodel.DataModel]=None)->Dict[int,datamodel.DataModel]:
    """Collect lineage taxa for a single taxid."""
    if taxa is None:
      taxa = {}
    self.get_lineage(taxid, conv, taxa)
    if query and taxa:
      query.resolve([taxid], taxa)
    return taxa

  def get_lineage(self, taxid, conv:Type[converter.ModelConverter], taxa)->None:
    """Collect lineage."""
    for j in self.taxa.get_lineage(self.connection, taxid, self.names.name):
      if int(j['taxon_id']) not in taxa:
        taxa[int(j['taxon_id'])] = conv.convert_to_model({'taxon_id': j['taxon_id'],
                                                          'parent_id':j['parent_id'],
                                                          'rank':j['rank']})
      taxa[int(j['taxon_id'])].update_names({j['name']:j['type']})

  def remove_group(self, groupname):
    """Remove a group."""
    self.groups.delete_group(self.connection, groupname)

  def remove_from_group(self, taxids, names, groupname):
    """Remove taxids and names from a given group."""
    values = []
    seen_taxids = set()
    while taxids:
      values.append((taxids.pop(), groupname))
      seen_taxids.add(values[-1][0])
    if names:
      stmt = """SELECT taxon_id FROM names WHERE name=?"""
      for i in names:
        taxid = self.connection.cursor().execute(stmt, (i,)).fetchone()[0]
        if taxid is not None and taxid not in seen_taxids:
          values.append((taxid, groupname))
          seen_taxids.add(taxid)
    seen_taxids.clear()
    self.groups.delete_from_group(self.connection, values)

  def retrieve_group_names(self):
    """Return all group names"""
    return self.groups.retrieve_names(self.connection)

  def retrieve_group(self, groupname):
    """Return all taxis withon a given group"""
    return self.groups.retrieve_group(self.connection, groupname)
