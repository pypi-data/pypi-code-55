"""
..
  Copyright 2020 The University of Sydney

  DTDs:
    assembly:
      https://eutils.ncbi.nlm.nih.gov/eutils/dtd/20180216/esummary_assembly.dtd
    bioprojects:
      https://eutils.ncbi.nlm.nih.gov/eutils/dtd/20180216/esummary_assembly.dtd
.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

accessions = {
  'assembly' :
    ['assemblyaccession', 'lastmajorreleaseaccession', 'assemblyname'],
  'bioproject' : ['project_id', 'project_acc', 'project_name'],
  'nucleotide' : ['accessionversion', 'caption', 'extra'],
  'protein' : ['accessionversion', 'caption', 'extra']
}

attributes = {'taxid' : 'taxon_id', 'parent_taxid' : 'parent_id', 'rank':'rank'}
