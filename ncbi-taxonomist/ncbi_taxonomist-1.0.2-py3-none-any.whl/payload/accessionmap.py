"""
..
  Copyright 2020

.. moduleauthor:: Jan Piotr Buchmann <jpb@members.fsf.org>
"""

import sys
import json
from typing import Dict, Iterable, List, Type

import ncbitaxonomist.cache.cache
import ncbitaxonomist.payload.payload
import ncbitaxonomist.payload.taxid
import ncbitaxonomist.model.datamodel
import ncbitaxonomist.model.accession

class AccessionMap(ncbitaxonomist.payload.payload.Payload):
  """
  Implements the special payload of an accession map containing
  Because each taxid can have several accessions, one dict stores all accessions
  associated with a given taxid. The other Dict stores the accessions instances.
  The results are stored as Dict with the accession as key and list of
  associated as value.
  """

  class Update(ncbitaxonomist.payload.payload.Payload.Update):

    def __init__(self, processed:bool=False, value:str=None):
      super().__init__(processed, value)

  def __init__(self):
    """Sets up payload and processes input data. If parse is False, do not
    read arguments or STDIN to allow different method."""
    super().__init__('accmap', args=None, parse=False)
    self.data:Dict[str,List[ncbitaxonomist.model.datamodel.DataModel]]
    self.accs:Dict[str,Type[ncbitaxonomist.model.accession.Accession]] = {}
    self.taxid_accs:Dict[int,List[str]] = {}
    self.parse_stdin()

  def parse_args(self, args:Iterable[str]):
    """No arguments required """
    pass

  def parse_stdin(self):
    for i in sys.stdin:
      mapping = json.loads(i.strip())
      if 'accs' not in mapping or 'data' not in mapping:
        sys.exit("Not valid mapping data. Abort.")
      self.add_taxid_accs(mapping['data']['taxon_id'], mapping['accs'])
      self.add(mapping.pop('accs'), mapping.pop('data'))

  def add_taxid_accs(self, taxid:int, accession:str):
    if int(taxid) not in self.taxid_accs:
      self.taxid_accs[int(taxid)] = []
    self.taxid_accs[int(taxid)].append(str(accession))

  def add(self, accession, attributes):
    if accession not in self.data:
      self.accs[accession] = ncbitaxonomist.model.accession.Accession(attributes)
      self.data[accession] = []

  def process(self, accession:str, result):
    """Checks if the accession model is part of the query"""
    if accession in self.data:
      self.data[accession] = result
      return AccessionMap.Update(True, accession)
    return AccessionMap.Update()

  def get_accession(self, acc:str):
    return self.accs.get(acc)

  def has_taxid(self, taxid:int)->bool:
    return taxid in self.taxid_accs

  def get_taxid_accsessions(self, taxid:int)->List[str]:
    return self.taxid_accs.get(int(taxid))

  def get_taxid_list(self)->List[int]:
    return list(self.taxid_accs)

  def get_data(self)->Dict:
    """Gets payload data."""
    return self.data

  def size(self)->int:
    """Gets the number of requested data."""
    if self.data is not None:
      return len(self.data)
    return 0

  def has_data(self)->bool:
    """Tests if payload contains any data."""
    if self.data is None or self.size() == 0:
      return False
    return True

  def as_list(self)->List[str]:
    """Returns data keys as list."""
    if self.data:
      return list(self.data)
    return []

  def is_processed(self, acc):
    """Tests if the accession has been processed."""
    if not self.data.get(str(acc)):
      return False
    return True

  def remove(self, acc):
    return self.data.pop(str(acc), None)

  def update_from_cache(self, cache:Type[ncbitaxonomist.cache.cache.Cache]):
    """Accession lineages are not cached."""
    pass
