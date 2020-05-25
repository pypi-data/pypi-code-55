# -*- coding: utf-8 -*-
# pylint: disable=invalid-name, unused-import

import importlib
import sys
import threading

import mmaare

# pylint: disable=import-error
from .hakemisto import Versiohakemisto
from .jakelu import _jakelu
from .luokka import Versio, Versiot
from .moduuli import _versio, _versiot
# pylint: enable=import-error


_lukko = threading.RLock()
def tuotu(moduuli):
  '''
  Aseta moduulin tietoihin määreet __jakelu__, __versio__ ja __versiot__.
  '''
  with _lukko:
    mmaare(_jakelu, nimi='__jakelu__', moduuli=moduuli)
    mmaare(_versio, nimi='__versio__', moduuli=moduuli)
    mmaare(_versiot, nimi='__versiot__', moduuli=moduuli)
  # def tuotu


class Lataaja:

  def __init__(self, lataaja):
    self.lataaja = lataaja

  def load_module(self, fullname):
    module = self.lataaja.load_module(fullname)
    tuotu(module)
    return module

  # class Lataaja


class Etsija:

  def __init__(self):
    self.kaynnissa = set()

  def find_module(self, fullname, path=None):
    with _lukko:
      if fullname in self.kaynnissa:
        return None
      self.kaynnissa.add(fullname)
      try:
        try:
          lataaja = importlib.util.find_spec(fullname).loader
        except (ImportError, AttributeError):
          # pylint: disable=deprecated-method
          lataaja = importlib.find_loader(fullname, path)
        if lataaja:
          return Lataaja(lataaja)
        else:
          return None
      finally:
        self.kaynnissa.remove(fullname)
      # with _lukko
    # def find_module

  # class Etsija


# Lisää edellä kuvatut määreet automaattisesti
# tämän jälkeen tuotuihin moduuleihin.
sys.meta_path.insert(0, Etsija())


# Lisää määreet heti aiemmin tuotuihin moduuleihin.
for aiemmin_tuotu_moduuli in sys.modules.values():
  tuotu(aiemmin_tuotu_moduuli)
