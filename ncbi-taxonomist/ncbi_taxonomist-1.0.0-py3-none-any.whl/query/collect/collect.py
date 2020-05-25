"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Type, Mapping, AbstractSet, Iterable


import ncbitaxonomist.payload.payload
import ncbitaxonomist.model.taxon


class CollectQuery:

  def __init__(self, qrypayload:Type[ncbitaxonomist.payload.payload.Payload]):
    self.payload = qrypayload

  def collect(self, taxon:Type[ncbitaxonomist.model.taxon.Taxon]):
    raise NotImplementedError
