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


def _versiot(moduuli):
  '''
  Etsi levyltä kaikki versiot moduulista ja palauta kohteet
  sanakirjana (Versiohakemistona).

  Python-tiedostoja etsitään nimellä <moduuli>-<versio>.py, missä
  moduuli vastaa `moduuli.__file__`-arvoa (ilman .py-päätettä).

  Kullekin versioidulle, sanakirjaan lisättävälle kohteelle
  lisätään määre __versio__, joka sisältää vastaavan versionumeron.
  '''
  # Etsi vanhempia versioita moduulin nimen mukaan.
  try: tiedosto = moduuli.__file__
  except AttributeError: return None

  # Kerätään levyltä löytyneet versiot sanakirjaan.
  versiot = {}

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
    sys.modules[nimi] = versioitu_moduuli
    try:
      spec.loader.exec_module(versioitu_moduuli)
    except: # pylint: disable=bare-except
      sys.modules.pop(nimi)
    else:
      versiot[versio] = versioitu_moduuli
    # for versioitu_tiedosto

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
