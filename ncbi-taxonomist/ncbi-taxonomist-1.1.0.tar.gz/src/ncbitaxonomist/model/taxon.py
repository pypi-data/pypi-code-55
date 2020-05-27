"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Dict, Mapping, Type

import ncbitaxonomist.utils
from ncbitaxonomist.model import datamodel


class Taxon(datamodel.DataModel):

  def __init__(self, attributes:Mapping=None):
    super().__init__(attributes)
    attributes = datamodel.standardize_attributes(attributes)
    self.taxon_id = datamodel.int_attribute(attributes.pop('taxon_id', None))
    self.parent_id = datamodel.int_attribute(attributes.pop('parent_id', None))
    self.rank = attributes.pop('rank', None)
    self.names = attributes.pop('names', {})
    if self.rank == 'no rank' or self.rank is None:
      self.rank = ncbitaxonomist.utils.no_rank()

  def update_names(self, names:Mapping[str, str])->None:
    """Update taxon names from a dictionary with the structure {name:type}."""
    self.names.update(names)

  def update(self, taxon:Type[__qualname__])->None:
    """Update taxon names from another Taxon instance."""
    self.update_names(taxon.names)

  def get_attributes(self)->Dict[str,any]:
    """Return taxon attributes as dictionary. The scientific_name is injected to
    simplify parsing with other tools."""
    return {'taxon_id':self.taxon_id, 'rank' : self.rank, 'names':self.names,
            'parent_id':self.parent_id, 'name' : self.get_name_by_type()}

  def get_names(self)->Dict[str,str]:
    """Return names as dictionary with the structure name:type"""
    return self.names

  def get_name_by_type(self, nametype:str='scientific_name')->str:
    """Return specific name type if known."""
    for i in self.names:
      if self.names[i] == nametype:
        return i
    return None

  def get_rank(self):
    return self.rank

  def get_parent(self)->int:
    return self.parent_id

  def isrank(self, rank):
    return self.rank == rank

  def taxid(self):
    return self.taxon_id
