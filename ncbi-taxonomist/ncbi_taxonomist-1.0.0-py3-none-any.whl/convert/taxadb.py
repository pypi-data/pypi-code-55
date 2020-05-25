"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Dict, Type, Mapping


from ncbitaxonomist.model import taxon
import ncbitaxonomist.convert.converter


class TaxaDbConverter(ncbitaxonomist.convert.converter.ModelConverter):
  """Converts local database attributes into
    class:`ncbitaxonomist.model.taxon.Taxon` instances and vice versa"""

  def convert_to_model(self, attributes:Mapping, srcdb=None)->Type[taxon.Taxon]:
    """
    Convert local database taxon attributes into
    class:`ncbitaxonomist.model.taxon.Taxon`
    """
    del srcdb
    attributes['names'] = {}
    if 'name' in attributes:
      attributes['names'].update({attributes['name']:attributes['type']})
    return taxon.Taxon(attributes)

  def convert_from_model(self, model:Type[taxon.Taxon], outdict=None)->Dict[str,str]:
    del outdict
    return model.get_attribues()
