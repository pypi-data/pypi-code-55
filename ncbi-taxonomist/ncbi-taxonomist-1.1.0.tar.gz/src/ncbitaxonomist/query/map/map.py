"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

from typing import Dict, Type


import ncbitaxonomist.model.datamodel
import ncbitaxonomist.payload.payload

class MapQuery:

  def __init__(self, qrypayload:Type[ncbitaxonomist.payload.payload.Payload]):
    self.payload = qrypayload

  def map_query(self, model:Type[ncbitaxonomist.model.datamodel.DataModel]):
    raise NotImplementedError
