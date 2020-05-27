"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

from typing import Dict, Iterable, Type



from ncbitaxonomist import utils
import ncbitaxonomist.model.accession
import ncbitaxonomist.query.map.map


cache = ncbitaxonomist.cache.cache.Cache()

class AccessionMapQuery(ncbitaxonomist.query.map.map.MapQuery):

  def map_query(self, acc:Type[ncbitaxonomist.model.accession.Accession]):
    cache.cache_accession(acc)
    upd = self.payload.process(acc)
    if upd.processed:
      utils.json_stdout({'accs': upd.value, 'data': acc.get_attributes()})
