def dcs(dcmap, pops):
  """ Find minimal cover of DCS
  Args:
    dcmap: A string, the name of the file with the dcmap.
    pops: A string, a comma separated list of pops to cover.

  Returns:
    A string, a comma separated list of DCs that cover pops minimally.
  """
  f = open(dcmap)
  lines = f.readlines()

  pop_coverage = {}
  dc_pops = collections.defaultdict(set)
  pop_dcs = collections.defaultdict(set)

  pops = pops.split(',')

  for i, line in enumerate(lines):
    if i == 1:
      continue
    dc, pops_ = line.split(' ')
    pops_ = pops[:-1]
    counter = 0
    for pop in pops_.split(','):
      dc_pops[dc].add(pop)
      pop_dcs[pop].add(dc)
      if pop in pops:
        counter += 1
    
    dc_coverage[dc] = counter

    
    

  f.close()

def test(func, test_cases):
  for case in test_cases:
    out = func(*case['in'])
    if out == case['out']:
      print('Success')
    else:
      print('Failed. The output is {}'.format(out))

if __name__ == "__main__":
    test_cases = [{
      'in': ['colomap', 'lhr01,syd04'],
      'out': 'ae'
    },
    {
      'in': ['colomap', 'syd01,mel01'],
      'out': 'ae,aa'
    }]
    test(dcs, test_cases)