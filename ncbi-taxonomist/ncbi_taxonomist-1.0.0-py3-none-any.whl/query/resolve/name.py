"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

from typing import Iterable, Mapping, Type


import ncbitaxonomist.utils
import ncbitaxonomist.model.taxon
import ncbitaxonomist.query.resolve.resolve
import ncbitaxonomist.cache.cache

cache = ncbitaxonomist.cache.cache.Cache()

class NameResolveQuery(ncbitaxonomist.query.resolve.resolve.ResolveQuery):

  def resolve(self, taxids:Iterable[int], taxa:Mapping[int,Type[ncbitaxonomist.model.taxon.Taxon]]):
    for i in taxids:
      taxon = taxa.get(i)
      if taxon:
        cache.cache_taxon(taxon)
        update = self.payload.process(taxon, NameResolveQuery.resolve_lineage(i, taxa))
        if update.processed:
          ncbitaxonomist.utils.json_stdout({
            'name':update.value,
            'lin':[x.get_attributes() for x in self.payload.get_data(update.value)]})


