"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import sys
import json
from typing import Iterable, List, Mapping


def read_stdin(sep:str=None)->List[str]:
  """Reads standard input expecting string arguments"""
  if not sep:
    return [x.strip() for x in sys.stdin]
  args = []
  for i in sys.stdin:
    if sep == ',':
      args += [x.strip() for x in i.replace(' ', '').split(',')]
    else:
      args += [x.strip() for x in i.split(' ')]
  return args

def read_int_stdin(sep:str=None)->List[int]:
  """Reads standard input expecting integer arguments"""
  uniq_taxids = set()
  if not sep:
    uniq_taxids.update([int(x.strip()) for x in sys.stdin])
    return list(uniq_taxids)
  for i in sys.stdin:
    if sep == ',':
      uniq_taxids.update([int(x.strip()) for x in i.replace(',', ' ').split()])
    else:
      uniq_taxids.update([int(x.strip()) for x in i.split()])
  return list(uniq_taxids)

def parse_taxids(taxids:Iterable[str])->List[int]:
  """Parses taxid arguments"""
  if taxids is None:
    return None
  if not taxids:
    return read_int_stdin()
  uniq_taxids = set()
  for i in taxids:
    #uniq_taxids.update(set([int(x) for x in i.replace(',', ' ').split()]))
    uniq_taxids.update(set(int(x) for x in i.replace(',', ' ').split()))
  return list(uniq_taxids)

def parse_names(names:Iterable[str])->List[str]:
  """Parses name arguments"""
  if names is None:
    return None
  if not names:
    return read_stdin()
  args = []
  for i in names:
    if i.rfind(',') != -1:
      for j in i.split(','):
        if j:
          args.append(j.strip())
    else:
      args.append(i.strip())
  return args

def json_stdout(data:Mapping[str,str]):
  """Prints input dict as JSON to stdout"""
  sys.stdout.write(json.dumps(data, separators=(',', ':'))+'\n')

#def resolve_func_nspace(cls, func, rootlogger='ncbi-taxonomist'):
  #return "{}.{}.{}.{}".format(rootlogger, cls.__module__, cls.__qualname__, sys._getframe().f_code.co_name)

def no_rank():
  """Returns the value for taxa without ranks, works as a constant since Python
     has no constants"""
  return 'NA'
