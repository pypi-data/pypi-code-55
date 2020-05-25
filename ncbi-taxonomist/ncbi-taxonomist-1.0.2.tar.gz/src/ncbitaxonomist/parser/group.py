"""
..
  Copyright 2020

.. moduleauthor:: Jan Piotr Buchmann <jpb@members.fsf.org>
"""

import io
import os
import sys
import json

class GroupParser:

  def __init__(self):
    self.seen_taxids = set()

  def parse(self, groupname:str):
    """Parse stdin for taxon_id to add into group groupname"""
    taxids = []
    for i in sys.stdin:
      linein = json.loads(i.strip())
      if 'subtrees' in linein:
        self.parse_taxa_list(linein['subtrees'], taxids, groupname)
      elif 'lin' in linein:
        self.parse_taxa_list(linein['lin'], taxids, groupname)
      elif 'taxon' in linein:
        self.parse_taxon(linein['taxon'], taxids, groupname)
      elif 'taxon_id' in linein:
        self.parse_taxon(linein['taxon_id'], taxids, groupname)
      else:
        sys.exit("Unknown input: {}.Abort".format(linein))
      print(i.strip())
    return taxids

  def parse_taxa_list(self, taxa_list, taxids, groupname):
    for i in taxa_list:
      self.parse_taxon(i['taxon_id'], taxids, groupname)

  def parse_taxon(self, taxid, taxids, groupname):
    if int(taxid) not in self.seen_taxids:
      self.seen_taxids.add(int(taxid))
      taxids.append((int(taxid), groupname))
