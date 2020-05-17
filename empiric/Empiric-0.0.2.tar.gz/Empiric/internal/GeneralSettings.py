import json
import os

from Empiric.internal.StatisticsTools import StatisticsTools

class GeneralSettings():
  _pathCollectedData = 'collected-data/'
  _generalSettings = 'settings.json'
  def __init__(self):
    if not os.path.exists(GeneralSettings._pathCollectedData):
      os.makedirs(GeneralSettings._pathCollectedData)
    if os.path.exists(self._filepath()):
      with open(self._filepath(), 'r') as f:
        self._generalSettings = json.load(f)
    else:
      self._generalSettings = {
        'statistics': {},
      }
  def _filepath(self):
    if not os.path.exists(self._pathCollectedData):
      os.makedirs(self._pathCollectedData)
    return os.path.join(GeneralSettings._pathCollectedData, GeneralSettings._generalSettings)
  def get(self, key=None):
    if key is None:
      return self._generalSettings
    else:
      return self._generalSettings[key] if key in self._generalSettings else None
  def setStatistics(self, statistics):
    statistics = StatisticsTools.fixKeyTitle(statistics)
    if 'key' in statistics:
      if statistics['key'] not in self._generalSettings['statistics']:
        self._generalSettings['statistics'][statistics['key']] = statistics
      return statistics['key']
    return None
  def save(self):
    with open(self._filepath(), 'w') as f:
      json.dump(self._generalSettings, f)
    return self._generalSettings
