from .apriori import dataset

def itemFreq(_item):
  """
    Return support value
    _item: list of string, ex ['123'] or ['123', '124']
    dataset: list of list of string, ex [['123'], ['123', '124']]
  """
  return len([row for row in dataset if set(_item).issubset(row)])

def support(_item):
  """
    Return support value
    _item: list of string, ex ['123'] or ['123', '124']
    dataset: list of list of string, ex [['123'], ['123', '124']]
  """
  return itemFreq(_item)/len(dataset)

def confidence(_item, next_item):
  """
    Return confidence value
    _item: list of string, ex ['123'] or ['123', '124']
    next_item: list of string, ex ['123'] or ['123', '124']
  """
  join = _item + next_item
  return support(join)/support(_item)
