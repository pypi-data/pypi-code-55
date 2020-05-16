from Empiric.internal.Print import Print

class StatisticsTools:
  @staticmethod
  def _camelCase(s):
    s = ''.join([c for c in s.replace('-', ' ') if c.isalnum() or c == ' '])
    return ''.join(x.capitalize() for x in s.split(' '))
  @staticmethod
  def fixKeyTitle(statistics):
    if 'key' not in statistics and 'title' in statistics:
      statistics['key'] = StatisticsTools._camelCase(statistics['title'])
    if 'title' not in statistics and 'key' in statistics:
      statistics['title'] = statistics['key']
    return statistics
  @staticmethod
  def statisticsToList(statistics, prefixToKey=None):
    if 'substatistics' not in statistics:
      return [statistics]
    ss = statistics['substatistics']
    if prefixToKey:
      for s in ss:
        s['key'] = prefixToKey + '-' + s['key']
    return ss
  @staticmethod
  def mergeWithDefaultStatistics(statistics, defaultStatistics, appendToDefaultStatistics, hideStatisticsByDefault):
    if not hideStatisticsByDefault and not statistics:
      Print.logWarning('Please provide \'statistics\' keyword for all relevant pages')
    if statistics is None or not defaultStatistics:
      return statistics
    if isinstance(statistics, str):
      defaultStatistics['title'] = statistics
      return defaultStatistics
    if not appendToDefaultStatistics:
      return statistics
    s = {
      'substatistics': [],
    }
    if 'key' in statistics:
      s['key'] = statistics['key']
    if 'title' in statistics:
      s['title'] = statistics['title']
    if not 'substatistics' in statistics and 'substatistics' in defaultStatistics:
      if 'key' in defaultStatistics:
        s['key'] = defaultStatistics['key']
      if 'title' in defaultStatistics:
        s['title'] = defaultStatistics['title']
    s['substatistics'].extend(StatisticsTools.statisticsToList(statistics))
    s['substatistics'].extend(StatisticsTools.statisticsToList(defaultStatistics, prefixToKey='default'))
    return s
