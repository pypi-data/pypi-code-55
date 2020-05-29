# -*- coding: utf-8 -*-
# pylint: disable=invalid-name

import glob
import importlib
import os
import re
import sys

import pkg_resources

from .hakemisto import Versiohakemisto


def _versio(moduuli):
  jakelu = moduuli.__jakelu__
  return jakelu.parsed_version if jakelu is not None else None
  # def _versio


class Sisallonlataaja(importlib.machinery.SourceFileLoader):
  ''' Lataa moduuli muistissa olevasta tiedostosisällöstä. '''
  def __init__(self, fullname, path, sisalto):
    super().__init__(fullname, path)
    self.sisalto = sisalto
  def get_data(self, path):
    return self.sisalto
  # class Sisallonlataaja


def _versiot_kehitettavassa_paketissa(moduuli):
  '''
  Etsi git-tietovarastosta kaikki versiointimäärityksen mukaiset
  aiemmat versiot moduulin määrittelevästä tiedostosta.

  Edellyttää `git-versiointi`-paketin asennusta.
  '''
  # pylint: disable=import-error
  try:
    pkg_resources.require('git-versiointi>=1.4.4')
  except pkg_resources.DistributionNotFound:
    return

  from versiointi.tiedostot import tiedostoversiot
  from versiointi.versiointi import Versiointi

  for versio, tiedostosisalto in tiedostoversiot(
    Versiointi(moduuli.__jakelu__.location),
    os.path.relpath(
      os.path.realpath(moduuli.__file__),
      os.path.realpath(moduuli.__jakelu__.location),
    )
  ):
    nimi = '-'.join((moduuli.__name__, str(versio)))
    spec = importlib.util.spec_from_loader(nimi, Sisallonlataaja(
      nimi,
      f'-{versio}'.join(os.path.splitext(
        moduuli.__file__
      )),
      tiedostosisalto
    ))
    versioitu_moduuli = importlib.util.module_from_spec(spec)
    versioitu_moduuli.__versio__ = pkg_resources.parse_version(versio)
    yield versioitu_moduuli
    # for versio, tiedostosisalto in tiedostoversiot
  # def _versiot_kehitettavassa_paketissa


def _versiot_asennetussa_paketissa(moduuli):
  '''
  Etsi levyltä kaikki versiot moduulin määrittelevästä tiedostosta.

  Python-tiedostoja etsitään nimellä <moduuli>-<versio>.py, missä
  moduuli vastaa `moduuli.__file__`-arvoa (ilman .py-päätettä).
  '''
  # Etsi vanhempia versioita moduulin nimen mukaan.
  try: tiedosto = moduuli.__file__
  except AttributeError: return

  alku, loppu = os.path.splitext(tiedosto)
  for versioitu_tiedosto in glob.glob('-*'.join((alku, loppu))):
    versio = pkg_resources.parse_version(re.sub(
      rf'-(.*){loppu}', r'\1', versioitu_tiedosto.replace(alku, '')
    ))
    nimi = '-'.join((moduuli.__name__, str(versio)))

    # Lataa versioidun moduulitiedoston sisältö;
    # ks. https://docs.python.org/3.6/library/importlib.html, kpl 31.5.6.3.
    spec = importlib.util.spec_from_file_location(
      nimi, versioitu_tiedosto,
    )
    versioitu_moduuli = importlib.util.module_from_spec(spec)
    versioitu_moduuli.__versio__ = versio
    yield versioitu_moduuli
    # for versioitu_tiedosto
  # def _versiot_asennetussa_paketissa


def _versiot(moduuli):
  '''
  Etsi kaikki saatavilla olevat versiot moduulista ja palauta ne
  sanakirjana (Versiohakemistona).
  '''
  # Kootaan olemassaolevat versiot sanakirjaan.
  versiot = {}
  for versioitu_moduuli in (
    _versiot_asennetussa_paketissa(moduuli)
    if moduuli.__jakelu__.has_metadata('RECORD')
    else _versiot_kehitettavassa_paketissa(moduuli)
  ):
    sys.modules[versioitu_moduuli.__name__] = versioitu_moduuli
    try:
      versioitu_moduuli.__loader__.exec_module(versioitu_moduuli)
    except: # pylint: disable=bare-except
      sys.modules.pop(versioitu_moduuli.__name__)
    else:
      versiot[versioitu_moduuli.__versio__] = versioitu_moduuli
    # for versioitu_moduuli

  # Muodosta ja aseta versiohakemisto.
  jarjestetyt_versionumerot = sorted(versiot)
  return Versiohakemisto((*zip(
    jarjestetyt_versionumerot,
    map(versiot.get, jarjestetyt_versionumerot)
  ), (
    # Lisää nykyinen versio.
    moduuli.__versio__ or pkg_resources.parse_version('0'),
    moduuli,
  )))
  # def _versiot
