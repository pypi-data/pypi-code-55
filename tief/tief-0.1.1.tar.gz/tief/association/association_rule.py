from .calc import confidence, support
import pandas as pd
import itertools

def has_duplicates(iterable):
  l = list(itertools.chain(*iterable)) # in case iterable is an iterator
  return len(set(l)) != len(l)

def permutations(iterable, r=None):
  pool = tuple(iterable)
  n = len(pool)
  r = n if r is None else r
  if r > n:
    return
  indices = list(range(n))
  cycles = list(range(n, n-r, -1))
  permu = [pool[i] for i in indices[:r]]
  if not(has_duplicates(permu)):
    yield permu

  while n:
    for i in reversed(range(r)):
      cycles[i] -= 1
      if cycles[i] == 0:
        indices[i:] = indices[i+1:] + indices[i:i+1]
        cycles[i] = n - i
      else:
        j = cycles[i]
        indices[i], indices[-j] = indices[-j], indices[i]
        permu = [pool[i] for i in indices[:r]]
        if not(has_duplicates(permu)):
          yield permu
        break
    else:
      return

def getPermutations(iterable, r=None):
    return list(permutations(iterable,r))

def association_rule(itemset = [], min_confidence = 0.5):
    asso = getPermutations(itemset,2)
    table = []
    for item in asso:
        conf = confidence(item[0], item[1])
        if conf >= min_confidence:
            table.append([str(item[0])+" --> "+str(item[1]),item[0], item[1], support(item[0]), support(item[1]), conf])
    return pd.DataFrame(table, columns=['Notasi','Antecedent', 'Consequents', 'Antecedent Support', 'Consequents Support', 'Confidence']) 
