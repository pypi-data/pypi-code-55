"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

from typing import Type, Mapping, List, AbstractSet, Iterable


import ncbitaxonomist.model.taxon
import ncbitaxonomist.payload.payload
import ncbitaxonomist.resolve.lineageresolver


class ResolveQuery:

  @staticmethod
  def resolve_lineage(taxid:int, taxa:Mapping[int,Type[ncbitaxonomist.model.taxon.Taxon]])->List[Type[ncbitaxonomist.model.taxon.Taxon]]:
    return ncbitaxonomist.resolve.lineageresolver.resolve_lineage(taxid, taxa)

  def __init__(self, qrypayload:Type[ncbitaxonomist.payload.payload.Payload]):
    self.payload = qrypayload

  def resolve(self, taxids:AbstractSet[int], taxa:Mapping[int,Type[ncbitaxonomist.model.taxon.Taxon]]):
    raise NotImplementedError
