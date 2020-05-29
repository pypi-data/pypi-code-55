# -*- coding: utf-8 -*-

import collections

import pkg_resources


class Versiohakemisto(collections.OrderedDict):
  '''
  Sanakirjaluokka, joka palauttaa pyydettyä avainta lähinnä
  vastaavan, saman tai aiemman version.

  Sanakirjaan kuuluminen määräytyy sen mukaan, sisältääkö
  se vähintään yhden kysyttyä avainta vastaavan tai vanhemman
  version.
  '''

  def __contains__(self, versio):
    if isinstance(versio, str):
      versio = pkg_resources.parse_version(versio)
    if not isinstance(versio, pkg_resources.packaging.version.Version):
      return False
    return next(iter(self)) <= versio
    # def __contains__

  def __getitem__(self, versio):
    if isinstance(versio, str):
      versio = pkg_resources.parse_version(versio)
    if not isinstance(versio, pkg_resources.packaging.version.Version):
      raise KeyError(repr(versio))
    for avain, arvo in reversed(self.items()):
      if avain <= versio:
        return arvo
    raise KeyError(repr(versio))
    # def __getitem__

  # class Versiohakemisto
