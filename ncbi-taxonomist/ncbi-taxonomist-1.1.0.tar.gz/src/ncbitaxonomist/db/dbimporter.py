"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import sys
import json
from typing import Dict, Iterable, Mapping, Type


from ncbitaxonomist.db import dbmanager
import ncbitaxonomist.log.importlogger

logger = ncbitaxonomist.log.importlogger.ImportLogger(name=__name__)

def parse_taxa(data:Mapping[str,any], taxa:Iterable, names:Iterable):
  """Parse taxa data from STDIN"""
  taxid = data.pop('taxon_id')
  taxa.append((taxid, data.pop('rank'), data.pop('parent_id')))
  if 'names' in data:
    for i in data['names']:
      names.append((taxid, i, data['names'][i]))

def filter_attribute(line, attrib:str)->Dict[str,any]:
  """Select specific attribute to print to STDOUT after import."""
  attribs = json.loads(line.strip())
  if attrib is None:
    sys.stdout.write(line)
    return attribs
  if attrib in attribs:
    sys.stdout.write(json.dumps(attribs[attrib])+'\n')
    return attribs
  #logger.log('filtering', msg="Attribute {} not found".format(attrib))
  return attribs

def commit(db:Type[dbmanager.TaxonomyDb], taxa:Iterable[tuple],
           names:Iterable[tuple], accessions:Iterable[tuple]=None,
           taxids:Iterable[tuple]=None):
  """Commit data into local database. Order of commits is important."""
  if taxa:
    logger.log('commit', db.path, msg="{} / {} (taxa/names)".format(len(taxa), len(names)))
    db.add_taxa(taxa)
    db.add_names(names)
    taxa = []
    names = []
  if accessions:
    logger.log('commit', db.path, msg="{} / {} (accs/taxid)".format(len(accessions), len(taxids)))
    db.add_taxids(taxids)
    db.add_accessions(accessions)
    accessions = []
    taxids = []

def parse_accession(data:Mapping[str,any], accessions:Iterable, taxids:Iterable,
                    taxa:Iterable, names:Iterable):
  """Parse accessions data from STDIN"""
  logger.log('parsing accession', 'STDIN')
  taxid = data.pop('taxon_id')
  db = data.pop('db')
  uid = data.pop('uid')
  for i in data['accessions']:
    accessions.append((data['accessions'][i], i, db, uid, taxid))
  if 'lin' in data:
    for i in data.pop('lin'):
      parse_taxa(i, taxa, names)
  taxids.append((taxid,))

def import_stdin(db:Type[dbmanager.TaxonomyDb], out_attrib:str=None):
  """Parse JSON STDIN and add data to local database"""
  batch_size = 100000
  taxa = []
  names = []
  taxids = []
  accessions = []
  logger.log("parsing STDIN", db.path)
  for i in sys.stdin:
    attribs = filter_attribute(i, out_attrib)
    if 'accs' in attribs:
      if not 'data' in attribs:
        sys.exit("Missing data attribute. Expected with accessions. Abort")
      parse_accession(attribs.pop('data'), accessions, taxids, taxa, names)
      if len(accessions) % batch_size == 0:
        commit(db, taxa, names, accessions, taxids)
    elif 'lin' in attribs:
      logger.log("parsing lineage", db.path)
      for j in attribs.pop('lin'):
        parse_taxa(j, taxa, names)
    elif 'subtrees' in attribs:
      logger.log("parsing subtree", db.path)
      for j in attribs.pop('subtrees'):
        parse_taxa(j, taxa, names)
    elif 'taxon' in attribs:
      parse_taxa(attribs.pop('taxon'), taxa, names)
    else:
      parse_taxa(attribs, taxa, names)
    if len(taxa) % batch_size == 0:
      commit(db, taxa, names)
  if taxa:
    commit(db, taxa, names)
  if accessions:
    commit(db, taxa, names, accessions, taxids)
