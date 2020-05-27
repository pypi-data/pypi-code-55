"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import entrezpy.base.result


class NcbiAccessionResult(entrezpy.base.result.EutilsResult):

  def __init__(self, request:object):
    super().__init__(request.eutil, request.query_id, request.db)
    self.accessions = {}

  def size(self):
    return len(self.accessions)

  def get_link_parameter(self, reqnum=0):
    del reqnum #Unused
    print("{}: Entrez links not supported".format(__name__))

  def isEmpty(self):
    if not self.accessions:
      return True
    return False

  def dump(self):
    return {'db':self.db, 'size' : self.size(), 'function' : self.function,
            'accs': list(self.accessions)}

  def add_accession(self, accs):
    self.accessions.update({accs.uid:accs})
