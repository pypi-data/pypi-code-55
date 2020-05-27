"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import sys
from typing import Dict, Mapping, Type


import ncbitaxonomist.model.accession
from ncbitaxonomist.convert import converter
from ncbitaxonomist.convert import convertermap

class NcbiAccessionConverter(converter.ModelConverter):
  """Convert NCBI accession data into model or model into attributes"""

  def convert_to_model(self, attributes:Mapping[str,any], srcdb=None)->Type[ncbitaxonomist.model.accession.Accession]:
    """Converts NCBI attributes to accession model"""
    mattribs = {'uid':attributes.pop('uid'), 'db': srcdb, 'accessions': {}}
    self.map_inattributes(mattribs, attributes, convertermap.attributes)
    if srcdb not in convertermap.accessions:
      print("{}: database not supported".format(srcdb), file=sys.stdout)
      return None
    if srcdb in convertermap.accessions:
      for i in convertermap.accessions[srcdb]:
        if i in attributes:
          mattribs['accessions'][i] = attributes.pop(i)
    return ncbitaxonomist.model.accession.Accession(mattribs)

  def convert_from_model(self, model:Type[ncbitaxonomist.model.accession.Accession], outdict=None)->Dict[str,str]:
    """Converts accession model to attributes"""
    del outdict
    attrib = model.attributes()
    attrib.update({'accessions':{'uid':model.uid}})
    return attrib
