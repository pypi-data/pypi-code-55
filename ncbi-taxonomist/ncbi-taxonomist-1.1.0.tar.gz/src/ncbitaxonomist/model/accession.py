"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Dict, Mapping


from ncbitaxonomist.model import datamodel

class Accession(datamodel.DataModel):

  def __init__(self, attributes:Mapping=None):
    super().__init__(attributes)
    attributes = datamodel.standardize_attributes(attributes)
    self.taxon_id = datamodel.int_attribute(attributes.pop('taxon_id', None))
    self.uid = datamodel.int_attribute(attributes.pop('uid', None))
    self.db = attributes.pop('db', None)
    self.accessions = attributes.pop('accessions', {})

  def update_accessions(self, accession:Mapping[str,str]):
    """Update accessions from dictionary with structure accession:type"""
    self.accessions.update(accession)

  def get_attributes(self) -> Dict[str,any]:
    return {'taxon_id':self.taxon_id, 'accessions':self.accessions,
            'db':self.db, 'uid':self.uid}

  def get_accessions(self)->Dict[str,str]:
    """Return accessions as dictionary"""
    return self.accessions
