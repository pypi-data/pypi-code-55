class AGGREGATE:
  COUNT = lambda xs: [len(x) for x in xs]
  FIRST = lambda xs: [x[0] for x in xs]
  MAX = lambda xs: [max(x) for x in xs]
  MEAN = lambda xs: [sum(x) / len(x) for x in xs]
  MIN = lambda xs: [min(x) for x in xs]
  SUM = lambda xs: [sum(x) for x in xs]
  COLLECT = lambda xss: [x for xs in xss for x in xs]
  @staticmethod
  def _fromString(s, xs):
    if s.upper() in xs.keys():
      return xs[s.upper()]
    return None
  @staticmethod
  def fromString(s):
    return AGGREGATE._fromString(s, {
      'COUNT': AGGREGATE.COUNT,
      'FIRST': AGGREGATE.FIRST,
      'MAX': AGGREGATE.MAX,
      'MEAN': AGGREGATE.MEAN,
      'MIN': AGGREGATE.MIN,
      'SUM': AGGREGATE.SUM,
      'COLLECT': AGGREGATE.COLLECT,
    })
  @staticmethod
  def needsFilterFromString(s):
    return AGGREGATE._fromString(s, {
      'COUNT': False,
      'FIRST': True,
      'MAX': True,
      'MEAN': True,
      'MIN': True,
      'SUM': True,
      'COLLECT': True,
    })

class VISUALIZATION_TYPE:
  BAR_CHART = 'BAR_CHART'
  BOX_PLOT = 'BOX_PLOT'
  TEXT_COLLECTION = 'TEXT_COLLECTION'
  MAP = 'MAP'
