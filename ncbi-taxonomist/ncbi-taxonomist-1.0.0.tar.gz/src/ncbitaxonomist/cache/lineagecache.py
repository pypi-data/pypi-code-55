"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Iterable, List, Set


class LineaegeCache:
  """
  Class to handle caching of lineages. Lineages are cached as taxids
  which can be retrieved from class:`ncbitaxonomist.cache.taxa.TaxaCache`.
  """

  def __init__(self):
    self.taxids = set()

  def cache(self, taxid):
    self.taxids.add(taxid)

  def remove_cached_lineages_taxids(self, taxids:Iterable[int]=None)->List[int]:
    noncached = []
    while taxids:
      t = taxids.pop()
      if not self.incache(t):
        noncached.append(t)
    return noncached

  def incache(self, name=None, taxid=None):
    del name # Unused
    return taxid in self.taxids

  def get_cached_lineage_taxids(self, taxids:Iterable[int]=None)->Set[int]:
    cached = set()
    for i in taxids:
      if self.incache(i):
        cached.add(i)
    return cached

  def is_empty(self):
    if self.taxids:
      return False
    return True
