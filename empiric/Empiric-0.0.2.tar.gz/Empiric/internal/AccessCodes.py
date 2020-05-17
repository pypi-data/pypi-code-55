from Empiric.Mode import MODE

import os
import random
import string

class AccessCodes():
  _accessCodeLength = 8
  _fileAccessCodes = 'access-codes.csv'
  _defaultAccessCode = '_'
  def __init__(self, mode, numberOfAccessCodes):
    self._mode = mode
    self._accessCodes = []
    if self._mode == MODE.USE_ACCESS_CODES:
      self._accessCodes = None
      if os.path.exists(AccessCodes._fileAccessCodes):
        print(' * Load list of access codes')
        with open(AccessCodes._fileAccessCodes, 'r') as f:
          self._accessCodes = f.read().splitlines()
      if self._accessCodes is None or len(self._accessCodes) < numberOfAccessCodes:
        print(' * Generate list of access codes' if self._accessCodes is None else ' * Extend list of access codes')
        if self._accessCodes is None:
          self._accessCodes = []
        while len(self._accessCodes) < numberOfAccessCodes:
          accessCode = AccessCodes.newAccessCode()
          if accessCode not in self._accessCodes:
            self._accessCodes.append(accessCode)
        with open(AccessCodes._fileAccessCodes, 'w') as f:
          f.write('\n'.join(self._accessCodes))
  def exists(self, accessCode):
    if self._mode == MODE.LOCAL:
      return accessCode == AccessCodes._defaultAccessCode
    elif self._mode == MODE.USE_ACCESS_CODES:
      return accessCode in self._accessCodes
    elif self._mode == MODE.NO_ACCESS_CODES:
      return True
  @staticmethod
  def newAccessCode():
    x = ''.join(random.choice(string.ascii_letters) for _ in range(0, AccessCodes._accessCodeLength))
    for s in ['login', 'logout', 'save', 'settings', 'statistics', 'data']:
      if x.startswith(s):
        x = AccessCodes.newAccessCode()
    return x
  @staticmethod
  def defaultAccessCode():
    return AccessCodes._defaultAccessCode
